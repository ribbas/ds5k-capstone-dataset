#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

from spotify.secret import CREDS
from spotify.spotify import SpotifyWrapper
from config import SPOTIFY_FIELDS

from pprint import pprint


class DataBase(object):

    def __init__(self, table_path, fields):

        self.con = sqlite3.connect(table_path)
        self.fields = fields

    def create(self, table):

        with self.con:
            print("CREATE TABLE IF NOT EXISTS {} ({})".format(
                table,
                ", ".join(" ".join(i) for i in self.fields)))
            self.con.execute(
                "CREATE TABLE IF NOT EXISTS {} ({})".format(
                    table,
                    ", ".join(" ".join(i) for i in self.fields)
                )
            )

    def dump(self, table, limit=None):

        with self.con:
            if limit:
                data = self.con.execute(
                    "SELECT * FROM {} LIMIT {}".format(table, limit))
            else:
                data = self.con.execute("SELECT * FROM {}".format(table))

        return list(data)

    def insert(self, table, data):

        with self.con:
            print(
                "INSERT INTO {}({}) VALUES ({})".format(
                    table, ', '.join(i[0] for i in self.fields[1:]),
                    ','.join(['?'] * (len(self.fields) - 1))
                )
            )
            self.con.executemany(
                "INSERT INTO {}({}) VALUES ({})".format(
                    table, ', '.join(i[0] for i in self.fields[1:]),
                    ','.join(['?'] * (len(self.fields) - 1))
                ), data
            )


if __name__ == '__main__':

    pitchfork = DataBase("pitchfork_kaggle.sqlite3", [])
    data = pitchfork.dump("reviews", 10)
    data = [i[1:3] for i in data]

    spotify_db = DataBase("db.sqlite3", SPOTIFY_FIELDS)
    spotify_db.create("spotify")

    obj = SpotifyWrapper(CREDS, data)
    obj.get_album_uri()
    obj.get_tracklist_uris()
    spotify_data = obj.get_table()
    spotify_db.insert("spotify", spotify_data)
