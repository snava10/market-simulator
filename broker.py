
import time

from events import BuyEvent, SellEvent, OrderCompletionEvent, RegisterTraderEvent, GetTraderBalancesEvent, \
    GetTraderPositionsEvent
from logger import Logger
from order import BuyOrderCompletion, OrderCompletion, SellOrderCompletion
from quote import get_quotes, broadcast_quotes


class Broker(Logger):

    def __init__(self, event_hub):
        event_hub.subscribe(BuyEvent(), self.buy)
        event_hub.subscribe(SellEvent(), self.sell)
        event_hub.subscribe(RegisterTraderEvent(), self.register_trader)
        event_hub.subscribe(GetTraderPositionsEvent(), self.get_trader_positions)
        event_hub.subscribe(GetTraderBalancesEvent(), self.get_trader_balances)
        self.event_hub = event_hub
        self.symbols_table = {}
        self.positions = {}
        self.balances = {}

    def buy(self, order):
        try:
            self.info('received buy order from trader %s \n' % order.trader_name)
            symbol = order.get_symbol()
            volume = order.get_volume()
            security_price = self.symbols_table[symbol].get_price()
            bought_quantity = volume / security_price
            trader_id = order.get_trader_id()

            if trader_id not in self.positions:
                self.info('Trader with id %s is not registered in this broker' % trader_id)
                order_completion = OrderCompletion('fail', order, 'Trader with id %s is not registered in this broker' 
                        % trader_id, security_price, volume, bought_quantity)
                self.event_hub.fire(OrderCompletionEvent(order_completion))
                return
            current_positions = self.positions[trader_id]
            current_positions.setdefault(symbol, 0)
            current_positions[symbol] += bought_quantity

            self.update_balance(trader_id, -volume, symbol, bought_quantity)
            order_completion = BuyOrderCompletion('success', order, security_price, volume, bought_quantity)
        except Exception as e:
            order_completion = BuyOrderCompletion('fail', order, security_price, volume, bought_quantity)
            self.error(e)
        finally:
            self.event_hub.fire(OrderCompletionEvent(order_completion))

    def sell(self, order):
        order_completion = None
        try:
            self.info('received sell order from trader %s\n' % order.trader_name)
            symbol_sell_volume = order.get_volume()
            symbol = order.get_symbol()
            security_price = self.symbols_table[symbol].get_price()
            sold_volume = symbol_sell_volume * security_price
            trader_id = order.get_trader_id()

            if trader_id not in self.positions:
                self.info('Trader with id %s is not registered in this broker' % order.get_trader_id())
                order_completion = OrderCompletion('fail', order, 'Trader with id %s is not registered in this broker'
                                                   % order.get_trader_id(), security_price, symbol_sell_volume,
                                                   sold_volume)
                self.event_hub.fire(OrderCompletionEvent(order_completion))
                return

            if symbol_sell_volume <= 0:
                self.info('The sell volume should be positive')
                order_completion = OrderCompletion('fail', order, 'The sell volume should be positive',
                                                   security_price, symbol_sell_volume, sold_volume)
                self.event_hub.fire(OrderCompletionEvent(order_completion))
                return
            
            current_positions = self.positions[trader_id]
            current_positions.setdefault(symbol, 0)

            if symbol_sell_volume > current_positions[symbol]:
                self.info('Trader {0} is trying to sell {1} {2} but it only holds {3}'
                          .format(trader_id, symbol_sell_volume, symbol, current_positions[symbol]))
                order_completion = SellOrderCompletion('fail', order, security_price, sold_volume, symbol_sell_volume)
            else:
                self.update_balance(trader_id, sold_volume, symbol, -symbol_sell_volume)
                order_completion = SellOrderCompletion('success', order, security_price, sold_volume, symbol_sell_volume)
        except Exception as e:
            order_completion = SellOrderCompletion('fail', order, security_price, sold_volume, symbol_sell_volume)
            self.event_hub.fire(OrderCompletionEvent(order_completion))
            self.error(e)
        finally:
            self.event_hub.fire(OrderCompletionEvent(order_completion))

    def update_balance(self, trader_id, cash_flow, symbol, symbol_flow):
        balance = self.balances[trader_id]
        balance['cash'] += cash_flow
        if symbol in balance:
            balance[symbol] += symbol_flow
        else:
            balance[symbol] = symbol_flow

    def register_trader(self, trader_id):
        self.positions.setdefault(trader_id, {})
        self.balances.setdefault(trader_id, {'cash': 0})

    def get_trader_balances(self, trader_ids):
        res = {}
        for tid in trader_ids:
            res[str(tid)] = dict(self.balances.get(tid, {}))
        return res
        # return [{tid: dict(self.positions.get(tid, {}))} for tid in trader_ids]

    def get_trader_positions(self, trader_ids):
        res = {}
        for tid in trader_ids:
            res[str(tid)] = dict(self.positions.get(tid, {}))
        return res

    def get_registered_trader_ids(self):
        return self.positions.keys()

    def start(self, symbols):
        while 1:
            try:
                print('-----------------------------------------------------------------------------')
                self.symbols_table = get_quotes(symbols)
                self.info('Broadcasting the new quotes %s' % self.symbols_table)
                broadcast_quotes(dict(self.symbols_table), self.event_hub)
                time.sleep(50)
            except Exception as e:
                self.error(e)
                break
