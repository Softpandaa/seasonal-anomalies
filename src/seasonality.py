"""Seasonal factor estimators, computed directly on the trading calendar.

The seasonal component of a classical additive decomposition is the mean of
the detrended series at each cycle position. Computing that directly avoids
assuming a fixed number of trading days per month.
"""

import pandas as pd
from scipy.stats import kendalltau

from config import HALLOWEEN_MONTHS


def monthly_factor(monthly):
    """Mean deviation of each calendar month from its own year's mean."""
    demeaned = monthly - monthly.groupby(monthly.index.year).transform("mean")
    return demeaned.groupby(demeaned.index.month).mean()


def daily_factor(frame, column):
    """Mean deviation of each trading day position from its own month's mean.

    `column` is either the forward or the backward trading day index.
    """
    month = frame.index.to_period("M")
    demeaned = frame["ret"] - frame["ret"].groupby(month).transform("mean")
    return demeaned.groupby(frame[column]).mean()


def rolling_split(monthly, mask, years, names):
    """Rolling mean monthly return inside and outside a calendar mask.

    Defined only where the trailing window is complete. `names` labels the two
    columns.
    """
    window = 12 * years
    complete = monthly.rolling(window).count() == window

    inside = monthly.where(mask).rolling(window, min_periods=1).mean()
    outside = monthly.where(~mask).rolling(window, min_periods=1).mean()

    frame = pd.DataFrame(
        {names[0]: inside.where(complete), names[1]: outside.where(complete)}
    ).dropna()
    frame["difference"] = frame[names[0]] - frame[names[1]]
    return frame


def rolling_halloween(monthly, years):
    mask = pd.Series(monthly.index.month.isin(HALLOWEEN_MONTHS), index=monthly.index)
    return rolling_split(monthly, mask, years, ("halloween", "non_halloween"))


def rolling_january(monthly, years):
    mask = pd.Series(monthly.index.month == 1, index=monthly.index)
    return rolling_split(monthly, mask, years, ("january", "non_january"))


def january_barometer(monthly):
    """January log return against the return over the rest of the year.

    Log returns aggregate by summation, so February to December is the sum of
    those eleven monthly figures.
    """
    january = monthly[monthly.index.month == 1].copy()
    january.index = january.index.year

    other = monthly[monthly.index.month != 1]
    rest = other.groupby(other.index.year).sum()

    return pd.DataFrame({"january": january, "rest": rest}).dropna()


def rolling_correlation(frame, column, window):
    """Rolling Pearson and Kendall correlation of January against `column`.

    `frame` carries one row per year, so `window` is a count of years. This
    differs from rolling_split, which takes years and converts to months.
    """
    rows = {}
    for i in range(window - 1, len(frame)):
        block = frame.iloc[i - window + 1 : i + 1]
        rows[frame.index[i]] = {
            "pearson": block["january"].corr(block[column]),
            "kendall": kendalltau(block["january"], block[column]).statistic,
        }
    return pd.DataFrame.from_dict(rows, orient="index")
