#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from termcolor import cprint


def __arg_fmt(*args):

    return datetime.now().strftime("%H:%M:%S | ") + \
        ("{}" * len(args)).format(*args)


def eprint(*ostream):

    cprint(__arg_fmt(*ostream), "red")


def wprint(*ostream):

    cprint(__arg_fmt(*ostream), "yellow")


def sprint(*ostream):

    cprint(__arg_fmt(*ostream), "green")


def iprint(*ostream):

    cprint(__arg_fmt(*ostream), "blue")
