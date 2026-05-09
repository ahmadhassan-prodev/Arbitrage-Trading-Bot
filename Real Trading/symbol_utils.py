def get_step_size(client, symbol):
    info = client.get_exchange_info()

    for s in info["symbols"]:
        if s["symbol"] == symbol:
            for f in s["filters"]:
                if f["filterType"] == "LOT_SIZE":
                    return float(f["stepSize"])
    return None


def round_qty(qty, step_size):
    return round(qty - (qty % step_size), 8)

def setup_futures_symbol(client, symbol):
    try:
        client.futures_change_margin_type(
            symbol=symbol,
            marginType="ISOLATED"
        )
    except:
        pass

    client.futures_change_leverage(
        symbol=symbol,
        leverage=1
    )

def is_safe_symbol(client, symbol):
    # 1. Must be ASCII (no weird characters)
    if not symbol.isascii():
        return False

    # 2. Must end with USDT
    if not symbol.endswith("USDT"):
        return False

    # 3. Must exist on Futures exchange
    futures_info = client.futures_exchange_info()
    futures_symbols = {s["symbol"] for s in futures_info["symbols"]}

    return symbol in futures_symbols

def get_spot_available_qty(client, symbol):
    base_asset = symbol.replace("USDT", "")
    balance = client.get_asset_balance(asset=base_asset)
    return float(balance["free"])

def get_futures_position_qty(client, symbol):
    positions = client.futures_position_information()

    for p in positions:
        if p["symbol"] == symbol:
            amt = float(p["positionAmt"])
            if abs(amt) > 1e-8:
                return amt

    return 0.0


def get_avg_fill_price(order):
    """
    Binance returns multiple fills.
    We calculate weighted average execution price.
    """
    if "fills" not in order:
        return None

    total_qty = 0.0
    total_cost = 0.0

    for f in order["fills"]:
        price = float(f["price"])
        qty = float(f["qty"])
        total_qty += qty
        total_cost += price * qty

    return round(total_cost / total_qty, 8) if total_qty > 0 else None

def get_futures_step_size(client, symbol):
    info = client.futures_exchange_info()
    for s in info["symbols"]:
        if s["symbol"] == symbol:
            for f in s["filters"]:
                if f["filterType"] == "LOT_SIZE":
                    return float(f["stepSize"])
    return None
