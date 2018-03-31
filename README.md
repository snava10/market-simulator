# market-simulator
Simple implementation of a broker to assist in the developing and testing of trading algorithms

# Get Started

- Clone this repository
- Run `python3 main.py`

## Add your own algorithm

- Create a class that inherit from `Trader`
- Override the method `trade`. Inside place the logic of your trading algorithm.
- Override the method `order_completion_handler` to internally handle the result of your trades. You could keep a track of your balance, update your model or execute any other custom logic. Check the file `trader.py` for examples.

## Register your trader

On the file `main.py` add an instance of your class to the list of traders.
```
def run():
    event_hub = EventHub()
    broker = Broker(event_hub)
    traders = [BuySellTrader(event_hub, 'buy sell %d' % x) for x in range(1)]
    traders.append(BuyBuyTrader(event_hub))
    for t in traders:
        t.register()

    broker.start(['btc'])
```
## Implementation Details

Although all the components of the simulator run in a single process, the system is composed of completely decouple modules that comunicate through events. The traders and the broker are the main components and the event hub is the shared shannel of comunication. If you want to add a new component, like a UI, all you have to do is subscribe or fire the correct events.

Below there is a table of the events and how they are used by the broker and the traders.

| Event        | Broker           | Trader  |
| ------------- |:-------------:| -----:|
| Quote | fire | subscribe |
| Buy | subscribe | fire |
| Sell | subscribe | fire |
| Order Completion | fire | subscribe |
| Register Trader | subscribe | fire |
| Get Trader Balance | subscribe | |
| Get Trader Positions | subscribe | |


