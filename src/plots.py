"""Figures for the seasonality analysis section."""

import matplotlib
matplotlib.use("Agg")

import matplotlib.dates as mdates

import matplotlib.pyplot as plt
import numpy as np

from config import FIGURE_DIR, ROLLING_YEARS, TOM_BACKWARD_DAYS, TOM_FORWARD_DAYS
import pandas as pd

import performance as pf
import strategy as st
from data import load_daily, monthly_returns
from seasonality import (
    daily_factor,
    january_barometer,
    monthly_factor,
    rolling_halloween,
    rolling_january,
    rolling_correlation,
)

# Okabe-Ito
BLUE, ORANGE, GREEN, GREY = "#0072B2", "#E69F00", "#009E73", "#666666"

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Latin Modern Roman", "DejaVu Serif"],
    "font.size": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.linewidth": 0.4,
    "grid.alpha": 0.35,
    "figure.dpi": 200,
    "savefig.bbox": "tight",
})

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def _save(fig, name):
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURE_DIR / name)
    plt.close(fig)


def _bar_by_month(values, ylabel, name):
    fig, ax = plt.subplots(figsize=(6.2, 3.2))
    colours = [BLUE if v >= 0 else ORANGE for v in values]
    ax.bar(range(1, 13), 100 * values.values, color=colours, width=0.68)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xticks(range(1, 13), MONTHS)
    ax.set_ylabel(ylabel)
    _save(fig, name)


def _bar_by_day(forward, backward, ylabel, name):
    labels = [f"+{j}" for j in range(1, TOM_FORWARD_DAYS + 1)]
    labels += [f"{j}" for j in range(-TOM_BACKWARD_DAYS, 0)]
    values = [forward.get(j, np.nan) for j in range(1, TOM_FORWARD_DAYS + 1)]
    values += [backward.get(j, np.nan) for j in range(-TOM_BACKWARD_DAYS, 0)]
    values = 100 * np.array(values, dtype=float)

    x = np.arange(len(values), dtype=float)
    x[TOM_FORWARD_DAYS:] += 0.8  # visual break between the two ends

    fig, ax = plt.subplots(figsize=(6.2, 3.2))
    ax.bar(x, values, color=[BLUE if v >= 0 else ORANGE for v in values], width=0.68)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xticks(x, labels)
    ax.set_ylabel(ylabel)
    _save(fig, name)


def _year_axis(ax):
    ax.xaxis.set_major_locator(mdates.YearLocator(5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))


def halloween_levels(rolling, name):
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    ax.plot(rolling.index, 100 * rolling["halloween"], color=BLUE,
            linewidth=1.4, linestyle="-", label="November to April")
    ax.plot(rolling.index, 100 * rolling["non_halloween"], color=ORANGE,
            linewidth=1.4, linestyle="--", label="May to October")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_ylabel("Mean monthly return (%)")
    ax.legend(frameon=False, loc="upper right")
    _year_axis(ax)
    _save(fig, name)


def halloween_gap(rolling, name):
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    gap = 100 * rolling["difference"]
    ax.plot(rolling.index, gap, color=GREEN, linewidth=1.4)
    ax.fill_between(rolling.index, 0, gap, where=gap >= 0, color=GREEN, alpha=0.18)
    ax.fill_between(rolling.index, 0, gap, where=gap < 0, color=ORANGE, alpha=0.18)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_ylabel("Nov-Apr minus May-Oct,\nmean monthly return (%)")
    _year_axis(ax)
    _save(fig, name)


def january_levels(rolling, name):
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    ax.plot(rolling.index, 100 * rolling["january"], color=BLUE,
            linewidth=1.4, linestyle="-", label="January")
    ax.plot(rolling.index, 100 * rolling["non_january"], color=ORANGE,
            linewidth=1.4, linestyle="--", label="All other months")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_ylabel("Mean monthly return (%)")
    ax.legend(frameon=False, loc="upper right")
    _year_axis(ax)
    _save(fig, name)


