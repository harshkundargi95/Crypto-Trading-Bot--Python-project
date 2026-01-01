#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from bot import BasicBot
import argparse

def main():
    parser = argparse.ArgumentParser(description='Place a TWAP order on Binance Futures Testnet.')
    parser.add_argument('symbol', help='Trading symbol, e.g., BTCUSDT')
    parser.add_argument('side', choices=['BUY', 'SELL'], help='Order side')
    parser.add_argument('total_quantity', help='Total order quantity')
    parser.add_argument('duration_minutes', type=int, help='Duration in minutes')
    parser.add_argument('intervals', type=int, help='Number of intervals')

    args = parser.parse_args()

    # Get API keys from environment variables
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')
    if not api_key or not api_secret:
        print("Please set BINANCE_API_KEY and BINANCE_API_SECRET environment variables.")
        sys.exit(1)

    bot = BasicBot(api_key, api_secret)

    try:
        orders = bot.place_twap_order(args.symbol, args.side, args.total_quantity, args.duration_minutes, args.intervals)
        print("TWAP orders placed successfully:")
        for i, order in enumerate(orders):
            print(f"Order {i+1}: {order}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()