#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from bot import BasicBot
import argparse

def main():
    parser = argparse.ArgumentParser(description='Place grid orders on Binance Futures Testnet.')
    parser.add_argument('symbol', help='Trading symbol, e.g., BTCUSDT')
    parser.add_argument('base_price', help='Base price for grid')
    parser.add_argument('range_percent', help='Range percentage')
    parser.add_argument('num_orders', type=int, help='Number of orders per side')
    parser.add_argument('quantity_per_order', help='Quantity per order')

    args = parser.parse_args()

    # Get API keys from environment variables
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')
    if not api_key or not api_secret:
        print("Please set BINANCE_API_KEY and BINANCE_API_SECRET environment variables.")
        sys.exit(1)

    bot = BasicBot(api_key, api_secret)

    try:
        orders = bot.place_grid_orders(args.symbol, args.base_price, args.range_percent, args.num_orders, args.quantity_per_order)
        print("Grid orders placed successfully:")
        for i, order in enumerate(orders):
            print(f"Order {i+1}: {order}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()