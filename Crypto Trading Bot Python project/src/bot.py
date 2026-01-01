import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
import os

# Set up logging
logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.client = Client(api_key, api_secret, testnet=testnet)
        self.testnet = testnet
        logging.info("Bot initialized with testnet=%s", testnet)

    def validate_symbol(self, symbol):
        # Simple validation: check if symbol is a string and ends with USDT
        if not isinstance(symbol, str) or not symbol.endswith('USDT'):
            raise ValueError("Invalid symbol. Must be a string ending with USDT.")
        return symbol.upper()

    def validate_quantity(self, quantity):
        try:
            qty = float(quantity)
            if qty <= 0:
                raise ValueError("Quantity must be positive.")
            return qty
        except ValueError:
            raise ValueError("Invalid quantity. Must be a number.")

    def validate_price(self, price):
        try:
            pr = float(price)
            if pr <= 0:
                raise ValueError("Price must be positive.")
            return pr
        except ValueError:
            raise ValueError("Invalid price. Must be a number.")

    def place_market_order(self, symbol, side, quantity):
        symbol = self.validate_symbol(symbol)
        quantity = self.validate_quantity(quantity)
        side = side.upper()
        if side not in ['BUY', 'SELL']:
            raise ValueError("Side must be BUY or SELL.")

        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='MARKET',
                quantity=quantity
            )
            logging.info("Market order placed: %s", order)
            return order
        except (BinanceAPIException, BinanceRequestException) as e:
            logging.error("Error placing market order: %s", str(e))
            raise

    def place_limit_order(self, symbol, side, quantity, price):
        symbol = self.validate_symbol(symbol)
        quantity = self.validate_quantity(quantity)
        price = self.validate_price(price)
        side = side.upper()
        if side not in ['BUY', 'SELL']:
            raise ValueError("Side must be BUY or SELL.")

        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='LIMIT',
                quantity=quantity,
                price=price,
                timeInForce='GTC'
            )
            logging.info("Limit order placed: %s", order)
            return order
        except (BinanceAPIException, BinanceRequestException) as e:
            logging.error("Error placing limit order: %s", str(e))
            raise

    def place_stop_limit_order(self, symbol, side, quantity, stop_price, limit_price):
        symbol = self.validate_symbol(symbol)
        quantity = self.validate_quantity(quantity)
        stop_price = self.validate_price(stop_price)
        limit_price = self.validate_price(limit_price)
        side = side.upper()
        if side not in ['BUY', 'SELL']:
            raise ValueError("Side must be BUY or SELL.")

        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='STOP_LOSS_LIMIT',
                quantity=quantity,
                stopPrice=stop_price,
                price=limit_price,
                timeInForce='GTC'
            )
            logging.info("Stop-Limit order placed: %s", order)
            return order
        except (BinanceAPIException, BinanceRequestException) as e:
            logging.error("Error placing stop-limit order: %s", str(e))
            raise

    def place_oco_order(self, symbol, side, quantity, price, stop_price, stop_limit_price):
        symbol = self.validate_symbol(symbol)
        quantity = self.validate_quantity(quantity)
        price = self.validate_price(price)
        stop_price = self.validate_price(stop_price)
        stop_limit_price = self.validate_price(stop_limit_price)
        side = side.upper()
        if side not in ['BUY', 'SELL']:
            raise ValueError("Side must be BUY or SELL.")

        try:
            order = self.client.futures_create_oco_order(
                symbol=symbol,
                side=side,
                quantity=quantity,
                price=price,
                stopPrice=stop_price,
                stopLimitPrice=stop_limit_price,
                stopLimitTimeInForce='GTC'
            )
            logging.info("OCO order placed: %s", order)
            return order
        except (BinanceAPIException, BinanceRequestException) as e:
            logging.error("Error placing OCO order: %s", str(e))
            raise

    def place_twap_order(self, symbol, side, total_quantity, duration_minutes, intervals):
        # TWAP: split total_quantity into intervals over duration_minutes
        symbol = self.validate_symbol(symbol)
        total_quantity = self.validate_quantity(total_quantity)
        side = side.upper()
        if side not in ['BUY', 'SELL']:
            raise ValueError("Side must be BUY or SELL.")
        if intervals <= 0:
            raise ValueError("Intervals must be positive.")

        quantity_per_order = total_quantity / intervals
        interval_seconds = (duration_minutes * 60) / intervals

        orders = []
        for i in range(intervals):
            try:
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type='MARKET',
                    quantity=quantity_per_order
                )
                orders.append(order)
                logging.info("TWAP order %d placed: %s", i+1, order)
                if i < intervals - 1:
                    import time
                    time.sleep(interval_seconds)
            except (BinanceAPIException, BinanceRequestException) as e:
                logging.error("Error placing TWAP order %d: %s", i+1, str(e))
                raise
        return orders

    def place_grid_orders(self, symbol, base_price, range_percent, num_orders, quantity_per_order):
        # Grid: place limit orders above and below base_price
        symbol = self.validate_symbol(symbol)
        base_price = self.validate_price(base_price)
        range_percent = float(range_percent)
        num_orders = int(num_orders)
        quantity_per_order = self.validate_quantity(quantity_per_order)

        orders = []
        for i in range(1, num_orders + 1):
            # Buy orders below base_price
            buy_price = base_price * (1 - (range_percent / 100) * i / num_orders)
            try:
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side='BUY',
                    type='LIMIT',
                    quantity=quantity_per_order,
                    price=buy_price,
                    timeInForce='GTC'
                )
                orders.append(order)
                logging.info("Grid buy order %d placed: %s", i, order)
            except (BinanceAPIException, BinanceRequestException) as e:
                logging.error("Error placing grid buy order %d: %s", i, str(e))
                raise

            # Sell orders above base_price
            sell_price = base_price * (1 + (range_percent / 100) * i / num_orders)
            try:
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side='SELL',
                    type='LIMIT',
                    quantity=quantity_per_order,
                    price=sell_price,
                    timeInForce='GTC'
                )
                orders.append(order)
                logging.info("Grid sell order %d placed: %s", i, order)
            except (BinanceAPIException, BinanceRequestException) as e:
                logging.error("Error placing grid sell order %d: %s", i, str(e))
                raise
        return orders