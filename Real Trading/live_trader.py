import time
from binance_client import get_client
from symbol_utils import *
from trade_logger import logger

client = get_client()

def enter_live_trade(opportunity):
    symbol = opportunity["symbol"]
    spot_price = opportunity["spot_price"]
    futures_price = opportunity["futures_price"]

    balance = client.get_asset_balance(asset='USDT')
    capital = float(balance['free'])
    CAPITAL = capital * 0.98

    account = client.futures_account()
    available_future_usdt = float(account["availableBalance"])

    print(f"Availabe spot usdt: {capital}")
    print(f"Availabe futures usdt: {available_future_usdt}")

    spot_step = get_step_size(client, symbol)          # spot step
    fut_step  = get_futures_step_size(client, symbol)  # futures step

    raw_qty = CAPITAL / spot_price

    spot_qty = round_qty(raw_qty, spot_step)
    fut_qty  = round_qty(raw_qty, fut_step)

    qty = min(spot_qty, fut_qty)

    if CAPITAL < 10 or available_future_usdt < futures_price * qty:
        if CAPITAL < 10:
            print("Capital too small to trade safely")
            return None
        elif available_future_usdt < futures_price * qty:
            CAPITAL = capital * 90
            raw_qty = CAPITAL / spot_price
            spot_qty = round_qty(raw_qty, spot_step)
            fut_qty  = round_qty(raw_qty, fut_step)
            qty = min(spot_qty, fut_qty)

            if available_future_usdt < futures_price * qty:
                CAPITAL = capital * 80
                raw_qty = CAPITAL / spot_price
                spot_qty = round_qty(raw_qty, spot_step)
                fut_qty  = round_qty(raw_qty, fut_step)
                qty = min(spot_qty, fut_qty)

                if available_future_usdt < futures_price * qty:
                    return None

    print(f"Raw qty: {raw_qty}")
    print(f"Spot qty: {spot_qty}")
    print(f"Futures qty: {fut_qty}")
    print(f"Hedge qty: {qty}")

    if qty <= 0:
        raise Exception("❌ hedge_qty <= 0 — skipping trade")
    
    print(f"\n🚀 ENTER LIVE TRADE {symbol}")
    print(f"Qty: {qty}")

    setup_futures_symbol(client, symbol)

    logger.info(f"ENTER TRADE START | {symbol} | Qty={qty}")

    try:
        # SELL futures
        futures_order = client.futures_create_order(
            symbol=symbol,
            side="SELL",
            type="MARKET",
            quantity=qty
        )

        logger.info(f"FUTURES SELL | {symbol} | Qty={qty} | Price={futures_price}")

        # BUY spot
        spot_order = client.create_order(
            symbol=symbol,
            side="BUY",
            type="MARKET",
            quantity=qty
        )

        spot_price = get_avg_fill_price(spot_order)
        logger.info(f"SPOT BUY | {symbol} | Qty={qty} | Price={spot_price}")

        logger.info(
            f"ENTRY SUMMARY | {symbol} | "
            f"Spot={spot_price} | Futures={futures_price} | "
            f"RawSpread={(futures_price - spot_price) / spot_price * 100:.4f}%"
        )

        print(f"Spot Price: {spot_price} | Futures Price: {futures_price}")
        print("✅ Position opened safely")

        return {
            "symbol": symbol,
            "qty": qty,
            "entry_time": time.time(),
            "entry_spot": spot_price,
            "entry_futures": futures_price,
            "spot_order": spot_order,
            "futures_order": futures_order
        }
    except Exception as e:
        print("⚠️ Entry mismatch detected — emergency hedge")
        raise e