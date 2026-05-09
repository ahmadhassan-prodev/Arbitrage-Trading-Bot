import csv
import os
from datetime import datetime
from config import LOG_FILE

# ---------------- EXISTING FUNCTION (unchanged) ---------------- #
def log_opportunity(data):
    os.makedirs("logs", exist_ok=True)

    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "timestamp",
                "symbol",
                "spot_price",
                "futures_price",
                "spread_pct",
                "funding_rate",
                "net_spread",
                "volume"
            ])

        writer.writerow([
            datetime.utcnow().isoformat(),
            data["symbol"],
            data["spot_price"],
            data["futures_price"],
            data["spread_pct"],
            data["funding_rate"],
            data["net_spread"],
            data["volume"]
        ])


# ---------------- NEW FUNCTION FOR PAPER TRADES ---------------- #
def log_trade_result(trade_result, file_name="logs/paper_trades.csv"):
    """
    Logs the details of a paper trade after exit.
    Does not interfere with log_opportunity.
    """
    os.makedirs("logs", exist_ok=True)

    file_exists = os.path.isfile(file_name)

    with open(file_name, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "timestamp",
                "symbol",
                "entry_spread",
                "exit_spread",
                # "spread_velocity",
                "hold_minutes",
                "pnl",
                "exit_reason"
            ])

        writer.writerow([
            datetime.utcnow().isoformat(),
            trade_result["symbol"],
            trade_result["entry_spread"],
            trade_result["exit_spread"],
            # trade_result["spread_velocity"],
            trade_result["hold_minutes"],
            trade_result["pnl"],
            trade_result["exit_reason"]
        ])
