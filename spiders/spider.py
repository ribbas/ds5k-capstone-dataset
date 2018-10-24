#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
import threading
import time

from bs4 import BeautifulSoup
import requests

from util import *
from util.browserconfig import HEADERS


from itertools import islice, chain


def window(seq, n=2):
    "Returns a sliding window (of width n) over data from the iterable"
    "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result


def missing_elements(L):
    missing = chain.from_iterable(range(x + 1, y)
                                  for x, y in window(L) if (y - x) > 1)
    return set(missing)


class Spider(object):

    def __init__(self, review_site, db, table):

        self.db = db
        self.table = table

        self.review_site = review_site
        self.base_url = self.review_site.base_url
        self.index_url = self.base_url + self.review_site.index_endp
        self.pages_range = self.review_site.pages_range
        self.range_log = self.review_site.range_log
        self.urls_log = self.review_site.urls_log

        self.scrape_urls = self.review_site.scrape_urls
        self.scrape_album_data = self.review_site.scrape_album_data
        self.urls = self.review_site.urls
        self.data = []

        self.n_threads = os.cpu_count() * 40

        self.pages_scraped = set()
        self.threads = []

        print("Initialize spider for '{}'".format(
            type(self.review_site).__name__))

    def split_list(self, seq):
        length = len(seq)
        return [seq[i * length // self.n_threads:
                    (i + 1) * length // self.n_threads]
                for i in range(self.n_threads)]

    def parse_urls(self, pages_range):

        if len(pages_range) > 1:
            thread_name = threading.current_thread().name
            iprint("{}: Scraping URLs from pages ({}, {})".format(
                thread_name, pages_range[0], pages_range[-1]))
            for page_num in pages_range:

                iprint("{}: Index page {}...".format(thread_name, page_num))

                page = requests.get(
                    self.index_url.format(page_num), HEADERS).text
                soup = BeautifulSoup(page, "html.parser")
                self.scrape_urls(soup)
                self.pages_scraped.add(page_num)

    def get_urls(self):

        pages_ranges = self.split_list(self.pages_range)

        for data_ix in range(len(pages_ranges)):
            t = threading.Thread(
                target=self.parse_urls, args=(pages_ranges[data_ix],))
            self.threads.append(t)
            t.start()

        for threads in self.threads:
            iprint("{} threads still active".format(threading.active_count()))
            threads.join()

        sprint("Scraped {} URLs".format(len(self.urls)))
        print(threading.active_count())
        self._dump_mem(self.urls_log, self.urls)
        self._dump_mem(self.range_log, missing_elements(
            sorted(self.pages_scraped)), False)
        iprint("Dumped URLs to '{}'".format(self.urls_log))

    def parse_album_data(self, urls):

        thread_name = threading.current_thread().name
        while urls:

            iprint("{}: {} pages left".format(thread_name, len(urls)))
            page_url = urls.pop()
            time.sleep(random.uniform(1.0, 3.0))
            page = requests.get(self.base_url + page_url, HEADERS).text
            soup = BeautifulSoup(page, "html.parser")
            self.data.append(self.scrape_album_data(soup))

    def get_album_data(self):

        urls = self.split_list(self.urls)

        for data_ix in range(len(urls)):
            t = threading.Thread(
                target=self.parse_album_data, args=(urls[data_ix],))
            self.threads.append(t)
            t.start()

        for threads in self.threads:
            iprint("{} threads still active".format(threading.active_count()))
            threads.join()

        sprint("Scraped {} pages".format(len(self.data)))
        iprint("{} pages left".format(len(self.urls)))

        self._dump_mem(self.urls_log, self.urls)
        iprint("Dumped URLs to '{}'".format(self.urls_log))

        self.db.insert(self.table, self.data)

    def _dump_mem(self, log_file, log_data, urls=True):

        with open(log_file, "w") as log_fp:
            if urls:
                log_fp.write("\n".join(log_data))
            else:
                log_fp.write("resume")
                log_fp.write(" ".join(log_data))