
# 🚀 Crypto Pilot - Your Beginner Crypto Trading Bot

![Crypto Pilot Banner](./crypto-pilot.png) 


*Your personal co-pilot for learning crypto trading strategies and backtesting in Python.*

---

## 🌟 Overview

Crypto Pilot is a **beginner-friendly Python crypto trading bot**. It helps you learn **algorithmic trading** without risking real money.

Key concepts you’ll explore:

- Trend-following strategies (EMA-based) 
- Indicators: EMA, RSI, MACD 
- Volatility-aware risk management with ATR 
- Simulated trades (Paper Trading) with leverage 
- Telegram alerts & CSV logging 

Think of it as a **crypto flight simulator**, test strategies, watch trades, and learn trading mechanics safely. ✈️💸

---

## ⚡ Features

### 🧠 Trading Strategy
- Follows **macro trend (200 EMA)** for direction 
- Uses **8 vs 21 EMA crossovers** for momentum signals 
- Filters trades with **RSI & MACD** to avoid bad entries 
- Generates **buy/sell signals** automatically 

### 🛡️ Risk Management & Position Sizing
- Uses **ATR** to measure market volatility 
- Calculates **position size** based on risk %, leverage, and margin 
- Supports **dynamic SL & TP** 

### 💹 Paper Trading with PaperBroker
- Simulates **margin, leverage, and fees** 
- Checks SL/TP **intra-candle** for realistic exits 
- Tracks **equity curve**, win rate, max drawdown & total return 

### 🔔 Alerts & Logging
- Sends **Telegram alerts** for entries, exits, SL/TP hits 
- Logs trades in **CSV** for offline review 

### 📊 Backtester
- Run **strategy simulations** on historical data 
- Evaluate **performance metrics** (returns, drawdown, Sharpe) 
- Test symbols, timeframes & parameters safely 

---

## 🏗️ How It Works (Beginner Analogy)

Imagine Crypto Pilot as your **flight co-pilot**:

| Trading Component | Flight Analogy | Meaning |
|------------------|----------------|----------|
| 200 EMA | Navigation Compass | Shows overall market direction |
| 8 & 21 EMA Cross | Speed & Tilt Meters | Detect momentum shifts |
| RSI & MACD | Warning Lights | Avoid risky/overheated markets |
| ATR | Safety Buffer | Adjusts stop-loss distance |
| PaperBroker | Flight Simulator | Practice without real loss |

---

## 💻 Installation & Setup

### ✅ Requirements
- Python ≥ 3.10 
- `pip` package manager 

### 1️. Clone the repo
1. Open your terminal or command prompt 
2. Run:

git clone https://github.com/YourUsername/crypto-pilot.git
cd crypto-pilot
3. Run pip install -r requirements.txt in the project folder to install dependencies

### 🧰 Beginner Setup Guide (Integrated Instructions)
## Telegram Alerts Setup

## Create a Telegram Bot

1. Open Telegram and search for BotFather

2. Start the chat and send /newbot

3. Name your bot (e.g., CryptoPilot Alerts)

4. Copy the Bot Token provided

## Get Your Chat ID

6. Search for **@userinfobot** in Telegram

7. Start the bot and note your Chat ID

## Configure the Bot

8. Open the .env file in the project folder

9. Add your credentials:
- TELEGRAM_BOT_TOKEN=your_token_here
- TELEGRAM_CHAT_ID=123456789

## Switching Exchanges

### Crypto Pilot supports multiple exchanges via ccxt. You can select the exchange in the configuration file.

Exchange Notes
- Bybit Beginner-friendly, testnet available
- Binance Popular, requires API keys and permissions
- OKX Advanced, strict API rules

## To change exchange, update the code:
- exchange = ccxt.binance()

## API Keys for Live Trading (Optional)

1. Create API keys on your chosen exchange (testnet recommended first)

2. Enable Read + Trade permissions

3. Add them to .env:
- API_KEY=your_api_key
- API_SECRET=your_secret_key
- TESTNET=true

## Recommended Beginner Workflow

1. Start with Paper Trading to learn risk-free

2. Enable Telegram Alerts to track trades and review results

3. Try Testnet Trading with small leverage

4. Only use a real account after consistent success

**⚠️ Remember:** Crypto Pilot is for learning and experimentation. Always prioritize safety over profit when starting out.

## 📫 Let’s Collaborate & Learn Together

Crypto Pilot is all about **learning and experimenting** with crypto trading. Your ideas and contributions can make it even better! 

- **Collaborate:** Want to add a new indicator, support another exchange, or improve the code? Jump in! 
- **Learn & Share:** Got tips, insights, or suggestions? Sharing helps everyone, including you grow. 
- **Reach Out:** Send me a message at [aminhydarali@gmail.com](mailto:amin@) anytime. I’d love to hear from you! 

> 🌟 **Remember:** Every little contribution counts, whether it’s a bug fix, a new feature, or just feedback. Let’s build and learn together!

MIT License © Amin Hydar Ali
