from events import QuoteEvent, BuyEvent, OrderCompletionEvent, RegisterTraderEvent, SellEvent
from order import Order, OrderCompletion
from logger import Logger
import uuid


class Trader(Logger):
    def __init__(self, pname, pevent_hub):
        self.name = pname
        self.id = uuid.uuid4()
        pevent_hub.subscribe(QuoteEvent(), self.trade)
        pevent_hub.subscribe(OrderCompletionEvent(OrderCompletion.default(self.id)), self.order_completion_handler)
        self.event_hub = pevent_hub

    def get_id(self):
        return self.id

    def train(self, hist_data):
        raise Exception('Not implemented')

    def trade(self, quotes_dict):
        print(self.name + ' is trading ...')

    def order_completion_handler(self, order_completion):
        if not order_completion.trader_id == self.id:
            self.warning('Trades %s should not be receiving this notification' % self.name)
        else:
            order = order_completion.order
            status = order_completion.status
            self.info('Trader %s acknowledge order %s has been completed with status %s ' %
                      (self.name, order, status))

    def register(self):
        self.event_hub.fire(RegisterTraderEvent((self.id,)))

    def get_name(self):
        return self.name

    def __str__(self):
        return self.name


class BuyBuyTrader(Trader):
    def __init__(self, event_hub, name='buy buy trader'):
        Trader.__init__(self, name, event_hub)

    def trade(self, quotes_dict):
        Trader.trade(self, quotes_dict)
        buy_order = Order('buy', 1, 'btc', self.id, self.name)
        #  Triggering a buy event that will be recieved by the broker
        #  A single parameter (the order) is needed
        buy_event = BuyEvent((buy_order,))
        self.event_hub.fire(buy_event)


class BuySellTrader(Trader):
    def __init__(self, event_hub, name='buy sell trader'):
        Trader.__init__(self, name, event_hub)
        self.nextAction = 0

    def trade(self, quotes_dict):
        Trader.trade(self, quotes_dict)
        if self.nextAction % 2:
            # buy
            buy_order = Order('buy', 1, 'btc', self.id, self.name)
            event = BuyEvent((buy_order,))
        else:
            sell_order = Order('sell', 1, 'btc', self.id, self.name)
            event = SellEvent((sell_order,))

        self.event_hub.fire(event)
        self.nextAction += 1
