SCAN_INTERVAL = 6  # seconds

LOG_FILE = "logs/arbitrage_log.csv"

CAPITAL = 150.0

# Exit thresholds
EXIT_SPREAD_TARGET = 0.10        # % (Rule 1)
EXIT_SPREAD_DROP = 0.30          # % (Rule 2 magnitude)
# SPREAD_VELOCITY_LIMIT = -0.20    # % per minute (Rule 2 speed)

MAX_HOLD_TIME = 60 * 60          # 60 minutes (Rule 5)
VOLATILITY_EXIT = 1.0            # % spot move (Rule 6)

PRICE_CHECK_INTERVAL = 1        # seconds
