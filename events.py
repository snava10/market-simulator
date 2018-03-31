
from threading import Thread
from logger import Logger


class Event(Logger):

    def __init__(self, pname, params=None):
        self.name = pname
        self.params = params
    
    def get_name(self):
        return self.name

    def get_params(self):
        return self.params

    def __eq__(self, other):
        return self.name == other.get_name()

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name


class QuoteEvent(Event):

    def __init__(self, params=None):
        Event.__init__(self, 'quote_event', params)


class BuyEvent(Event):
    
    def __init__(self, params=None):
        Event.__init__(self, 'buy', params)


class SellEvent(Event):

    def __init__(self, params=None):
        Event.__init__(self, 'sell', params)


class OrderCompletionEvent(Event):

    def __init__(self, order_completion):
        Event.__init__(self, 'order_completion', (order_completion,))
        self.trader_id = order_completion.trader_id

    def __eq__(self, other):
        return Event.__eq__(self, other) and other.trader_id == self.trader_id

    def __hash__(self):
        return Event.__hash__(self) & hash(self.trader_id)


class RegisterTraderEvent(Event):
    def __init__(self, params=None):
        Event.__init__(self, 'register_trader', params)


class GetTraderBalancesEvent(Event):
    def __init__(self, params=None):
        Event.__init__(self, 'trader_balances', params)


class GetTraderPositionsEvent(Event):
    def __init__(self, params=None):
        Event.__init__(self, 'trader_positions', params)


class EventHub(Logger):
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event, handler):
        self.subscribers.setdefault(event, []).append(handler)

    def fire(self, event):
        for handler in self.subscribers[event]:
            thread = Thread(target=handler, args=event.get_params())
            thread.start()
