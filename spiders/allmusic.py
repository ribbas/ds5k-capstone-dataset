#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import datetime
from dateutil import parser as date_parser
import dateutil.relativedelta as relativedelta
import dateutil.rrule as rrule

from util import *
from util import logs


class AllMusic(object):

    def __init__(self):

        self.base_url = "https://www.allmusic.com/newreleases/all/"
        self.index_endp = ""

        self.range_log = logs.ALLMUSIC_RANGE
        self.urls_log = logs.ALLMUSIC_URLS

        self.index_only = True

        self.pages_range = []
        self.urls = []
        start_date = datetime(2012, 1, 1)
        end_date = datetime(2015, 12, 31)
        rr = rrule.rrule(rrule.WEEKLY, byweekday=relativedelta.FR,
                         dtstart=start_date)
        x = rr.between(start_date, end_date, True)
        all_fridays = [
            str(i.year) + str(i.month).zfill(2) + str(i.day).zfill(2)
            for i in x]
        with open(self.range_log) as log_file:
            line = log_file.readline()
            if line == "init\n":
                self.urls = all_fridays
            else:
                line = line.split()
                self.urls = [i for i in all_fridays if i not in line]

    def scrape_urls(self, html):

        pass

    def scrape_album_data(self, html):

        albums = []
        artists = []
        genres = []
        scores = []
        data = []

        # album
        for tag in html.find_all("td", {"class": "album"}):
            albums.append(tag.find("a").text)

        # artist
        for tag in html.find_all("td", {"class": "artist"}):
            artist_tag = tag.find("a")
            if not artist_tag:
                artist_tag = tag
                if not artist_tag:
                    wprint("breaking")
                    break
            artist_tag = artist_tag.text.strip()
            if artist_tag:
                artists.append(artist_tag)

        # genre
        for tag in html.find_all("td", {"class": "genre"}):
            genre_tag = tag.find("a")
            if not genre_tag:
                genres.append(None)
            else:
                genres.append(genre_tag.text)

        # score
        for tag in html.find_all("td", {"class": "rating"}):
            score_tag = tag.find("span").get("class")[-1][-1]
            if score_tag == "-":
                scores.append(None)
            else:
                scores.append((int(score_tag) + 1) * 0.5)

        no_artist = len(artists)
        albums = albums[:no_artist]
        artists = artists[:no_artist]
        genres = genres[:no_artist]
        scores = scores[:no_artist]
        time = date_parser.parse(
            html.find("meta", {"property": "og:url"}
                      ).get("content").split("/")[-1]
        )

        for album, artist, genre, score in zip(albums, artists, genres, scores):
            if score:
                data.append((album, artist, time, genre, score, None))

        if len(data) < 10:
            wprint("Very low data count in URL: '/{}/'".format(time))

        return data
