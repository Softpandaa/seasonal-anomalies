"""Load the committed series and build the return and calendar variables."""

import numpy as np
import pandas as pd

from config import (
    DTB3_FILE,
    PRICE_START,
    SAMPLE_END,
    SAMPLE_START,
    SPX_FILE,
    TRADING_DAYS_PER_YEAR,
)


def _read(path):
    frame = pd.read_csv(path, parse_dates=["date"], index_col="date")
    return frame["close"].astype(float).sort_index()


def load_daily():
    """Daily frame indexed by trading date.

    Columns are the price return, the risk free daily accrual, and the forward
    and backward trading day position within the calendar month.
    """
    spx = _read(SPX_FILE).loc[PRICE_START:SAMPLE_END]
    bill = _read(DTB3_FILE).loc[PRICE_START:SAMPLE_END]

    # H.15 quotes the three month bill on a discount basis. Convert to a bond
    # equivalent yield before accruing it.
    discount = bill / 100.0
    bey = 365.0 * discount / (360.0 - 91.0 * discount)

    frame = pd.DataFrame({"price": spx})
    frame["ret"] = frame["price"].pct_change()
    # H.15 does not publish on every equity trading day; the bill still accrues.
    frame["rf"] = bey.reindex(frame.index).ffill() / TRADING_DAYS_PER_YEAR

    # Drop the first row, which has no return, before numbering the trading days,
    # so every month in the sample contributes to both the forward and the
    # backward position counts.
    frame = frame.dropna()

    month = frame.index.to_period("M")
    position = frame.groupby(month).cumcount() + 1
    length = month.map(frame.groupby(month).size())
    frame["day_fwd"] = position
    frame["day_bwd"] = position - length - 1

    return frame.loc[SAMPLE_START:SAMPLE_END]


def monthly_returns():
    """Month log returns over the sample, labelled by the month they belong to.

    Read from PRICE_START rather than from the daily frame so that the first
    month of the sample has a complete return and every year carries twelve.
    """
    month_end = _read(SPX_FILE).loc[PRICE_START:SAMPLE_END].resample("ME").last()
    return np.log(month_end).diff().dropna().loc[SAMPLE_START:SAMPLE_END]