def barometer(frame, correlations, name):
    fig, (left, right) = plt.subplots(1, 2, figsize=(7.4, 3.2))

    left.scatter(100 * frame["january"], 100 * frame["rest"], s=18,
                 color=BLUE, alpha=0.8, edgecolor="none")
    left.axhline(0, color="black", linewidth=0.8)
    left.axvline(0, color="black", linewidth=0.8)
    left.set_xlabel("January return (%)")
    left.set_ylabel("February to December return (%)")

    right.plot(correlations.index, correlations["pearson"], color=BLUE,
               linewidth=1.4, linestyle="-", label="Pearson")
    right.plot(correlations.index, correlations["kendall"], color=ORANGE,
               linewidth=1.4, linestyle="--", label="Kendall")
    right.axhline(0, color="black", linewidth=0.8)
    right.set_ylim(-1.05, 1.05)
    right.set_xlabel("Year")
    right.set_ylabel("Rolling correlation")
    right.legend(frameon=False, loc="lower left")

    _save(fig, name)


STYLES = [(BLUE, "-"), (ORANGE, "--"), (GREEN, "-."), (GREY, ":")]


def _lines(curves, ylabel, name, logscale=False, zero=False, legend="upper left"):
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    for (label, series), (colour, dash) in zip(curves.items(), STYLES):
        ax.plot(series.index, series.values, color=colour, linewidth=1.4,
                linestyle=dash, label=label)
    if logscale:
        ax.set_yscale("log")
    if zero:
        ax.axhline(0, color="black", linewidth=0.8)
    ax.set_ylabel(ylabel)
    ax.legend(frameon=False, loc=legend)
    _year_axis(ax)
    _save(fig, name)


def underwater(returns):
    equity = np.exp(returns.cumsum())
    return 100 * (equity / equity.cummax() - 1.0)


def build():
    frame = load_daily()
    monthly = monthly_returns()

    _bar_by_month(monthly.groupby(monthly.index.month).mean(),
                  "Mean monthly return (%)", "returns_by_month.png")
    _bar_by_month(monthly_factor(monthly),
                  "Seasonal factor (%)", "factor_by_month.png")

    _bar_by_day(frame.groupby("day_fwd")["ret"].mean(),
                frame.groupby("day_bwd")["ret"].mean(),
                "Mean daily return (%)", "returns_by_day.png")
    _bar_by_day(daily_factor(frame, "day_fwd"), daily_factor(frame, "day_bwd"),
                "Seasonal factor (%)", "factor_by_day.png")

    rolling = rolling_halloween(monthly, ROLLING_YEARS)
    halloween_levels(rolling, "halloween_rolling_levels.png")
    halloween_gap(rolling, "halloween_rolling_gap.png")

    january_levels(rolling_january(monthly, ROLLING_YEARS), "january_rolling_levels.png")

    barometer_frame = january_barometer(monthly)
    barometer(barometer_frame,
              rolling_correlation(barometer_frame, "rest", ROLLING_YEARS),
              "january_barometer.png")

    r1 = st.returns(frame, st.position(frame))
    r2 = st.returns(frame, st.position(frame, turn_of_month=True))
    rb = st.benchmark(frame, dividends=False)

    rp = st.benchmark(frame, dividends=True)
    log_rf = np.log1p(frame["rf"])

    _lines({"S1": np.exp(r1.cumsum()), "S2": np.exp(r2.cumsum()), "P1": np.exp(rb.cumsum())},
           "Growth of one dollar, log scale", "equity_curves.png", logscale=True)

    _lines({"S1": 100 * pf.rolling_alpha(r1, rb), "S2": 100 * pf.rolling_alpha(r2, rb)},
           "Annualised return over P1 (%)", "rolling_outperformance.png", zero=True)

    _lines({"S1": pf.rolling_sharpe(r1, log_rf), "S2": pf.rolling_sharpe(r2, log_rf),
            "P1": pf.rolling_sharpe(rb, log_rf)},
           "Rolling Sharpe ratio", "rolling_sharpe.png", zero=True)

    _lines({"S1": underwater(r1), "S2": underwater(r2), "P1": underwater(rb)},
           "Drawdown from running peak (%)", "drawdown.png",
           zero=True, legend="lower left")

    return pf.table({
        "S1 Halloween": r1,
        "S2 Halloween and turn of month": r2,
        "P1 Buy and hold": rb,
        "P2 Buy and hold with dividend": rp,
    }, log_rf)


if __name__ == "__main__":
    pd.set_option("display.width", 200)
    print(build().round(3).to_string())
