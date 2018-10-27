#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np


def normalize_scores(actuals, maxes):

    scores = (actuals / maxes) * 100
    return (scores, np.mean(scores), np.std(scores))


def get_earliest_date(dates):

    return np.min(dates)
