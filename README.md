# Seasonality Anomalies in the US Equity Market

This study examines what remains of monthly and daily calendar seasonality in the S&P 500 over 1981 to 2023, and whether the Halloween and turn-of-month effects still pay as trading strategies.

## Findings

The seasonal pattern is real but narrow. November to April beats May to October by 0.81% a month (Newey–West t = 2.46), driven by a weak September and a strong year end. January trails the other months in 48% of 5-year windows, and the data give no evidence for the January barometer.

Every index position, in both strategies and in buy and hold, earns the same average dividend yield. The combined strategy beats buy and hold on every measure, leading by 2.06% a year, though not significantly, and its lead shows no decline from 1981 to 2023. The Halloween strategy alone trails on return but has the higher Sharpe ratio.

## Layout

```
data/     committed inputs
src/      analysis modules, every parameter declared once in config.py
report.pdf
```

The report is distributed as a compiled PDF. Its typesetting source is not included.

## Data

`data/spx.csv` is the S&P 500 daily close from Yahoo Finance. `data/dtb3.csv` is the 3-month Treasury bill secondary market rate on a discount basis from FRED. Every index position earns an average annual dividend yield of 2.48%, the mean over 1980 to 2023, declared in `src/config.py`.

## Reproducing

Python 3.13.

```
pip install -r requirements.txt
python src/plots.py
```

This prints the performance table of the report and draws its twelve figures.
