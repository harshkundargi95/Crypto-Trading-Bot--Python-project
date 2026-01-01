#!/usr/bin/env python3
import os
import sys
from bot import BasicBot
from tabulate import tabulate

def main():
    # Get API keys
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')
    if not api_key or not api_secret:
        print("Please set BINANCE_API_KEY and BINANCE_API_SECRET environment variables.")
        sys.exit(1)

    bot = BasicBot(api_key, api_secret)

    while True:
        print("\nBinance Futures Order Bot")
        print("1. Market Order")
        print("2. Limit Order")
        print("3. Stop-Limit Order")
        print("4. OCO Order")
        print("5. TWAP Order")
        print("6. Grid Orders")
        print("7. Exit")

        choice = input("Choose an option: ").strip()

        if choice == '1':
            symbol = input("Symbol: ").strip()
            side = input("Side (BUY/SELL): ").strip().upper()
            quantity = input("Quantity: ").strip()
            try:
                order = bot.place_market_order(symbol, side, quantity)
                print("Order placed:")
                print(tabulate(order.items(), headers=['Key', 'Value'], tablefmt='grid'))
            except Exception as e:
                print(f"Error: {e}")

        elif choice == '2':
            symbol = input("Symbol: ").strip()
            side = input("Side (BUY/SELL): ").strip().upper()
            quantity = input("Quantity: ").strip()
            price = input("Price: ").strip()
            try:
                order = bot.place_limit_order(symbol, side, quantity, price)
                print("Order placed:")
                print(tabulate(order.items(), headers=['Key', 'Value'], tablefmt='grid'))
            except Exception as e:
                print(f"Error: {e}")

        elif choice == '3':
            symbol = input("Symbol: ").strip()
            side = input("Side (BUY/SELL): ").strip().upper()
            quantity = input("Quantity: ").strip()
            stop_price = input("Stop Price: ").strip()
            limit_price = input("Limit Price: ").strip()
            try:
                order = bot.place_stop_limit_order(symbol, side, quantity, stop_price, limit_price)
                print("Order placed:")
                print(tabulate(order.items(), headers=['Key', 'Value'], tablefmt='grid'))
            except Exception as e:
                print(f"Error: {e}")

        elif choice == '4':
            symbol = input("Symbol: ").strip()
            side = input("Side (BUY/SELL): ").strip().upper()
            quantity = input("Quantity: ").strip()
            price = input("Take-Profit Price: ").strip()
            stop_price = input("Stop Price: ").strip()
            stop_limit_price = input("Stop Limit Price: ").strip()
            try:
                order = bot.place_oco_order(symbol, side, quantity, price, stop_price, stop_limit_price)
                print("Order placed:")
                print(tabulate(order.items(), headers=['Key', 'Value'], tablefmt='grid'))
            except Exception as e:
                print(f"Error: {e}")

        elif choice == '5':
            symbol = input("Symbol: ").strip()
            side = input("Side (BUY/SELL): ").strip().upper()
            total_quantity = input("Total Quantity: ").strip()
            duration_minutes = int(input("Duration (minutes): ").strip())
            intervals = int(input("Intervals: ").strip())
            try:
                orders = bot.place_twap_order(symbol, side, total_quantity, duration_minutes, intervals)
                print("Orders placed:", len(orders))
            except Exception as e:
                print(f"Error: {e}")

        elif choice == '6':
            symbol = input("Symbol: ").strip()
            base_price = input("Base Price: ").strip()
            range_percent = input("Range Percent: ").strip()
            num_orders = int(input("Number of Orders per Side: ").strip())
            quantity_per_order = input("Quantity per Order: ").strip()
            try:
                orders = bot.place_grid_orders(symbol, base_price, range_percent, num_orders, quantity_per_order)
                print("Orders placed:", len(orders))
            except Exception as e:
                print(f"Error: {e}")

        elif choice == '7':
            break

        else:
            print("Invalid choice.")

if __name__ == '__main__':
    main()