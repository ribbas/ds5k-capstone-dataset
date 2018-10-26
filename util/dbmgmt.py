#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from sqlite3 import Error as sql_error

from . import *


class DataBase(object):

    def __init__(self, db_path, detect_types=True):

        self.db_path = db_path
        self.con = sqlite3.connect(
            db_path, detect_types=detect_types)
        iprint("Connected to '{}'".format(db_path))
        self.fields = None

    def __del__(self):

        iprint("Disconnected from '{}'".format(self.db_path))

    def create(self, table, fields):

        iprint("Creating table '{}' with fields '{}'".format(table, fields))
        with self.con:
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
                eprint("DATABASE ERROR OF TYPE {} -> {}".format(type(e), e))

    def dump(self, table, limit=None):

        with self.con:
            if limit:
                data = self.con.execute(
                    "SELECT * FROM {} LIMIT {}".format(table, limit))
            else:
                data = self.con.execute("SELECT * FROM {}".format(table))

        return data.fetchall()

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
                eprint("DATABASE ERROR OF TYPE {} -> {}".format(type(e), e))

    def count(self, table, cond=None):

        with self.con:
            try:
                cur = self.con.execute(
                    "SELECT COUNT(*) FROM {}".format(table)).fetchone()
                iprint("Row count of table '{}': {}".format(table, cur[0]))
            except sql_error as e:
                eprint("DATABASE ERROR OF TYPE {} -> {}".format(type(e), e))
