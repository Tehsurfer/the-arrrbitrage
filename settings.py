# settings.py a file to change elements of the project

from pathlib import Path
global PATH, Coins

PATH = Path("/home/jessekhorasanee/workspace/the-arrrbitrage/data/")


RUNTIME = 60*5 # Amount of time software runs ins
ALERTTHRESH = 0.015 # margin threshold for alerts
FLOW = 10000 #Amount Moved per arbitrage (in AUD)
CURRENCYEXCHANGEFEE = .003 # Exchange rate losses
CURRENCYEXCHANGEFLATFEE = 25 # Exchange rate losses


Coins = ['BTC','ETH','LTC','BCH','OMG','TRX',] #
Fiats = ['AUD','USD','NZD','GBP','EUR']
Native = ['AUD','AUD','AUD','AUD','AUD','AUD','USD','GBP','USD','USDT','USD','USD']
Native2 = ['AUD','AUD','AUD','AUD','AUD','AUD','USD','GBP','USD','USD','USD','USD']
OrderBookNeeded = [0,0,0,1,1,1,1,1,1,1,1,1]
ExchangeNames = ['coinspot',
             'coinspot nominal',
             'coinjar',
             'acx',
             'btcmarkets',
             'independentreserve',
             'bitfinex',
             'coinfloor',
             'kraken',
             'bittrex',
             'gemini',
             'bitstamp',]

TradeFees =  [0.01,
              0.02,
              0.0001,
              0.002,
              0.006,
              0.0048,
              0.002,
              0.0025,
              0.0025,
              0.0025,
              0.0025,
              0.0025]

#(Exhchange rates are just taken to all be in BTC)
CryptoWithdrawalRate = [
                        .001,
                        .001,
                        .0005,
                        .001,
                        .0005,
                        .001,
                        .0005,
                        .001,
                        .001,
                        .001,
                        .001,
                        .001]

DepositFees = [0, 0, 0, 0, 0, 0, 20, 0, 0, 0, 0, 0]

FiatWithdrawalFees = [ 0, 0, 0.0, 20, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

DisplayNames = ['Coinspot', 'CSpot B/S', 'Coinjar ', 'ACX.io   ', 'BTC Mrkts', 'IND RES  ',  'Bitfinex', 'Coinfloor', 'KrakenUS', 'Bittrex ', 'Gemini  ', 'Bitstamp']
