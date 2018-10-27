# db = DataBase(DB_PATH)

# am_db = db.dump("allmusic")
# mc_db = db.dump("metacritic")
# pf_db = db.dump("pitchfork")

# print(pf_db)


#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

# OAuth credentials, a 2-tuple of CLIENT_TOKEN and CLIENT_SECRET
from spotify.secret import CREDS
from spotify.spotify import SpotifyWrapper
from util.dbmgmt import DataBase
from util.dbconfig import DB_PATH, SPOTIFY_FIELDS, FEATURE_FIELDS, IND_REVIEW_FIELDS
from util.parsers import normalize_scores, get_earliest_date

from pprint import pprint

"""
SELECT
    count(*)
    FROM allmusic AS am
    INNER JOIN metacritic AS mc ON am.album = mc.album
    INNER JOIN pitchfork AS pf ON am.album = pf.album
    WHERE (
        TRIM(am.album) == TRIM(pf.album) AND
        TRIM(am.album) == TRIM(mc.album) AND
        TRIM(am.artist) == TRIM(pf.artist) AND
        TRIM(am.artist) == TRIM(mc.artist)
    );
"""
if __name__ == '__main__':

    # db = DataBase(DB_PATH)

    # db.create("allmusic", IND_REVIEW_FIELDS)
    # db.create("metacritic", IND_REVIEW_FIELDS)
    # db.create("pitchfork", IND_REVIEW_FIELDS)
    # mc_db = db.dump("metacritic")
    # pf_db = db.dump("pitchfork")

    # print(pf_db)

    merge_db = DataBase(DB_PATH)
    tables = ("allmusic", "metacritic", "pitchfork")
    cond = ("allmusic.album == pitchfork.album AND "
            "allmusic.album == metacritic.album AND "
            "allmusic.artist == pitchfork.artist AND "
            "allmusic.artist == metacritic.artist")
    kind = "INNER"
    fields = [
        "allmusic.album", "allmusic.artist",
        "allmusic.genre", "metacritic.genre", "pitchfork.genre",
        "allmusic.time", "metacritic.time", "pitchfork.time",
        "allmusic.score", "metacritic.score", "pitchfork.score",
        "allmusic.reviewer", "metacritic.reviewer", "pitchfork.reviewer"
    ]
    join_col = "album"
    db = merge_db.join(tables=tables, cond=cond,
                       join_col=join_col, fields=fields)
    t = db.fetchone()
    t = db.fetchone()
    t = db.fetchone()
    t = db.fetchone()
    t = db.fetchone()

    print(t)
    print(normalize_scores(np.array(t[8:11]), np.array([5, 100, 10])))
    print(get_earliest_date(t[5:8]))
