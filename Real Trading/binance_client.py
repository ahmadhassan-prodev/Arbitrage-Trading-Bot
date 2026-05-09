from binance.client import Client
from config import API_KEY, API_SECRET, USE_TESTNET

def get_client():
    client = Client(API_KEY, API_SECRET)

    if USE_TESTNET:
        client.API_URL = "https://testnet.binance.vision/api"
        client.FUTURES_API_URL = "https://testnet.binancefuture.com"

    return client

# client = get_client()
# balance = client.get_asset_balance(asset='USDT')
# capital = float(balance['free'])
# CAPITAL = capital * 0.98

# account = client.futures_account()  # get futures account info
# available_future_usdt = float(account["availableBalance"])

# print(f"Spot:{CAPITAL}")
# print(f"Future:{available_future_usdt}")