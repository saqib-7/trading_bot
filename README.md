# Binance Futures Trading Bot

A fast, CLI-based trading bot for the Binance Futures Testnet, built with Python. 

This project uses FastAPI under the hood to structure the order placement logic cleanly, while providing a fully interactive Typer CLI to execute trades directly from your terminal.

## Core Features
- **Binance Futures Testnet**: Safely practice trading on the testnet via Signed REST requests (`https://testnet.binancefuture.com`).
- **Interactive CLI**: Place trades instantly using an interactive prompt that guides you through the `MARKET` or `LIMIT` parameters.
- **Auto Environment Loading**: Plugs right into your `.env` file to load Binance credentials securely.
- **Robust Logging**: Every API request and response is automatically logged to `logs/trading_bot.log` for easy auditing.

## Project Structure
```text
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py         # Binance custom REST wrapper
│   ├── orders.py         # FastAPI instance & routes
│   ├── validators.py     # Pydantic input models
│   └── logging_config.py # Logger setup
├── cli.py                # The main CLI entry point
├── Dockerfile
├── requirements.txt
└── .env                  # Your target credentials file
```

## Setup & Running Locally

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Set up your Credentials**
Create a `.env` file in the root directory (next to `cli.py`) and add your Binance Testnet keys:
```text
BINANCE_API_KEY="your_testnet_api_key"
BINANCE_API_SECRET="your_testnet_secret"
```
*(The bot also supports `BINANCE_SECRET_KEY` if you prefer that naming convention)*

3. **Placing an Order**
The easiest way to place an order is to launch the interactive prompt:
```bash
python cli.py order
```
It will ask you step-by-step for the Trading Pair, Side, Order Type, and Quantity.

Alternatively, you can pass arguments directly to skip the prompts:
```bash
# Place a 0.001 BTC Market Buy
python cli.py order --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.001

# Place a 0.01 ETH Limit Sell (requires price)
python cli.py order --symbol ETHUSDT --side SELL --order-type LIMIT --quantity 0.01 --price 2500.50
```

## Docker Execution

You can run the bot without installing Python locally by building the Docker container. 

```bash
# Build the image
docker build -t binance-bot .

# Run the CLI container interactively (-it flag is required for prompts)
docker run -it --env-file .env --rm binance-bot order
```
