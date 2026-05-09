import time
from scanner import scan_arbitrage
from paper_trader import paper_trade
from logger import log_opportunity, log_trade_result
from config import SCAN_INTERVAL
import sys

sys.stdout.reconfigure(encoding='utf-8')

def run_paper_trader():
    print("🧪 PAPER TRADING MODE STARTED\n")

    while True:
        try:
            # ------------------ SCAN ------------------ #
            opportunity = scan_arbitrage()

            if opportunity:
                # Opportunity found — display and log
                print("✅ Opportunity Found:",
                      opportunity["symbol"],
                      f"Spread={opportunity['spread_pct']:.3f}%",
                      f"Net={opportunity['net_spread']:.3f}%")

                # Log the opportunity (scanner-style)
                log_opportunity(opportunity)

                # ------------------ PAPER TRADE ------------------ #
                trade_result = paper_trade(opportunity)

                # ------------------ LOG TRADE EXIT ------------------ #
                log_trade_result(trade_result)

                # Print trade result
                print("📊 PAPER TRADE RESULT:", trade_result)
                print("\n🔁 Waiting for next opportunity...\n")
                time.sleep(SCAN_INTERVAL)

            else:
                # No opportunity
                # print("⏳ No opportunity")
                time.sleep(SCAN_INTERVAL)

        except Exception as e:
            print("❌ Error:", e)
            time.sleep(10)


if __name__ == "__main__":
    run_paper_trader()
