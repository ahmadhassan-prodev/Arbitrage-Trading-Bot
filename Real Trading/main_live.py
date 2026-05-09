import time
from scanner import scan_arbitrage
from live_trader import enter_live_trade
from live_monitor import get_live_prices
from live_exit import exit_live_trade
from binance_client import get_client
from config import *
from symbol_utils import is_safe_symbol

client = get_client()
trade = None

print("🔥 LIVE TRADING MODE STARTED\n")

while True:
    try:
        opportunity = scan_arbitrage()

        if opportunity:
            print("✅ Opportunity Found:",
                    opportunity["symbol"],
                    f"Spread={opportunity['spread_pct']:.3f}%",
                    f"Net={opportunity['net_spread']:.3f}%")
            print(f"Spot price={opportunity["spot_price"]} | Future price={opportunity["futures_price"]}")
            
        else:
            time.sleep(SCAN_INTERVAL)
            continue

        symbol = opportunity["symbol"]
        
        if not is_safe_symbol(client, symbol):
            print(f"⚠️ Skipping unsafe symbol: {symbol}")
            time.sleep(SCAN_INTERVAL)
            continue

        trade = enter_live_trade(opportunity)

    except Exception as e:
        print("🔥 CRITICAL ERROR:", e)
        time.sleep(5)
        continue

    if trade:
        while True:
            try:
                time.sleep(PRICE_CHECK_INTERVAL)

                spot, futures = get_live_prices(client, trade["symbol"])
                spread = (futures - spot) / spot * 100
                hold_time = time.time() - trade["entry_time"]

                print(f"Spread={spread:.3f}% | Hold={int(hold_time/60)}m")

                if spread <= EXIT_SPREAD_TARGET or hold_time >= MAX_HOLD_TIME:
                    exit_live_trade(client, trade, futures)
                    trade = None
                    break

            except Exception as e:
                print("🔥 CRITICAL ERROR:", e)
                time.sleep(5)
