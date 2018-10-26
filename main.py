#!/usr/bin/env python
# -*- coding: utf-8 -*-

# OAuth credentials, a 2-tuple of CLIENT_TOKEN and CLIENT_SECRET
from spotify.secret import CREDS
from spotify.spotify import SpotifyWrapper
from util.dbmgmt import DataBase
from util.dbconfig import DB_PATH, SPOTIFY_FIELDS, FEATURE_FIELDS, IND_REVIEW_FIELDS

from spiders.spider import Spider
from spiders.allmusic import AllMusic
from spiders.metacritic import Metacritic

from dateutil import parser as date_parser
from pprint import pprint

if __name__ == '__main__':

    am_db = DataBase(DB_PATH)
    am_db.create("allmusic", IND_REVIEW_FIELDS)
    am_ob = Spider(AllMusic(), am_db, "allmusic")
    am_ob.get_album_data()
