import alpaca_trade_api as tradeapi
import numpy as np
import datetime as dt
import pytz
import time
import argparse
from alpaca_trade_api.rest import TimeFrame

SEC_KEY = ''
PUB_KEY = 'PKWWDFXGUAI923FPFH4C'
BASE_URL = 'https://paper-api.alpaca.markets'
api = tradeapi.REST(key_id= PUB_KEY, secret_key=SEC_KEY, base_url=BASE_URL)

# Returns 20 day moving average
def get_20_day(symb):
    now = dt.datetime.now(pytz.timezone('UTC'))

    # Free version of Alpaca doesn't allow receiving data from the last 15 minutes, so our end time will be 15 minutes ago
    fifteenMinPrior = (now - dt.timedelta(minutes=15)).isoformat() 
    fiftyDaysPrior = (now - dt.timedelta(days=50)).isoformat()

    market_data = api.get_bars(symb, TimeFrame.Minute, start=fiftyDaysPrior, end=fifteenMinPrior, limit=20)
    
    close_list = []
    for bar in market_data:
        close_list.append(bar.c)
    
    ma = np.mean(np.array(close_list, dtype=np.float64))

    return ma

# Gets 100 day moving average
def get_100_day(symb):
    now = dt.datetime.now(pytz.timezone('UTC'))

    fifteenMinPrior = (now - dt.timedelta(minutes=15)).isoformat()
    twoHundredDaysPrior = (now - dt.timedelta(days=200)).isoformat()

    market_data = api.get_bars(symb, TimeFrame.Minute, start=twoHundredDaysPrior, end=fifteenMinPrior)
    
    close_list = []
    for bar in market_data:
        close_list.append(bar.c)
    
    ma = np.mean(np.array(close_list, dtype=np.float64))

    return ma

def buy(q, s): 
    api.submit_order(
        symbol=s,
        qty=q,
        side='buy',
        type='market',
        time_in_force='gtc'
    )
def sell(q, s):
    api.submit_order(
        symbol=s,
        qty=q,
        side='sell',
        type='market',
        time_in_force='gtc'
    )

symbols = []
pos_held = {}

parser = argparse.ArgumentParser(description='')
parser.add_argument('-q', '--quantity', type=int, required=False, help='Specifies the amount of stocks that can be traded')
parser.add_argument('-s', '--symbols', nargs='+', type=str, required=True, help='Specifies the stocks to be traded (max 5)')

args = parser.parse_args()
symbols = args.symbols

for symb in symbols:
    pos_held[symb] = False

while True:

    for symb in symbols:
        print("")
        print(symb + ": ")
        
        twenty = get_20_day(symb)
        hundred = get_100_day(symb)

        print("20 Day Moving Average: " + str(twenty))
        print("100 Day Moving Average: " + str(hundred))

        if twenty > hundred and not pos_held[symb]:
            print("Buy")
            buy(1, symb)
            pos_held[symb] = True
        
        elif twenty < hundred and pos_held[symb]:
            print("Sell")
            sell(1, symb)
            pos_held[symb] = False
    
    # Wait half a day
    time.sleep(43200)
