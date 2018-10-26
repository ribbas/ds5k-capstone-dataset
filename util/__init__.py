#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from termcolor import cprint


def __arg_fmt(*args):

    return ("{} {} " * len(args)).format(datetime.now().strftime('%H:%M:%S'), *args)


def eprint(*io):

    cprint(__arg_fmt(*io), "red")


def wprint(*io):

    cprint(__arg_fmt(*io), "yellow")


def sprint(*io):

    cprint(__arg_fmt(*io), "green")


def iprint(*io):

    cprint(__arg_fmt(*io), "blue")
