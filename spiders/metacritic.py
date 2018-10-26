#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dateutil import parser as date_parser

from util import *
from util import logs


class Metacritic(object):

    def __init__(self):

        self.base_url = "https://www.metacritic.com/browse/albums/release-date/available/date?view=detailed&page="
        self.index_endp = ""
        self.range_log = logs.METACRITIC_RANGE
        self.urls_log = logs.METACRITIC_URLS
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

        self.urls = [str(i) for i in range(len(self.pages_range))]
        self.index_only = True

    def scrape_urls(self, html):

        pass

    def scrape_album_data(self, html):

        albums = []
        artists = []
        genres = []
        scores = []
        times = []
        data = []

        # album
        for tag in html.find_all("h3", {"class": "product_title"}):
            albums.append(tag.find("a").text)

        # artist
        for tag in html.find_all("span", {"class": "product_artist"}):
            artists.append(tag.text.replace(" - ", ""))

        for tag in html.find_all("ul", {"class": "more_stats"}):
            # time
            time_tag = tag.find("li", {"class": "release_date"})
            times.append(date_parser.parse(
                time_tag.find("span", {"class": "data"}).text))
            # genre
            genre_tag = tag.find("li", {"class": "stat genre"})
            if genre_tag:
                genres.append(
                    genre_tag.find("span", {"class": "data"}).text.replace(
                        ' ', '').replace("\n", "").replace(",", ", ")
                )
            else:
                genres.append(None)

        # score
        for tag in html.find_all("span", {"class": "metascore_w"}):
            scores.append(tag.text)

        len_fields = {len(albums), len(artists), len(
            times), len(genres), len(scores)}
        if len(len_fields) == 1:
            for fields in zip(albums, artists, times, genres, scores):
                data.append(fields + (None,))
        elif 0 in len_fields:
            eprint("EMPTY FIELDS")
            sys.exit(1)
        else:
            eprint("MISSING FIELDS")
            sys.exit(1)

        return data
