
from events import QuoteEvent
from datetime import datetime
from logger import Logger
import requests
import json


class Quote(Logger):
    def __init__(self, pdatetime, pprice, psymbol='btc'):
        self.datetime = pdatetime
        self.price = pprice
        self.symbol = psymbol

    def get_price(self):
        return self.price

    def get_datetime(self):
        return self.datetime

    def get_symbol(self):
        return self.symbol

    def __str__(self):
        return 'time:%s, price:%s' % (self.datetime, self.price)

    def __unicode__(self):
        return u'%s' % self.__str__()

    def __repr__(self):
        return self.__str__()


def get_quote(symbol='btc'):
    data = get_live_data()
    return Quote(datetime.now(), data['bpi']['USD']['rate_float'])


def broadcast_quote(quote, event_hub):
    event_hub.fire(QuoteEvent((quote,))) 


def broadcast_quotes(quotesDict, event_hub):
    event_hub.fire(QuoteEvent((quotesDict,)))


def get_and_broadcast_quote(event_hub):
    broadcast_quote(get_quote(), event_hub)


def get_quotes(symbols=['btc']):
    quotesDict = {}
    for q in [get_quote(s) for s in symbols]:
        quotesDict[q.get_symbol()] = q
    return quotesDict

def get_live_data():
    url = "https://api.coindesk.com/v1/bpi/currentprice.json"
    response = requests.request("GET", url)
    return json.loads(response.text)

