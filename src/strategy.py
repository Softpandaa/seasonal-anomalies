"""Position construction.

Entry is at the close of the last trading day of October and exit at the close
of the last trading day of April, so the position must already be on for the
first trading day of November. With profit and loss formed as w_{t-1} r_t, the
indicator therefore looks one trading day ahead of the calendar test.
"""

import numpy as np
import pandas as pd

from config import (
    DIVIDEND_YIELD,
    HALLOWEEN_MONTHS,
    POSITION_CAP,
    TOM_BACKWARD_DAYS,
    TOM_FORWARD_DAYS,
    TRADING_DAYS_PER_YEAR,
    TRANSACTION_COST,
)


def _next_day(flag):
    """Shift a per-day calendar flag back one trading day."""
    return flag.shift(-1).fillna(False).astype(bool)


def halloween_flag(frame):
    return _next_day(pd.Series(frame.index.month.isin(HALLOWEEN_MONTHS), index=frame.index))


def turn_of_month_flag(frame):
    inside = (frame["day_fwd"] <= TOM_FORWARD_DAYS) | (frame["day_bwd"] >= -TOM_BACKWARD_DAYS)
    return _next_day(inside)


def position(frame, turn_of_month=False):
    weight = halloween_flag(frame).astype(float)
    if turn_of_month:
        weight += turn_of_month_flag(frame).astype(float)
    return weight.clip(upper=POSITION_CAP)


def benchmark(frame, dividends=True):
    """Buy and hold log return.

    A position held every trading day receives the whole annual dividend
    whatever its timing, so the average yield is exact here. It is not applied
    to the seasonal strategies, whose dividend capture depends on timing the
    annual figure cannot resolve.

    No transaction cost is charged. A single entry over the sample is worth five
    basis points in total and is immaterial against the strategies' turnover.
    """
    simple = frame["ret"].copy()
    if dividends:
        simple = simple + DIVIDEND_YIELD / TRADING_DAYS_PER_YEAR
    return np.log1p(simple).dropna()


def returns(frame, weight, cost=TRANSACTION_COST):
    """Daily strategy log return.

    The portfolio is combined in simple returns, which is the only form that
    weights across positions, and the result is converted to a log return so
    every statistic downstream is on one scale.
    """
    held = weight.shift(1)
    traded = np.abs(weight.shift(1) - weight.shift(2)).fillna(0.0)
    simple = held * frame["ret"] + (1.0 - held) * frame["rf"] - cost * traded
    return np.log1p(simple).dropna()
