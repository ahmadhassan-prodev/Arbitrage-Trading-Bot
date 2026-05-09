from symbol_utils import *
from trade_logger import logger

def exit_live_trade(client, trade, future_price):
    symbol = trade["symbol"]
    spot_price = None
    futures_price = future_price

    print(f"\n📤 EXIT LIVE TRADE {symbol}")
    logger.info(f"EXIT TRADE START | {symbol}")

    # STEP SIZES (VERY IMPORTANT)
    spot_step = get_step_size(client, symbol)
    futures_step = get_futures_step_size(client, symbol)

    # ---------- SPOT EXIT ----------
    spot_qty_raw = get_spot_available_qty(client, symbol)
    spot_qty = round_qty(spot_qty_raw, spot_step)

    if spot_qty >= spot_step:
        spot_order = client.create_order(
            symbol=symbol,
            side="SELL",
            type="MARKET",
            quantity=spot_qty
        )
        print(f"✅ Spot closed: {spot_qty}")

        spot_price = get_avg_fill_price(spot_order)
        logger.info(
            f"SPOT SELL | {symbol} | Qty={spot_qty} | Price={spot_price}"
        )
    else:
        print("ℹ️ No spot position to close")
        logger.info(f"SPOT SELL | {symbol} | No balance")

    # ---------- FUTURES EXIT ----------
    pos_amt = get_futures_position_qty(client, symbol)

    if abs(pos_amt) < futures_step:
        print("ℹ️ Futures position too small to close")
        logger.info(f"FUTURES CLOSE | {symbol} | Dust position")
        pos_amt = 0

    if pos_amt != 0:
        fut_qty = round_qty(abs(pos_amt), futures_step)
        side = "BUY" if pos_amt < 0 else "SELL"

        futures_order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=fut_qty,
            reduceOnly=True
        )
        print(f"✅ Futures closed: {fut_qty}")

        logger.info(
            f"FUTURES CLOSE | {symbol} | Qty={fut_qty} | Price={futures_price}"
        )
    else:
        print("ℹ️ No futures position to close")
        logger.info(f"FUTURES CLOSE | {symbol} | No position")

    # ---------- FINAL LOG ----------
    logger.info(
        f"TRADE COMPLETE | {symbol} | "
        f"SpotEntry={trade.get('spot_entry')} | "
        f"FuturesEntry={trade.get('futures_entry')} | "
        f"SpotExit={spot_price} | "
        f"FuturesExit={futures_price if pos_amt != 0 else None}"
    )

    print(f"Spot Price: {spot_price} | Futures Price: {futures_price}")
