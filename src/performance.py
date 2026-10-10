"""Performance statistics of daily log returns and rolling comparisons with buy and hold."""

import numpy as np
import pandas as pd

from config import ROLLING_YEARS, TRADING_DAYS_PER_YEAR as PERIODS


def drawdown(returns):
    """Drawdown from the running peak (%)."""
    equity = np.exp(returns.cumsum())
    return 100 * (equity / equity.cummax() - 1.0)


def summary(returns, risk_free):
    """Annualised return and volatility, Sharpe, Sortino and maximum drawdown."""
    excess = (returns - risk_free.reindex(returns.index)).mean() * PERIODS
    volatility = returns.std() * np.sqrt(PERIODS)
    # Root lower partial moment about zero, not the std of negative returns.
    downside = np.sqrt((np.minimum(returns, 0.0) ** 2).mean()) * np.sqrt(PERIODS)
    return pd.Series({
        "ann_return": 100 * returns.mean() * PERIODS,
        "ann_volatility": 100 * volatility,
        "sharpe": excess / volatility,
        "sortino": excess / downside,
        "max_drawdown": drawdown(returns).min(),
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
