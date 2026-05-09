SPOT_FEE = 0.10      # %
FUTURES_FEE = 0.04   # %
EXIT_FEES = 0.14    # %
SLIPPAGE = 0.08     # %

MIN_RAW_SPREAD = 1     # %
MIN_NET_SPREAD = 1.1    # %
MIN_VOLUME = 20_000_000 # USDT
MIN_FUNDING = 0.0
MIN_FUNDING_TIME = 15 * 60  # seconds

SPOT_TICKER = "https://api.binance.com/api/v3/ticker/24hr"
FUTURES_TICKER = "https://fapi.binance.com/fapi/v1/ticker/24hr"
FUNDING_RATE = "https://fapi.binance.com/fapi/v1/premiumIndex"

import requests
import time

def get_json(url, retries=3, timeout=10):
    for attempt in range(1, retries + 1):
        try:
            r = requests.get(url, timeout=timeout)
            r.raise_for_status()
            return r.json()

        except requests.exceptions.ReadTimeout:
            print(f"⚠️ Timeout ({attempt}/{retries}) → {url}")

        except requests.exceptions.RequestException as e:
            print(f"⚠️ Request error ({attempt}/{retries}): {e}")
        
        time.sleep(2)

    print("❌ Failed after retries, skipping this cycle")
    return None

def scan_arbitrage():

    spot_data = get_json(SPOT_TICKER)
    futures_data = get_json(FUTURES_TICKER)
    funding_data = get_json(FUNDING_RATE)

    if not spot_data or not futures_data or not funding_data:
        return None

    # Map spot prices & volume
    spot_map = {
        s["symbol"]: {
            "price": float(s["lastPrice"]),
            "volume": float(s["quoteVolume"])
        }
        for s in spot_data
        if s["symbol"].endswith("USDT")
    }

    # Map funding info
    funding_map = {
        f["symbol"]: {
            "fundingRate": float(f["lastFundingRate"]) * 100,
            "nextFundingTime": int(f["nextFundingTime"]) / 1000
        }
        for f in funding_data
    }

    candidates = []

    for f in futures_data:
        symbol = f["symbol"]

        if symbol not in spot_map:
            continue

        # Prices
        spot_price = spot_map[symbol]["price"]
        futures_price = float(f["lastPrice"])
        volume = spot_map[symbol]["volume"]

        # Spread calculation
        spread_pct = (futures_price - spot_price) / spot_price * 100

        if spread_pct < MIN_RAW_SPREAD:
            continue

        # Liquidity filter
        if volume < MIN_VOLUME:
            continue

        # Funding filter
        funding = funding_map.get(symbol)
        if not funding:
            continue

        funding_rate = funding["fundingRate"]
        time_to_funding = funding["nextFundingTime"] - time.time()

        if funding_rate <= MIN_FUNDING:
            continue

        if time_to_funding < MIN_FUNDING_TIME:
            continue

        # Net spread
        net_spread = (
            spread_pct
            - SPOT_FEE
            - FUTURES_FEE
            - EXIT_FEES
            - SLIPPAGE
        )

        if net_spread < MIN_NET_SPREAD:
            continue

        candidates.append({
            "symbol": symbol,
            "spot_price": spot_price,
            "futures_price": futures_price,
            "spread_pct": round(spread_pct, 3),
            "funding_rate": funding_rate,
            "net_spread": round(net_spread, 3),
            "volume": volume
        })

    if not candidates:
        return None

    # Rank best candidate
    candidates.sort(
        key=lambda x: (x["net_spread"], x["volume"]),
        reverse=True
    )

    return candidates[0]

if __name__ == "__main__":
    result = scan_arbitrage()

    if result:
        print("✅ Arbitrage Opportunity Found:")
        for k, v in result.items():
            print(f"{k}: {v}")
    else:
        print("❌ No safe arbitrage opportunity right now")
