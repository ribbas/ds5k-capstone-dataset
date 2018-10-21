#!/usr/bin/env python
# -*- coding: utf-8 -*-

# OAuth credentials, a 2-tuple of CLIENT_TOKEN and CLIENT_SECRET
from spotify.secret import CREDS
from spotify.spotify import SpotifyWrapper
from util.dbmgmt import DataBase
from util.dbconfig import SPOTIFY_FIELDS

from pprint import pprint

if __name__ == '__main__':

    pf_db = DataBase("pitchfork_kaggle.sqlite3")
    pf_data = pf_db.dump("reviews", 10)
    pf_data = [i[1:3] for i in pf_data]

    spotify_db = DataBase("db.sqlite3")
    spotify_db.create("spotify", SPOTIFY_FIELDS)

    sp_obj = SpotifyWrapper(CREDS, pf_data)
    sp_obj.get_albums_uris()
    sp_obj.get_tracklists_uris()
    spotify_data = sp_obj.get_table()
    spotify_db.insert("spotify", SPOTIFY_FIELDS, spotify_data)
