#!/usr/bin/env python
# -*- coding: utf-8 -*-

# OAuth credentials, a 2-tuple of CLIENT_TOKEN and CLIENT_SECRET
from spotify.secret import CREDS
from spotify.spotify import SpotifyWrapper
from util.dbmgmt import DataBase
from util.dbconfig import DB_PATH, SPOTIFY_FIELDS, FEATURE_FIELDS, IND_REVIEW_FIELDS

from spiders.spider import Spider
from spiders.pitchfork import Pitchfork

from pprint import pprint

if __name__ == '__main__':

    # pf_db = DataBase("pitchfork_kaggle.sqlite3")
    # pf_data = pf_db.dump("reviews", 20)
    # pf_data = [i[1:3] for i in pf_data]

    # spotify_db = DataBase("db.sqlite3")
    # spotify_db.create("spotify", SPOTIFY_FIELDS)

    # sp_obj = SpotifyWrapper(CREDS, pf_data)
    # sp_obj.get_albums_uris()
    # sp_obj.get_tracklists_uris()
    # spotify_db.insert("spotify", SPOTIFY_FIELDS, sp_obj.get_table())
    # del sp_obj

    # data = spotify_db.dump("spotify")
    # spotify_db.create("features", FEATURE_FIELDS)
    # sp_obj = SpotifyWrapper(CREDS, data)
    # sp_obj.get_tracks_analysis()
    # spotify_db.insert("features", FEATURE_FIELDS, sp_obj.get_table())

    pitchfork_db = DataBase(DB_PATH)
    pitchfork_db.create("pitchfork", IND_REVIEW_FIELDS)

    obj = Spider(Pitchfork, pitchfork_db, "pitchfork")
    obj.get_urls()
    obj.get_album_data()

    # pitchfork_db.insert("pitchfork", pitchfork_data)
