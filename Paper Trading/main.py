import time
from scanner import scan_arbitrage
from logger import log_opportunity
from config import SCAN_INTERVAL

def run_scanner():
    print("🚀 Arbitrage scanner started...\n")

    while True:
        try:
            result = scan_arbitrage()

            if result:
                print("✅ Opportunity Found:", result["symbol"],
                      f"Spread={result['spread_pct']}%",
                      f"Net={result['net_spread']}%")

                log_opportunity(result)
            else:
                print("⏳ No opportunity")

        except Exception as e:
            print("❌ Error:", e)

        time.sleep(SCAN_INTERVAL)

if __name__ == "__main__":
    run_scanner()
