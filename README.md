# Seasonal Anomalies

Monthly and daily calendar seasonality in the S&P 500 over 1981 to 2023, and whether the Halloween and turn of month effects are profitable as tradable strategies.

## Findings

The seasonal pattern is real but narrow. November to April exceeds May to October by 0.81% per month, driven by the weakness of September and the strength of the year end. The January effect is not stable, changing sign in half of all five year windows, and the January barometer is rejected.

Neither strategy beats the total return benchmark. The Halloween strategy reaches a Sharpe ratio of 0.360 and the combined Halloween and turn of month strategy reaches 0.377, against 0.376 for buy and hold with dividends. The only improvement is in drawdown, which is seven percentage points shallower. Rolling outperformance and the rolling Sharpe advantage both narrow monotonically over time, and the outperformance is not statistically significant.

## Layout

```
data/     committed inputs
src/      analysis modules, every parameter declared once in config.py
report.pdf
```

The report is distributed as a compiled PDF. Its typesetting source is not included.

## Data

`data/spx.csv` is the S&P 500 daily close from Yahoo Finance. `data/dtb3.csv` is the three month Treasury bill secondary market rate on a discount basis from from FRED. The total return benchmark is credited with an average annual dividend yield of 2.48%, the mean over 1980 to 2023, declared in `src/config.py`.

## Reproducing

Python 3.13.

```
pip install -r requirements.txt
python src/plots.py
```

This prints the performance table of the report and writes the twelve figures it uses to `figures/`, which is created on first run and is not tracked.
