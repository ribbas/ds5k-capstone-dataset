#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

import numpy as np

from .genreconfig import *


def normalize_scores(actuals, maxes):

    scores = (np.array(actuals) / np.array(maxes)) * 100
    return (*scores, np.mean(scores), np.std(scores))


def get_earliest_date(dates):

    return np.min(dates)


def get_genres(genres):

    def __clean_delims(_str):

        return _str.lower().replace(" ", "")

    genres = [
        __clean_delims(item)
        for sublist in genres if sublist for item in sublist.split(",")]

    genres_vec = GENRES_VEC[:]
    not_null = 0
    for genre in genres:

        if genre not in AMBIGUOUS or not not_null:
            not_null = 1

            if genre in CLASSICAL or "classical" in genre:
                genres_vec[GENRES.index("classical")] = 1

            if genre in COUNTRY or "country" in genre:
                genres_vec[GENRES.index("country")] = 1

            if genre in ELECTRONIC or "electro" in genre:
                genres_vec[GENRES.index("electronic")] = 1

            if genre in EXPERIMENTAL or "experimental" in genre:
                genres_vec[GENRES.index("experimental")] = 1

            if genre in FOLK or "folk" in genre:
                genres_vec[GENRES.index("folk")] = 1

            if genre in HIPHOP or "rap" in genre or "hip-hop" in genre:
                genres_vec[GENRES.index("hiphop")] = 1

            if genre in INTERNATIONAL or "international" in genre:
                genres_vec[GENRES.index("international")] = 1

            if genre in JAZZ or "jazz" in genre:
                genres_vec[GENRES.index("jazz")] = 1

            if genre in METAL or "metal" in genre or "core" in genre:
                genres_vec[GENRES.index("metal")] = 1

            if genre in POP or "pop" in genre or "r&b" in genre:
                genres_vec[GENRES.index("pop")] = 1

            if genre in ROCK or "rock" in genre or "punk" in genre:
                genres_vec[GENRES.index("rock")] = 1

    return genres_vec


def get_reviewers(reviewers):

    return ", ".join(filter(None, reviewers))
