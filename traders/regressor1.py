from trader import Trader
from events import EventHub
import numpy as np
import pandas as pd


class Regressor1Trader(Trader):

    def __init__(self, pname, pevent_hub):
        Trader.__init__(self, pname, pevent_hub)

    def train(self, hist_data):
        x = np.array(range(len(hist_data)))
        y = np.array(hist_data)
        degree = 3

        z = np.polyfit(x, y, degree)
        self.p = np.poly1d(z)

        print(z)
        print(self.p(0.5))


if __name__ == '__main__':
    event_hub = EventHub()
    regressor_trader = Regressor1Trader('regressor1', event_hub)
    df = pd.read_csv('../data/btc.csv', names=['date', 'price'], parse_dates=True, index_col='date')
    mean = df['price'].mean()
    std = df['price'].std()
    minimum = df['price'].min()
    maximum = df['price'].max()
    # df['price'] = (df['price'] - mean) / std
    df['price'] = (df['price'] - minimum) / (maximum - minimum)
    data = np.array(df['price'])
    # print(arr)
    # data = [0.0, 0.8, 0.9, 0.1, -0.8, -1.0]
    regressor_trader.train(data)
