import json
import os
import sys
import datetime
import websocket
from threading import Thread
from queue import Queue

api_key, api_secret = os.environ['API_KEY'], os.environ['SECRET_KEY']
priceq = Queue()
def orders():
    global priceq
    while True:
        while priceq.qsize() != 0:
            price = priceq.get()
            print(price)
            sys.stdout.flush()
        #В этом месте мы и решаем, нужнно ли делать ордер какой-то, открывать новое соединение
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
n = 1
working = False
def handle_trades(json_message):
    global n
    global priceq
    global working
    price = json_message['p']
    '''
    date_time = datetime.datetime.fromtimestamp(json_message['E'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
    print("SYMBOL: " + json_message['s'])
    print("PRICE: " + price)
    print("QTY: " + json_message['q'])
    print("TIMESTAMP: " + str(date_time))
    print("-----------------------")
    '''
    print(f'UPD {n}')
    n+=1
    priceq.put(price)
    sys.stdout.flush()
    if not working:
        working = True
        torders.start()
init_listen()