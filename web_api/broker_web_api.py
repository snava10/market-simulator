from flask import Flask
from flask import request
from uuid import UUID
import json

app = Flask(__name__)
broker = None


def start_web_api(pbroker):
    if not pbroker:
        raise Exception('broker is null')
    global broker
    broker = pbroker
    app.run(debug=False)


@app.route('/balances', methods=['POST'])
def get_trader_balances():
    global broker
    trader_ids = []
    for tid in [x.strip(' ') for x in request.form['trader_ids'].split(',')]:
        trader_ids.append(UUID(tid))
    if not broker:
        return 'Broker is null'
    return json.dumps(broker.get_trader_balances(trader_ids))


@app.route('/positions', methods=['POST'])
def get_trader_positions():
    global broker
    trader_ids = []
    for tid in [x.strip(' ') for x in request.form['trader_ids'].split(',')]:
        trader_ids.append(UUID(tid))
    if not broker:
        return 'Broker is null'
    return json.dumps(broker.get_trader_positions(trader_ids))


@app.route('/trader-ids', methods=['GET'])
def get_registered_trader_ids():
    global broker
    return json.dumps(list(map(str, broker.get_registered_trader_ids())))
