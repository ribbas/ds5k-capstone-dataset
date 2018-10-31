#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os

from spotify.spotify import SpotifyWrapper
from util import *
from util.dbmgmt import DataBase
from util.dbconfig import DB_PATH, ALBUM_FIELDS, \
    IND_REVIEW_FIELDS, REVIEW_FIELDS, GENRE_FIELDS
from util.parsers import normalize_scores, get_earliest_date, get_genres, \
    get_reviewers


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="Album Reviews x Features Dataset Driver")
    parser.add_argument("--db", help="Path of database")

    parser.add_argument("--tables", nargs="+", help="Database tables")
    db_actions = {"dump": "Dump database tables", }
    # print({method: func.__code__.co_varnames[1:func.__code__.co_argcount] for method,
    #        func in DataBase.__dict__.items() if method[:2] != "__"})

    parser.add_argument("--list_db", "-l", action="store_true",
                        help="List database table actions")

    for k, v in db_actions.items():
        parser.add_argument("--" + k, action="store_true",
                            help=v)

    parser.add_argument("--reviews",
                        help="Scrape supported reviews site",
                        choices=("allmusic", "metacritic", "pitchfork"))
    parser.add_argument("--pages", nargs=2, metavar="n",
                        help="Pages to scrape supported reviews site",
                        default=[0, 1], type=int)
    parser.add_argument(
        "--spotify", nargs="*", action="store",
        help="Use Spotify API to analyze album track audio features")

    args = parser.parse_args().__dict__
    if args["db"] and args["db"].split(".")[-1] == "sqlite3" \
            and os.path.exists(args["db"]):
        print(args)

    if args["list_db"]:
        iprint("Database actions available:")
        for k, v in db_actions.items():
            iprint(k, v)

    if args["spotify"] is not None and len(args["spotify"]) in (0, 2):
        try:
            # OAuth credentials, a 2-tuple of CLIENT_TOKEN and CLIENT_SECRET
            from spotify.secret import CREDS
            iprint("Client credentials found")
        except ImportError:
            iprint("Saving client credentials")
            with open("spotify/secret.py", "w") as creds_file:
                creds_file.write(
                    "CREDS = (\"{}\", \"{}\")".format(*args["spotify"]))

    print(args)
