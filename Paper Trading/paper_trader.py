import time
import requests
from config import *

SPOT_PRICE_URL = "https://api.binance.com/api/v3/ticker/price?symbol={}"
FUTURES_PRICE_URL = "https://fapi.binance.com/fapi/v1/ticker/price?symbol={}"
FUNDING_URL = "https://fapi.binance.com/fapi/v1/premiumIndex?symbol={}"

def get_price(url):
    return float(requests.get(url, timeout=5).json()["price"])

def get_funding(symbol):
    data = requests.get(FUNDING_URL.format(symbol), timeout=5).json()
    return float(data["lastFundingRate"]) * 100

def paper_trade(opportunity):
    symbol = opportunity["symbol"]

    entry_spot = opportunity["spot_price"]
    entry_futures = opportunity["futures_price"]
    entry_spread = opportunity["spread_pct"]

    entry_time = time.time()
    quantity = CAPITAL / entry_spot

    print(f"\n📥 ENTER PAPER TRADE: {symbol}")
    print(f"Entry spread: {entry_spread:.3f}%")

    # prev_spread = entry_spread

    while True:
        time.sleep(PRICE_CHECK_INTERVAL)

        spot_now = get_price(SPOT_PRICE_URL.format(symbol))
        futures_now = get_price(FUTURES_PRICE_URL.format(symbol))
        funding_now = get_funding(symbol)

        current_spread = (futures_now - spot_now) / spot_now * 100
        hold_time = time.time() - entry_time

        # spread_velocity = (
        #     (current_spread - prev_spread) /
        #     (PRICE_CHECK_INTERVAL / 60)
        # )

        spot_change = abs(
            (spot_now - entry_spot) / entry_spot * 100
        )

        print(
            f"⏱ Spread={current_spread:.3f}% | "
            # f"Vel={spread_velocity:.3f}%/min | "
            f"Funding={funding_now:.4f}% | "
            f"Hold={int(hold_time/60)}m"
        )

        # prev_spread = current_spread

        # ---------------- EXIT RULES ---------------- #

        # Rule 1 — Healthy convergence (profit)
        if current_spread <= EXIT_SPREAD_TARGET:
            reason = "Spread converged (profit)"

        # Rule 2 — Unhealthy collapse (speed + magnitude)
        # elif (
        #     spread_velocity <= SPREAD_VELOCITY_LIMIT and
        #     current_spread <= entry_spread - EXIT_SPREAD_DROP
        # ):
        #     reason = "Spread collapsing fast"

        # Rule 3 — Funding flip
        elif funding_now <= 0:
            reason = "Funding flipped"

        # Rule 5 — Time-based exit
        elif hold_time >= MAX_HOLD_TIME:
            reason = "Time limit reached"

        # Rule 6 — Volatility spike
        # elif spot_change >= VOLATILITY_EXIT:
        #     reason = "Spot volatility spike"

        else:
            continue

        # ---------------- EXIT EXECUTION ---------------- #

        spot_pnl = (spot_now - entry_spot) * quantity
        futures_pnl = (entry_futures - futures_now) * quantity
        total_pnl = spot_pnl + futures_pnl

        print(f"\n📤 EXIT PAPER TRADE — {reason}")
        print(f"Spot PnL: {spot_pnl:.2f}")
        print(f"Futures PnL: {futures_pnl:.2f}")
        print(f"TOTAL PnL: {total_pnl:.2f}\n")

        return {
            "symbol": symbol,
            "entry_spread": round(entry_spread, 3),
            "exit_spread": round(current_spread, 3),
            # "spread_velocity": round(spread_velocity, 3),
            "hold_minutes": round(hold_time / 60, 2),
            "pnl": round(total_pnl, 2),
            "exit_reason": reason
        }
