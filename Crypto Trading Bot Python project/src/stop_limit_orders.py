#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(__file__))

from bot import BasicBot
import argparse
from tabulate import tabulate

def main():
    parser = argparse.ArgumentParser(description='Place a stop-limit order on Binance Futures Testnet.')
    parser.add_argument('symbol', help='Trading symbol, e.g., BTCUSDT')
    parser.add_argument('side', choices=['BUY', 'SELL'], help='Order side')
    parser.add_argument('quantity', help='Order quantity')
    parser.add_argument('stop_price', help='Stop price')
    parser.add_argument('limit_price', help='Limit price')

    args = parser.parse_args()

    # Get API keys from environment variables
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')
    if not api_key or not api_secret:
        print("Please set BINANCE_API_KEY and BINANCE_API_SECRET environment variables.")
        sys.exit(1)

    bot = BasicBot(api_key, api_secret)

    try:
        order = bot.place_stop_limit_order(args.symbol, args.side, args.quantity, args.stop_price, args.limit_price)
        print("Stop-Limit order placed successfully:")
        print(tabulate(order.items(), headers=['Key', 'Value'], tablefmt='grid'))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()