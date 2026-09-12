"""Performance statistics and the rolling comparisons against buy and hold.

Inputs are daily log returns. The mean of a log return series times 252 is the
continuously compounded annual return, so the annualised figure and the Sharpe
numerator come from the same quantity. Volatility uses the total return
standard deviation.
"""

import numpy as np
import pandas as pd

from config import ROLLING_YEARS, TRADING_DAYS_PER_YEAR as PERIODS


def summary(returns, risk_free):
    """Annualised return and volatility, Sharpe, Sortino and maximum drawdown."""
    excess = (returns - risk_free.reindex(returns.index)).mean() * PERIODS
    volatility = returns.std() * np.sqrt(PERIODS)
    # Downside deviation is the root lower partial moment about zero, not the
    # standard deviation of the negative observations.
    downside = np.sqrt((np.minimum(returns, 0.0) ** 2).mean()) * np.sqrt(PERIODS)
    equity = np.exp(returns.cumsum())
    return pd.Series({
        "ann_return": 100 * returns.mean() * PERIODS,
        "ann_volatility": 100 * volatility,
        "sharpe": excess / volatility,
        "sortino": excess / downside,
        "max_drawdown": 100 * (equity / equity.cummax() - 1.0).min(),
    })


def table(strategies, risk_free):
    return pd.DataFrame({name: summary(r, risk_free) for name, r in strategies.items()}).T


def rolling_alpha(returns, benchmark, years=ROLLING_YEARS):
    """Trailing annualised return of the strategy less that of the benchmark."""
    window = years * PERIODS
    difference = returns - benchmark.reindex(returns.index)
    return (difference.rolling(window).mean() * PERIODS).dropna()


def rolling_sharpe(returns, risk_free, years=ROLLING_YEARS):
    window = years * PERIODS
    excess = returns - risk_free.reindex(returns.index)
    volatility = returns.rolling(window).std() * np.sqrt(PERIODS)
    return (excess.rolling(window).mean() * PERIODS / volatility).dropna()
