#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path

LOGS_DIR = path.join(path.dirname(path.dirname(path.abspath(__file__))), "logs")

PITCHFORK_RANGE = path.join(LOGS_DIR, "pf.range")
PITCHFORK_URLS = path.join(LOGS_DIR, "pf.urls")
