"""Load the committed series and build the return and calendar variables."""

import numpy as np
import pandas as pd

from config import (DTB3_FILE, PRICE_START, SAMPLE_END, SAMPLE_START, SPX_FILE,
                    TRADING_DAYS_PER_YEAR)


def _read(path):
    frame = pd.read_csv(path, parse_dates=["date"], index_col="date")
    return frame["close"].astype(float).sort_index().loc[PRICE_START:SAMPLE_END]


def load_daily():
    """Daily price, return, risk-free accrual and day position from month start and end."""
    spx = _read(SPX_FILE)
    bill = _read(DTB3_FILE)

    # H.15 quotes a discount rate, converted here to a bond equivalent yield.
    discount = bill / 100.0
    bey = 365.0 * discount / (360.0 - 91.0 * discount)

    frame = pd.DataFrame({"price": spx})
    frame["ret"] = frame["price"].pct_change()
    # H.15 skips some equity trading days, while the bill still accrues.
    frame["rf"] = bey.reindex(frame.index).ffill() / TRADING_DAYS_PER_YEAR

    # The first row has no return.
    frame = frame.dropna()

    month = frame.index.to_period("M")
    position = frame.groupby(month).cumcount() + 1
    length = month.map(frame.groupby(month).size())
    frame["day_fwd"] = position
    frame["day_bwd"] = position - length - 1

    return frame.loc[SAMPLE_START:SAMPLE_END]


def monthly_returns():
    """Month log returns over the sample."""
    month_end = _read(SPX_FILE).resample("ME").last()
    return np.log(month_end).diff().dropna().loc[SAMPLE_START:SAMPLE_END]
