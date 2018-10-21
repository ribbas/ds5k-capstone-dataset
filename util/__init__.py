#!/usr/bin/env python
# -*- coding: utf-8 -*-

from termcolor import cprint


def __arg_fmt(*args):

    s = "{} " * len(args)
    return s.format(*args)


def eprint(*io):

    cprint(__arg_fmt(*io), "red")


def wprint(*io):

    cprint(__arg_fmt(*io), "yellow")


def sprint(*io):

    cprint(__arg_fmt(*io), "green")


def iprint(*io):

    cprint(__arg_fmt(*io), "blue")
