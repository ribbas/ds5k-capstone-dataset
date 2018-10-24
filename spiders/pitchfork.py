#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dateutil import parser as date_parser

from util import logs


class Pitchfork(object):

    def __init__(self):

        self.base_url = "https://pitchfork.com/"
        self.index_endp = "reviews/albums/?page={}"
        self.range_log = logs.PITCHFORK_RANGE
        self.urls_log = logs.PITCHFORK_URLS
        self.pages_range = []
        with open(self.range_log) as log_file:
            line = log_file.readline()
            if line == "init\n":
                line = log_file.readline().split()
                self.pages_range = range(
                    int(line[0]),
                    int(line[-1]) + 1
                )
            else:
                line = log_file.readline().split()
                self.pages_range = [int(i) for i in line]

        with open(self.urls_log) as log_file:
            self.urls = log_file.read().split()

    def scrape_urls(self, html):

        for tag in html.find_all("a", {"class": "review__link"}):
            self.urls.append(tag.get("href"))

    def scrape_album_data(self, html):

        data = ()

        found = 0
        for tag in html.find_all("h1", {"class": "single-album-tombstone__review-title"}):
            data = (tag.text, )
            found = 1
            break
        if not found:
            data = (None,)
        found = 0

        for tag in html.find_all("ul", {"class": "artist-links artist-list single-album-tombstone__artist-links"}):
            data = data + (tag.text, )
            found = 1
            break
        if not found:
            data = data + (None,)
        found = 0

        for tag in html.find_all("time", {"class": "pub-date"}):
            data = data + (date_parser.parse(tag.get("datetime")), )
            found = 1
            break
        if not found:
            data = data + (None,)
        found = 0

        for tag in html.find_all("a", {"class": "genre-list__link"}):
            data = data + (tag.text, )
            found = 1
            break
        if not found:
            data = data + (None,)
        found = 0

        for tag in html.find_all("span", {"class": "score"}):
            data = data + (tag.text, )
            found = 1
            break
        if not found:
            data = data + (None,)
        found = 0

        for tag in html.find_all("a", {"class": "authors-detail__display-name"}):
            data = data + (tag.text, )
            found = 1
            break
        if not found:
            data = data + (None,)

        return data
