
class Order:
    def __init__(self, porder_type, pvolume, psymbol, ptrader_id, ptrader_name):
        self.order_type = porder_type
        self.volume = pvolume
        self.trader_id = ptrader_id
        self.symbol = psymbol
        self.trader_name = ptrader_name

    def get_trader_id(self):
        return self.trader_id

    def get_symbol(self):
        return self.symbol

    def get_volume(self):
        return self.volume

    def get_order_type(self):
        return self.order_type

    def __str__(self):
        return 'type: %s, symbol: %s, volume: %d, trader: %s' % (self.order_type, self.symbol, self.volume, self.trader_name)

    def __unicode__(self):
        return u'%s' % self.__str__()

    def __repr__(self):
        return self.__str__()    


class OrderCompletion:
    def __init__(self, status, order, message=None, symbol_unit_price=None, payed_out=None, payed_in=None,
                 symbol_volume_in=None, symbol_volume_out=None):
        self.trader_id = order.get_trader_id()
        self.status = status
        self.order = order
        self.traded_symbol = order.symbol
        self.symbol_unit_price = symbol_unit_price
        self.payed_out = payed_out
        self.payed_in = payed_in
        self.symbol_volume_in = symbol_volume_in
        self.symbol_volume_out = symbol_volume_out
        self.message = message

    def default(trader_id):
        order = Order(None, None, None, trader_id, None)
        return OrderCompletion(None, order)


class BuyOrderCompletion(OrderCompletion):
    def __init__(self, status, order, symbol_unit_price, payed_out, symbol_volume_in):
        OrderCompletion.__init__(self, status, order, 'Success', symbol_unit_price, payed_out, 0, symbol_volume_in, 0)


class SellOrderCompletion(OrderCompletion):
    def __init__(self, status, order, symbol_unit_price, payed_in, symbol_volume_out):
        OrderCompletion.__init__(self, status, order, 'Success', symbol_unit_price, 0, payed_in, 0, symbol_volume_out)

    def __str__(self):
        return 'type %s, symbol: %s, symbol_volume: %d, trader: %s' % (self.order_type, self.symbol, self.volume,
                                                                       self.trader_name)
