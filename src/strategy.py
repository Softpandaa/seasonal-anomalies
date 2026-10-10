"""Positions, buy and hold benchmarks and strategy returns."""

import numpy as np
import pandas as pd

from config import (DIVIDEND_YIELD, HALLOWEEN_MONTHS, POSITION_CAP, TOM_BACKWARD_DAYS,
                    TOM_FORWARD_DAYS, TRADING_DAYS_PER_YEAR, TRANSACTION_COST)


def _next_day(flag):
    """Shift a calendar flag back one trading day, since profit and loss is w_{t-1} r_t."""
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
    """Buy and hold log return, without cost, plus the average dividend yield if `dividends`."""
    simple = frame["ret"].copy()
    if dividends:
        simple = simple + DIVIDEND_YIELD / TRADING_DAYS_PER_YEAR
    return np.log1p(simple).dropna()


def returns(frame, weight, cost=TRANSACTION_COST):
    """Daily log return of weight w_{t-1} in the index and 1 - w_{t-1} in bills, net of cost."""
    held = weight.shift(1)
    traded = held.diff().abs().fillna(0.0)
    simple = held * frame["ret"] + (1.0 - held) * frame["rf"] - cost * traded
    return np.log1p(simple).dropna()
