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
        with open(self.range_log) as log_file:
            self.pages_range = range(
                int(log_file.readline()),
                int(log_file.readline()) + 1
            )

        with open(self.urls_log) as log_file:
            self.urls = set(log_file.read().split())

    def scrape_urls(self, html):

        for tag in html.find_all("a", {"class": "review__link"}):
            self.urls.add(tag.get("href"))

    def scrape_album_data(self, html):

        data = ()

        for tag in html.find_all("h1", {"class": "single-album-tombstone__review-title"}):
            data = (tag.text, )
            break

        for tag in html.find_all("ul", {"class": "artist-links artist-list single-album-tombstone__artist-links"}):
            data = data + (tag.text, )
            break

        for tag in html.find_all("time", {"class": "pub-date"}):
            data = data + (date_parser.parse(tag.get("datetime")), )
            break

        for tag in html.find_all("span", {"class": "score"}):
            data = data + (tag.text, )
            break

        for tag in html.find_all("a", {"class": "authors-detail__display-name"}):
            data = data + (tag.text, )
            break

        return data
