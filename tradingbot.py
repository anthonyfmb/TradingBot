import alpaca_trade_api as tradeapi
import numpy as np
import datetime as dt
import pytz
import time
import argparse
from alpaca_trade_api.rest import TimeFrame

'''
    This is a trading script that you can run in the cloud and customize with your own trading algorithms
    The example uses the Alpaca Trading API, which is a free algorithmic trading platform that allows for paper trading
    This project was built from LiorB-D's TradingBot
'''

SEC_KEY = ''
PUB_KEY = 'PKWWDFXGUAI923FPFH4C'
BASE_URL = 'https://paper-api.alpaca.markets'
api = tradeapi.REST(key_id= PUB_KEY, secret_key=SEC_KEY, base_url=BASE_URL)


def get_data():
    now = dt.datetime.now(pytz.timezone('UTC'))
    fifteenMinPrior = (now - dt.timedelta(minutes=15)).isoformat()
    twentyMinPrior = (now - dt.timedelta(hours=1)).isoformat()

    market_data = api.get_bars(symb, TimeFrame.Minute, start=twentyMinPrior, end=fifteenMinPrior, limit=5)
    
    close_list = []
    for bar in market_data:
        close_list.append(bar.c)
    
    close_list = np.array(close_list, dtype=np.float64)

    return close_list

def buy(q, s): # Returns nothing, makes call to buy stock
    api.submit_order(
        symbol=s,
        qty=q,
        side='buy',
        type='market',
        time_in_force='gtc'
    )
def sell(q, s): # Returns nothing, makes call to sell stock
    api.submit_order(
        symbol=s,
        qty=q,
        side='sell',
        type='market',
        time_in_force='gtc'
    )

symb = ""
quantity = 0
pos_held = False

parser = argparse.ArgumentParser(description='')
parser.add_argument('-q', '--quantity', type=int, required=True, help='Specifies the amount of stocks that can be traded')
parser.add_argument('-s', '--symbols', type=str, required=True, help='Specifies the stocks to be traded')

args = parser.parse_args()
symb = args.symbol
quantity = args.quantity

while True:
    print("")
    print("Checking Price")
    
    close_list = get_data()

    ma = np.mean(close_list)
    last_price = close_list[4]

    print("Moving Average: " + str(ma))
    print("Last Price: " + str(last_price))

    if ma + 0.1 < last_price and not pos_held: # Buy when moving average is ten cents below the last price
        print("Buy")
        buy(quantity, symb)
        pos_held = True
    
    elif ma - 0.1 > last_price and pos_held: # Sell when moving average is ten cents above the last price
        print("Sell")
        sell(quantity, symb)
        pos_held = False
    
    time.sleep(60)
