"""Every parameter used by this project, declared once."""

from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
SPX_FILE = DATA_DIR / "spx.csv"
DTB3_FILE = DATA_DIR / "dtb3.csv"
FIGURE_DIR = Path(__file__).resolve().parent.parent / "figures"

# Prices are read from PRICE_START so the first return in the sample is complete.
# The analysis window itself is SAMPLE_START to SAMPLE_END, whole years only.
PRICE_START = "1980-01-01"
SAMPLE_START = "1981-01-01"
SAMPLE_END = "2023-12-31"

TRADING_DAYS_PER_YEAR = 252

# Average annual S&P 500 dividend yield over 1980 to 2023, credited to the
# total return benchmark only.
DIVIDEND_YIELD = 0.0248

# Canonical Halloween window, November through April.
HALLOWEEN_MONTHS = (11, 12, 1, 2, 3, 4)

# Turn of month, first five and last five trading days of each month.
TOM_FORWARD_DAYS = 5
TOM_BACKWARD_DAYS = 5

# One-way cost as a fraction of notional, charged on absolute position change.
TRANSACTION_COST = 0.0005

# Window for the rolling seasonality figures, in years.
ROLLING_YEARS = 5

# Leverage cap when the Halloween and turn-of-month signals coincide.
POSITION_CAP = 1.5
