from broker import Broker
from events import EventHub
from trader import BuyBuyTrader, BuySellTrader
from web_api.broker_web_api import *
from threading import Thread


def run():
    traders = [BuySellTrader(event_hub, 'buy sell %d' % x) for x in range(1)]
    traders.append(BuyBuyTrader(event_hub))
    for t in traders:
        t.register()

    broker.start(['btc'])


if __name__ == '__main__':
    event_hub = EventHub()
    broker = Broker(event_hub)
    thread = Thread(target=run)
    thread.start()
    start_web_api(broker)
