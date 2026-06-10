# Arbitrage Trading Bot

**A real-time cryptocurrency basis arbitrage bot exploiting price discrepancies between Binance Spot and Futures markets (USDT pairs).**

This repository implements an automated trading system that scans for positive funding rate + spread opportunities, executes hedged trades (long spot / short futures), and manages exits for profit.

---

## Overview

This project is a **professional-grade arbitrage trading bot** focused on **cash-and-carry / basis arbitrage** on Binance. It continuously monitors thousands of USDT perpetual futures contracts versus their spot counterparts, identifies high-conviction opportunities based on spread, volume, liquidity, and funding rates, and executes live or paper trades.

The bot includes separate implementations for **Paper Trading** (simulation) and **Real Trading** (live execution).

## Repository Purpose

- Automate profitable basis arbitrage strategies between Spot and Futures markets
- Demonstrate robust scanner logic with multiple risk filters
- Provide production-ready trade execution with proper error handling and logging
- Serve as both a functional trading tool and an advanced example of crypto trading systems

## Key Features

- **Real-time Arbitrage Scanner** using public Binance APIs
- **Multi-filter Opportunity Detection**:
  - Minimum raw spread
  - Net spread after fees & slippage
  - High volume/liquidity requirements
  - Positive funding rate + time-to-funding filter
- **Hedged Trading**:
  - Buy Spot + Sell Futures (or reverse)
  - Precise quantity calculation with step size handling
  - Dynamic position sizing based on available balance
- **Live Monitoring & Exit Logic**:
  - Spread convergence exit
  - Time-based exit
  - Funding rate flip protection
- **Paper Trading Mode** for safe strategy testing
- **Comprehensive Logging** and error resilience

## Technologies Used

- **Python 3**
- **python-binance** (official Binance API client)
- **Requests** (for public ticker endpoints)
- Modular architecture with clear separation of concerns

## Project Structure

```bash
Arbitrage-Trading-Bot/
├── README.md
│
├── Paper Trading/                  # Simulation environment
│   ├── paper_trader.py            # Main paper trading logic
│   ├── scanner.py                 # Scanner with relaxed thresholds
│   ├── config.py
│   └── logger.py
│
├── Real Trading/                   # Live execution environment
│   ├── main_live.py               # Main trading loop
│   ├── live_trader.py             # Entry logic (hedged orders)
│   ├── live_exit.py               # Exit logic
│   ├── live_monitor.py            # Price monitoring
│   ├── scanner.py                 # Production scanner
│   ├── binance_client.py          # Client configuration
│   ├── config.py                  # Trading parameters
│   ├── symbol_utils.py            # Quantity & step size helpers
│   └── trade_logger.py            # Logging utilities
│
└── screenshots/                    # Performance examples
```

**How the Code Works**

- **Scanning Phase**: Fetches 24h tickers for Spot & Futures + funding rates.
- **Opportunity Detection**: Filters symbols meeting strict criteria (spread, volume, funding).
- **Entry**: Places simultaneous market orders - BUY on Spot + SELL on Futures.
- **Monitoring**: Continuously checks current spread and hold time.
- **Exit**: Closes positions when spread converges, funding flips, or time limit is reached.
- **Loop**: Repeats scanning for new opportunities.

The system is designed to be resilient with retry logic, balance checks, and error handling.

**Installation**

- Clone the repository:

Bash

git clone &lt;repository-url&gt;

cd Arbitrage-Trading-Bot

- Install dependencies:

Bash

pip install python-binance requests

- Configure API keys in Real Trading/config.py (and optionally Paper Trading/config.py).

**Usage**

**Paper Trading (Recommended for testing)**

Bash

cd "Paper Trading"

python paper_trader.py

**Live Trading**

Bash

cd "Real Trading"

python main_live.py

**Important**:

- Update API_KEY and API_SECRET in config.py
- Start with USE_TESTNET = True and small capital
- Monitor console output for real-time status

**Learning Outcomes**

Studying this codebase will help you understand:

- Basis arbitrage strategies in cryptocurrency markets
- Working with Binance Spot and Futures APIs simultaneously
- Building robust, production-ready trading scanners
- Risk management through multi-layer filtering
- Hedged position management and precise order execution
- Modular Python architecture for trading systems

**Notes & Disclaimer**

- **High Risk**: Live trading can result in significant financial loss.
- Always start on **Testnet** and use minimal capital.
- The bot is optimized for **USDT-margined perpetuals**.
- Market conditions, fees, and slippage can affect profitability.
- This project is for educational and experimental purposes.
