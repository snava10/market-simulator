
from events import QuoteEvent
from datetime import datetime
from logger import Logger
import requests
import json
import time
import csv
import sqlite3

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

def get_quote_dict(symbol='btc'):
    data = get_live_data()
    d = dict({ 'time' : data['time']['updatedISO'],
          'price': data['bpi']['USD']['rate_float']
        })
    return d

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

def write_to_csv(csvfile, rows):
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerows(rows)#[quote['time'], quote['price']])
    csvfile.close()

def save_to_database(db_name, quote):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("insert into btc values({},'{}')".format(quote['price'], quote['time']))
    conn.commit()
    conn.close()

if __name__=='__main__':
    last_time = None
    line = 1
    db_name = 'data/database'
    
    while 1:
        try:
            print(str(line) + ' Get quote ...')
            line+=1
            quote = get_quote_dict()
            new_time = quote['time']
            
            if new_time != last_time:
                print(quote)
                #rows.append([quote['time'],quote['price']])
                #with open('data/btc_minute_data.csv', 'a', newline='\n') as csvfile:
                    # write_to_csv(csvfile, rows)
                    #csvfile.write(str(quote['time']) + ',' + str(quote['price']) + '\n')
                save_to_database(db_name, quote) 
                last_time = new_time
            print('Sleeping 59 seconds')
            time.sleep(59)
        except Exception as e:
            print(e)
            time.sleep(5)
