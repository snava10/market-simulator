from events import Event, QuoteEvent, EventHub
from trader import Trader, BuyBuyTrader, BuySellTrader
from quote import Quote, get_quote, get_and_broadcast_quote
from broker import Broker
from order import Order


def run():
    event_hub = EventHub()
    broker = Broker(event_hub)
    traders = [BuySellTrader(event_hub, 'buy sell %d' % x) for x in range(1)]
    traders.append(BuyBuyTrader(event_hub))
    for t in traders:
        t.register()

    broker.start(['btc'])


if __name__ == '__main__':
    run()
