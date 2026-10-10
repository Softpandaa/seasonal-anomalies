"""Every parameter used by this project, declared once."""

from pathlib import Path

# Paths -----------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
SPX_FILE = DATA_DIR / "spx.csv"
DTB3_FILE = DATA_DIR / "dtb3.csv"
FIGURE_DIR = ROOT / "figures"

# Sample ----------------------------------------------------------------------
PRICE_START = "1980-01-01"            # load start, so the first return is complete
SAMPLE_START = "1981-01-01"
SAMPLE_END = "2023-12-31"
TRADING_DAYS_PER_YEAR = 252

# Strategies ------------------------------------------------------------------
HALLOWEEN_MONTHS = (11, 12, 1, 2, 3, 4)
TOM_FORWARD_DAYS = 5                  # turn of month: first and last 5 trading days
TOM_BACKWARD_DAYS = 5
POSITION_CAP = 1.5                    # when both signals are on
TRANSACTION_COST = 0.0005             # one way, per unit of position change
DIVIDEND_YIELD = 0.0248               # P2 only, 1980 to 2023 mean

# Figures ---------------------------------------------------------------------
ROLLING_YEARS = 5
