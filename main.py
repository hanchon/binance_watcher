from binance import Client
from binance import ThreadedDepthCacheManager
from binance import ThreadedWebsocketManager

from alerter import Alerter
from config import API_KEY
from config import SECRET
from constants import ARRIBA
from pair import Pair

client = Client(API_KEY, SECRET)

pairs = [
    'BNBBUSD',
    'ETHBUSD',
    'BTCBUSD',
    'DOGEBUSD',
    'MATICBUSD',
    'ADABUSD',
    'DOTBUSD',
    'XRPBUSD',
    'SHIBBUSD',
    'KSMBUSD',
]

data = {}

print('Creating pairs')
for p in pairs:
    data[p] = Pair(p)

print('Creating klines')
for pair in pairs:
    klines = client.get_historical_klines(pair, Client.KLINE_INTERVAL_1MINUTE, '30 minutes ago UTC')
    data[pair].init_emas(klines)

print('Creating alerter')
alerter = Alerter()

print('Creating websockert for klines')
# socket manager using threads
twm = ThreadedWebsocketManager()
twm.start()

print('Creating websockert for depth')
# depth cache manager using threads
dcm = ThreadedDepthCacheManager()
dcm.start()


def handle_socket_message(msg):
    global data
    global alerter
    if msg['e'] == 'kline':
        data[msg['s']].add_ema_value(float(msg['k']['T']), float(msg['k']['o']))

    res, direction = data[msg['s']].tendency_has_changed()
    if res:
        if direction == ARRIBA:
            emoji = '\U0001F525'
        else:
            emoji = '\U000026C4'
        bolsa = '\U0001F4B0'
        alerter.broadcast(
            f'[{msg["s"]}] -> {emoji} Cambió hacia {direction} {emoji}. {bolsa} ({data[msg["s"]].bids[0][0]})', )


def handle_dcm_message(depth_cache):
    global data
    data[depth_cache.symbol].bids = depth_cache.get_bids()[:5]
    data[depth_cache.symbol].asks = depth_cache.get_asks()[:5]


for p in pairs:
    twm.start_kline_socket(callback=handle_socket_message, symbol=p)
    dcm.start_depth_cache(callback=handle_dcm_message, symbol=p)

alerter.run_the_bot()
