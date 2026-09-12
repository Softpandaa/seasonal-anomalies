# Seasonal Anomalies

Monthly and daily calendar seasonality in the S&P 500 over 1981 to 2023, and whether the Halloween and turn of month effects survive as tradable strategies once the risk free leg and transaction costs are charged.

## Findings

The seasonal pattern is real but narrow. November to April exceeds May to October by 0.81% per month, driven by the weakness of September and the strength of the year end. The January effect is not stable, changing sign in half of all five year windows, and the January barometer is rejected.

Neither strategy beats the total return benchmark. The Halloween strategy reaches a Sharpe ratio of 0.360 and the combined Halloween and turn of month strategy reaches 0.377, against 0.376 for buy and hold with dividends. The only improvement is in drawdown, which is seven percentage points shallower. Rolling outperformance and the rolling Sharpe advantage both narrow monotonically across the sample, which is the alpha decay of the title.

## Layout

```
data/     committed inputs
src/      analysis modules, every parameter declared once in config.py
latex/    main.tex and its figures
report.pdf
```

## Data

`data/spx.csv` is the S&P 500 daily close from Yahoo Finance. `data/dtb3.csv` is the three month Treasury bill secondary market rate on a discount basis, series DTB3 of the Federal Reserve H.15 release, retrieved from FRED. Both run from 1980, one year ahead of the sample, so the first return of the sample is complete. The bill is converted to a bond equivalent yield before it is accrued.

The total return benchmark is credited with an average annual dividend yield of 2.48%, the mean over 1980 to 2023, declared in `src/config.py`.

## Reproducing

Python 3.13.

```
pip install -r requirements.txt
python src/plots.py
```

This writes the twelve figures to `latex/figures/` and prints the performance table of the report. Compile `latex/main.tex` for the report itself.
