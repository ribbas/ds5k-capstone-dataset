#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from bs4 import BeautifulSoup
import requests

from util import *
from util.browserconfig import HEADERS


class Spider(object):

    def __init__(self, review_site):

        self.review_site = review_site()
        self.base_url = self.review_site.base_url
        self.index_url = self.base_url + self.review_site.index_endp
        self.pages_range = self.review_site.pages_range
        self.range_log = self.review_site.range_log
        self.urls_log = self.review_site.urls_log

        self.scrape_urls = self.review_site.scrape_urls
        self.scrape_album_data = self.review_site.scrape_album_data
        self.urls = self.review_site.urls
        self.data = []
        print("Initialize spider for '{}'".format(
            type(self.review_site).__name__))

    def get_urls(self):

        if len(self.pages_range) > 1:
            print("Scraping URLs from pages ({}, {})".format(
                self.pages_range[0], self.pages_range[-1]))
            cur_page = self.pages_range[0]
            for page_num in self.pages_range:

                iprint("Index page {}...".format(page_num))
                cur_page = page_num

                try:
                    page = requests.get(
                        self.index_url.format(page_num), HEADERS).text
                    soup = BeautifulSoup(page, "html.parser")
                    self.scrape_urls(soup)

                except KeyboardInterrupt:
                    wprint("Keyboard interrupt...")
                    sprint("Scraped {} URLs".format(len(self.urls)))
                    self._dump_mem(self.urls_log, self.urls)
                    self._dump_mem(self.range_log, (str(cur_page),
                                                    str(self.pages_range[-1])))
                    iprint("Dumped URLs to '{}'".format(self.urls_log))
                    sys.exit(0)

            sprint("Scraped {} URLs".format(len(self.urls)))
            self._dump_mem(self.urls_log, self.urls)
            self._dump_mem(self.range_log,
                           (str(cur_page), str(self.pages_range[-1])))
            iprint("Dumped URLs to '{}'".format(self.urls_log))

    def get_album_data(self):

        while self.urls:

            iprint("{} pages left".format(len(self.urls)))
            try:
                page_url = self.urls.pop()
                page = requests.get(self.base_url + page_url, HEADERS).text
                soup = BeautifulSoup(page, "html.parser")
                self.data.append(self.scrape_album_data(soup))

            except KeyboardInterrupt:
                wprint("Keyboard interrupt...")
                sprint("Scraped {} pages".format(len(self.data)))
                iprint("{} pages left".format(len(self.urls)))
                self._dump_mem(self.urls_log, self.urls)
                iprint("Dumped URLs to '{}'".format(self.urls_log))
                sys.exit(0)

        sprint("Scraped {} pages".format(len(self.data)))
        iprint("{} pages left".format(len(self.urls)))
        self._dump_mem(self.urls_log, self.urls)
        iprint("Dumped URLs to '{}'".format(self.urls_log))

    def _dump_mem(self, log_file, log_data):

        with open(log_file, "w") as log_fp:
            log_fp.write("\n".join(log_data))
