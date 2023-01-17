import json
import os
import sys
import datetime
import websocket
from threading import Thread
from queue import Queue
import hmac
import time
import hashlib
import requests

api_key, api_secret, userdata_listenkey = os.environ['API_KEY'], os.environ['SECRET_KEY'], os.environ.get('USERDATA_LISTENKEY')
step = 30
def hashing(query):
    return hmac.new(
        api_secret.encode("utf-8"), query.encode("utf-8"), hashlib.sha256
    ).hexdigest()
def get_timestamp():
    return int(time.time() * 1000)

priceq = Queue()
pricelist = []
do_order = False
def makeString(dictionary):
    arr = sorted(dictionary.items(), key = lambda x:x)
    res = str(arr[0][0])+'='+str(arr[0][1])
    for i, elem in enumerate(arr):
        if i == 0:
            continue
        res+='&'+str(elem[0])+'='+str(elem[1])
    print(res)
    return res
def makeOrderAndWait(price:float):
    request = {
        'id':f'testid1488{n+1}',
        'method': 'order.place',
        'params': {
            'apiKey': api_key,
            'symbol': 'ETHUSDT',
            'side': 'sell',
            'type': 'LIMIT',
            'price': 1588.63000000,
            'timeInForce': 'GTC',
            'timestamp': get_timestamp(),
            'quantity': round(3,3), #step = 30USDT, не нашёл способа, как при покупке указать сумму, на которую нужно купить
        }
    }
    r_signature = makeString(request['params'])
    request['params']['signature'] = hashing(r_signature)
    socket = f'wss://testnet.binance.vision/ws-api/v3'
    request_query = json.dumps(request)
    def on_open(wsapp2):
        wsapp2.send(request_query)
    def on_message(wsapp2, message):
        print(message)
    def on_error(wsapp2, error):
        print(error)

    wsapp2 = websocket.WebSocketApp(socket, on_message=on_message, on_error=on_error, on_open = on_open)
    wsapp2.run_forever()

def orders():
    global priceq
    global n
    global pricelist
    global do_order
    while True:
        while priceq.qsize() != 0:
            price = float(priceq.get())
            if n > 1 and price > pricelist[-1] and not do_order:
                do_order = True
                makeOrderAndWait(price)
                do_order = False
                print('Done!')
                sys.exit()
            pricelist.append(price)
            print(price)
            sys.stdout.flush()
def init_listen():

    socket = f'wss://testnet.binance.vision/ws/ethusdt@trade'

    def on_message(wsapp, message):
        json_message = json.loads(message)
        handle_trades(json_message)

    def on_error(wsapp, error):
        print(error)

    wsapp = websocket.WebSocketApp(socket, on_message=on_message, on_error=on_error)
    wsapp.run_forever()
torders = Thread(target = orders)
n = 0
working = False
def orders_status():
    pingurl = f'https://testnet.binance.vision/api/v3/userDataStream'
    def ping():
        global userdata_listenkey
        if not userdata_listenkey:
            response = requests.post(pingurl, headers={'X-MBX-APIKEY': api_key})
        print(response.text)
        response_json = response.json()
        if not userdata_listenkey:
            userdata_listenkey = response_json['listenKey']
            print('Got listenKey',userdata_listenkey)
            os.environ['USERDATA_LISTENKEY'] = userdata_listenkey
            os.environ['USERDATA_LISTENKEY_TIMESTAMP'] = str(time.time())
            #timestamp notice
    ping()
    listenupdates_socket = f'wss://testnet.binance.vision/ws/{userdata_listenkey}'
    def on_message(wsapp, message):
        print(message)
    def on_error(wsapp, error):
        print(error)
    def on_open(wsapp):
        print('Listening to account updates has started')

    wsapp = websocket.WebSocketApp(listenupdates_socket, on_message=on_message, on_error=on_error, on_open=on_open)
    wsapp.run_forever()
torders_status = Thread(target = orders_status)
def handle_trades(json_message):
    global n
    global priceq
    global working
    price = json_message['p']
    print(f'UPD {n}, {price}')
    n+=1
    priceq.put(price)
    sys.stdout.flush()
    if not working:
        working = True
        torders.start()
        torders_status.start()
init_listen()