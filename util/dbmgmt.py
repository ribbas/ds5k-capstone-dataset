#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from sqlite3 import Error as sql_error

from . import *


class DataBase(object):

    def __init__(self, db_path, detect_types=True):

        self.db_path = db_path
        self.con = sqlite3.connect(db_path, detect_types=detect_types)
        iprint("Connected to '{}'".format(db_path))
        self.fields = None

    def __del__(self):

        iprint("Disconnected from '{}'".format(self.db_path))

    def create(self, table, fields, force=False):

        with self.con:

            if force:
                iprint("Dropping table '{}'".format(table))
                self.con.execute("DROP TABLE IF EXISTS {}".format(table))

            iprint("Creating table '{}' with fields '{}'".format(table, fields))
            try:
                self.con.execute(
                    "CREATE TABLE IF NOT EXISTS {} ({})".format(
                        table,
                        ", ".join(" ".join(i) for i in fields)
                    )
                )
                sprint("Create successful")
                self.fields = fields

            except sql_error as e:
                eprint(
                    "DATABASE ERROR OF TYPE {} -> {}".format(
                        e.__class__.__name__, e)
                )

    def dump(self, table, limit=None):

        with self.con:
            if limit:
                return self.con.execute(
                    "SELECT * FROM {} LIMIT {}".format(table, limit))
            else:
                return self.con.execute("SELECT * FROM {}".format(table))

    def insert(self, table, data, fields=None):

        if not fields:
            fields = self.fields

        iprint("Inserting into table '{}'".format(table))
        with self.con:
            try:
                self.con.executemany(
                    "INSERT INTO {}({}) VALUES ({})".format(
                        table, ', '.join(i[0] for i in fields[1:]),
                        ','.join(['?'] * (len(fields) - 1))
                    ), data
                )
                sprint("Insert successful")
                self.count(table)
            except sql_error as e:
                eprint(
                    "DATABASE ERROR OF TYPE {} -> {}".format(
                        e.__class__.__name__, e)
                )

    def count(self, table, cond=None):

        with self.con:
            try:
                cur = self.con.execute(
                    "SELECT COUNT(*) FROM {}".format(table)).fetchone()
                iprint("Row count of table '{}': {}".format(table, cur[0]))
            except sql_error as e:
                eprint(
                    "DATABASE ERROR OF TYPE {} -> {}".format(
                        e.__class__.__name__, e)
                )

    def query(self, q):

        with self.con:
            try:
                return self.con.execute(q)

            except sql_error as e:
                eprint(
                    "DATABASE ERROR OF TYPE {} -> {}".format(
                        e.__class__.__name__, e)
                )
