# Binance Futures Order Bot

This project is a CLI-based trading bot for Binance USDT-M Futures, developed as part of a hiring process assignment. It supports placing market and limit orders on the Binance Testnet, with optional advanced order types like Stop-Limit, OCO, TWAP, and Grid. The bot includes robust input validation, comprehensive logging, and error handling, using the python-binance library for API interactions.

## 🚀 Features

- **Core Orders**: Market and Limit orders
- **Advanced Orders**: Stop-Limit, OCO (One-Cancels-Other), TWAP (Time-Weighted Average Price), Grid orders
- **Interactive CLI Menu**: User-friendly interface for placing orders
- **Comprehensive Validation**: Input checking for symbols, quantities, and prices
- **Structured Logging**: All actions logged to `bot.log` with timestamps
- **Error Handling**: Detailed error messages and exception handling
- **Testnet Support**: Safe testing environment (no real money)
- **Modular Design**: Easy to extend and maintain

## 📋 Prerequisites

- Python 3.7+
- Binance Testnet account
- API credentials from Binance

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/binance-bot.git
cd binance-bot
```

### 2. Set Up Python Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

#### Install python-binance (if not in requirements.txt)
In the same PowerShell window, run:
```powershell
pip install python-binance
```

If that doesn't work, try:
```powershell
python -m pip install python-binance
```

### 3. Get Binance Testnet API Keys

1. Go to https://testnet.binance.vision/
2. Authenticate with GitHub
3. Create API keys in the dashboard
4. Enable Futures trading permissions

### 4. Set Environment Variables

**Windows (PowerShell):**
```powershell
$env:BINANCE_API_KEY = "your_testnet_api_key_here"
$env:BINANCE_API_SECRET = "your_testnet_api_secret_here"
```

**macOS/Linux:**
```bash
export BINANCE_API_KEY="your_testnet_api_key_here"
export BINANCE_API_SECRET="your_testnet_api_secret_here"
```

**Important**: Never commit real API keys to version control!

## 🚀 Running the Bot

After setting up the environment and API keys, you can run the bot using the following commands. The bot requires API keys to be set as environment variables.

### Windows PowerShell Setup
1. Activate the virtual environment:
   ```powershell
   & "C:/Users/your-username/path-to-project/.venv/Scripts/Activate.ps1"
   ```
   (Replace `your-username` and `path-to-project` with your actual paths.)

2. Set the Binance Testnet API environment variables:
   ```powershell
   $env:BINANCE_API_KEY = "your_testnet_api_key_here"
   $env:BINANCE_API_SECRET = "your_testnet_api_secret_here"
   ```
   (Replace with your actual testnet keys from https://testnet.binance.vision/)

3. Run the bot in interactive mode:
   ```powershell
   python .\src\main.py
   ```

### Interactive Mode (Recommended for beginners)
```bash
python src/main.py
```

This launches an interactive menu where you can select order types and enter parameters.

### Direct Commands (for automation or scripting)
```bash
# Market Order
python src/market_orders.py <SYMBOL> <SIDE> <QUANTITY>

# Limit Order
python src/limit_orders.py <SYMBOL> <SIDE> <QUANTITY> <PRICE>

# Stop-Limit Order
python src/stop_limit_orders.py <SYMBOL> <SIDE> <QUANTITY> <STOP_PRICE> <LIMIT_PRICE>

# OCO Order
python src/advanced/oco.py <SYMBOL> <SIDE> <QUANTITY> <TP_PRICE> <SL_PRICE> <SL_LIMIT_PRICE>

# TWAP Order
python src/advanced/twap.py <SYMBOL> <SIDE> <QUANTITY> <INTERVAL_MINUTES> <NUM_ORDERS>

# Grid Order
python src/advanced/grid_orders.py <SYMBOL> <GRID_SPREAD> <NUM_LEVELS> <LEVEL_SPACING> <QUANTITY_PER_LEVEL>
```

Replace the placeholders with actual values (e.g., `BTCUSDT`, `BUY`, `0.01`, etc.).

## 🎯 Usage

All commands use Binance Futures Testnet by default.

### Interactive Menu (Recommended)
```bash
python src/main.py
```
Choose from the menu options to place orders interactively.

### Direct CLI Commands

#### Market Orders
```bash
python src/market_orders.py BTCUSDT BUY 0.01
```

#### Limit Orders
```bash
python src/limit_orders.py BTCUSDT SELL 0.01 50000
```

#### Stop-Limit Orders
```bash
python src/stop_limit_orders.py BTCUSDT BUY 0.01 49000 49500
```

#### OCO Orders (Take Profit + Stop Loss)
```bash
python src/advanced/oco.py BTCUSDT SELL 0.01 51000 48500 48000
```

#### TWAP Orders (Spread over time)
```bash
python src/advanced/twap.py BTCUSDT BUY 0.1 10 5
```

#### Grid Orders (Automated range trading)
```bash
python src/advanced/grid_orders.py BTCUSDT 50000 5 3 0.01
```

## 📊 Order Types Explained

- **Market Order**: Buy/sell immediately at current market price
- **Limit Order**: Buy/sell only at specified price or better
- **Stop-Limit Order**: Trigger a limit order when stop price is hit
- **OCO Order**: Place take-profit and stop-loss simultaneously
- **TWAP Order**: Split large orders into smaller chunks over time
- **Grid Order**: Automated buy-low/sell-high within a price range

## 📝 Logging

All bot activities are logged to `bot.log` in the project root:
- Order placements
- API responses
- Errors and exceptions
- Timestamps for all actions

View logs:
```bash
tail -f bot.log  # Linux/macOS
Get-Content bot.log -Wait  # Windows
```

## 🔒 Security Notes

- This bot uses **Binance Testnet** - no real funds at risk
- API keys are stored as environment variables (not in code)
- Never share your API keys
- Test all strategies on testnet before live trading
- The bot includes rate limiting and error handling

## 🏗️ Project Structure

```
binance-bot/
│
├── src/
│   ├── bot.py              # Core bot logic and order methods
│   ├── main.py             # Interactive CLI menu
│   ├── market_orders.py    # Market order CLI
│   ├── limit_orders.py     # Limit order CLI
│   ├── stop_limit_orders.py # Stop-limit order CLI
│   └── advanced/
│       ├── oco.py          # OCO orders
│       ├── twap.py         # TWAP strategy
│       └── grid_orders.py  # Grid trading
│
├── bot.log                 # Activity logs
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🧪 Testing

1. Use very small quantities (0.001 BTC) for testing
2. Check your testnet balance before and after orders
3. Monitor the testnet dashboard for order execution
4. Review logs for any issues

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is for educational purposes. Use at your own risk.

## ⚠️ Disclaimer

This is a learning project for algorithmic trading concepts. Not financial advice. Always test strategies thoroughly and never risk more than you can afford to lose.

## 🏃‍♂️ Quick Start

1. Set up testnet account and API keys
2. Clone repo and install dependencies
3. Set environment variables
4. Run: `python src/main.py`
5. Choose an order type and start trading!

---

**API Keys Used**: This project uses Binance Futures Testnet API keys. You must obtain your own keys from https://testnet.binance.vision/ and set them as environment variables as described above. Never commit real API keys to the repository.