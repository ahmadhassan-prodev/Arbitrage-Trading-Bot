def get_live_prices(client, symbol):
    spot = float(client.get_symbol_ticker(symbol=symbol)["price"])
    futures = float(client.futures_symbol_ticker(symbol=symbol)["price"])
    return spot, futures
