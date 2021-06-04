import os

from binance import Client
from binance.enums import ORDER_TYPE_LIMIT_MAKER
from binance.enums import SIDE_BUY
from binance.enums import SIDE_SELL

API_KEY_TO_OPERATE = os.getenv('API_KEY_TO_OPERATE', None)
SECRET_TO_OPERATE = os.getenv('SECRET_TO_OPERATE', None)

binance_client = Client(API_KEY_TO_OPERATE, SECRET_TO_OPERATE)


def buy(pair='BNBBUSD', amount=0, take_profit=1.0015, stop_loss=0):
    print(f'Buy {pair} {amount} {take_profit} {stop_loss}')
    depth = binance_client.get_order_book(symbol=pair)
    print(f'Create order at {depth["bids"][0]}')
    price = depth['bids'][0][0]

    # Try to make an ordedr using limit maker (it will fail if it automatically matchs)
    # return False
    placed = False
    while not placed:
        order = binance_client.create_test_order(
            symbol=pair,
            side=SIDE_BUY,
            type=ORDER_TYPE_LIMIT_MAKER,
            quantity=amount,
            price=price,
        )
        placed = True
        print(order)
        # TODO if placed is false, reget the order book and retry

    # TODO:
    # place a sell order
    if take_profit != 0:
        price = price * take_profit
        placed = False
        while not placed:
            order = binance_client.create_test_order(
                symbol=pair,
                side=SIDE_SELL,
                type=ORDER_TYPE_LIMIT_MAKER,
                quantity=amount,
                price=price,
            )
            placed = True
            print(order)
            # TODO if placed is false, reget the order book and retry
    # TODO: make an oco with stop loss


def sell_at_current(pair='BNBBUSD', amount=0):
    print(f'Sell {pair} {amount}')
    depth = binance_client.get_order_book(symbol=pair)
    print(f'Create order at {depth["asks"][0]}')
    price = depth['asks'][0][0]

    # TODO: while not executed, retry to avoid paying fees
    placed = False
    while not placed:
        order = binance_client.create_test_order(
            symbol=pair,
            side=SIDE_SELL,
            type=ORDER_TYPE_LIMIT_MAKER,
            quantity=amount,
            price=price,
        )
        placed = True
        print(order)
        # TODO if placed is false, reget the order book and retry


def stop_all_orders(pair='BNBBUSD'):
    orders = binance_client.get_open_orders(symbol=pair)
    for order in orders:
        # TODO: do something with the result
        result = binance_client.cancel_order(symbol=pair, orderId=order['orderId'])
        print(result)


if __name__ == '__main__':
    buy(amount=0)
