import alpaca_trade_api as tradeapi
import numpy as np
import time

SEC_KEY = 'bxx9mpoKcoGZDnkm2QTNOY1TGIb5erhcbKFtVM3m'
PUB_KEY = 'PKNRULROQYCRTMK9O9BD'
BASE_URL = 'https://paper-api.alpaca.markets'
api = tradeapi.REST(key_id=PUB_KEY, secret_key=SEC_KEY, base_url=BASE_URL)

def get_data():
    # Returns a an numpy array of the closing prices of the past 5 minutes
    market_data = api.get_bars(symb, 'minute', limit=5)
    
    close_list = []
    for bar in market_data[symb]:
        close_list.append(bar.c)
    
    close_list = np.array(close_list, dtype=np.float64)

    return close_list

def buy(qty, symbol):
    api.submit_order(
        symbol=symbol,
        qty=qty,
        side='buy',
        type='market',
        time_in_force='gtc'
    )

def sell(qty, symbol):
    api.submit_order(
        symbol=symbol,
        qty=qty,
        side='sell',
        type='market',
        time_in_force='gtc'
    )

symb = ""
pos_held = False

while True:
    print("")
    print("Checking Price")

    close_list = get_data()

    ma = np.mean(close_list)
    last_price = close_list[4]

    print("Moving Average: " + str(ma))
    print("Last Price: " + str(last_price))

    if (ma + 0.1 < last_price and not pos_held):
        print("Buy")
        buy(1, symb)
        pos_held = True

    elif ma - 0.1 > last_price and pos_held:
        print("Sell")
        sell(1, symb)
        pos_held = False

    time.sleep(60)