import settings
import ccxt
import requests
import coinspotscrape


exchanges = {}  # a placeholder for instaces of the exchange

for id in ccxt.exchanges:
    exchange = getattr(ccxt, id)
    exchanges[id] = exchange()

# now exchanges dictionary contains all exchange instances...

class Exchange(object):
    # A crypto currency base exchange class



    def __init__(self,name,nativeCurrency):
        self.name = name
        self.displayName = ''
        self.nativeCurrency = nativeCurrency
        self.tradeFees = 0.002
        self.depositFees = 0
        self.WBTCFees = .001 * 10000  # btc price
        self.WFIATFees = 0
        self.sellAsks = [1000000] * len(settings.Coins)
        self.buyBids = [0.001] * len(settings.Coins)
        self.successfullyLoaded = [0] * len(settings.Coins)



    def update(self):
        raise NotImplementedError

    def order_book_buy(self,coin,fillamount):
        #TO BUY CRYPTO

        # coinspot requires API key for all requests
        if self.name == 'coinspot':
            coinspot = ccxt.coinspot()
            coinspot.apiKey = '88cfb4705e658dea85ed0f580b40a4ce'
            coinspot.secret = '*KTGVNEK33Q85FBKUQA02AVLEE7B0JHK5G25XNCZZ29F80H1T2M6ETAVCMMB8HT9YXL1ELCRNU2VG3PPVW'


        orde = exchanges[self.name].fetch_order_book(coin+ '/' + self.nativeCurrency, limit=1000)
        totalfilled = 0
        totalpaid = 0
        i = 0
        print('exchange is' + self.name)
        if self.name == 'acx':
            tt = 0
        while totalfilled <= fillamount:
            if i < len(orde['asks']):
                price = orde['asks'][i][0]
                amount = orde['asks'][i][1]
                totalfilled += amount
                totalpaid += price * amount
                i += 1
            else:
                totalpaid = totalpaid*2
                break
        if totalfilled > fillamount:
            totalpaid -= orde['asks'][i - 1][0] * (totalfilled - fillamount)
        print(totalpaid)
        return (totalpaid / fillamount)

    def order_book_sell(self,coin,fillamount):
        #TO SELL CRYPTO

        # coinspot requires API key for all requests
        if self.name == 'coinspot':
            coinspot = ccxt.coinspot()
            coinspot.apiKey = '88cfb4705e658dea85ed0f580b40a4ce'
            coinspot.secret = 'KTGVNEK33Q85FBKUQA02AVLEE7B0JHK5G25XNCZZ29F80H1T2M6ETAVCMMB8HT9YXL1ELCRNU2VG3PPVW'

        orde = exchanges[self.name].fetch_order_book(coin + '/' + self.nativeCurrency, limit=1000)
        print(orde['bids'])

        totalfilled = 0
        totalpaid = 0
        i = 0

        while totalfilled <= fillamount:
            if i < len(orde['bids']):
                price = orde['bids'][i][0]
                amount = orde['bids'][i][1]
                totalfilled += amount
                totalpaid += price * amount
                i += 1
            else:
                totalpaid = totalpaid * 2
                break
        if totalfilled > fillamount:
            totalpaid -= orde['bids'][i - 1][0] * (totalfilled - fillamount)
        print(totalpaid)
        return (totalpaid / fillamount)

class ccxtApproved(Exchange):

    def update(self):

        print('Updating the prices at: ' + self.name + ' ...')
        for i,coin in enumerate(settings.Coins):
            try:
                self.sellAsks[i] = exchanges[self.name].fetch_ticker(coin + '/' + self.nativeCurrency)['ask']
                self.buyBids[i] = exchanges[self.name].fetch_ticker(coin + '/' +  self.nativeCurrency)['bid']
                self.successfullyLoaded[i] = 1
            except:
                self.sellAsks[i] = 1000000
                self.buyBids[i] = .001

class scraped(Exchange):


    def update(self):

        print('Updating the prices at: ' + self.name + ' ...')

        # Each exchange requires a different method for getting the prices so we must go case by case

        if self.name == 'coinspot':

            #Coinspot requires a key to access the public api
            coinspot = ccxt.coinspot()
            coinspot.apiKey = '88cfb4705e658dea85ed0f580b40a4ce'
            coinspot.secret = 'KTGVNEK33Q85FBKUQA02AVLEE7B0JHK5G25XNCZZ29F80H1T2M6ETAVCMMB8HT9YXL1ELCRNU2VG3PPVW'
            response = requests.get("https://www.coinspot.com.au/pubapi/latest")
            coinspotresponse = response.json()
            for i, coin in enumerate(settings.Coins):
                try:
                    temp = coinspotresponse['prices'][str.lower(coin)]
                    self.sellAsks[i] = float(temp['ask']) #sell asks
                    self.buyBids[i] = float(temp['bid']) # buy bids
                    self.successfullyLoaded[i] = 1
                except:
                    self.sellAsks[i] = 1000000
                    self.buyBids[i] = .001

        elif self.name == 'coinspot nominal':
            cs = coinspotscrape.coinspotscrape()
            for i, coin in enumerate(settings.Coins):
                try:
                    self.sellAsks[i] = cs.bid(coin)
                    self.buyBids[i] = cs.ask(coin)
                    self.successfullyLoaded[i] = 1
                except:
                    self.sellAsks[i] = 1000000
                    self.buyBids[i] = .001

        elif self.name == 'coinjar':
            for i, coin in enumerate(settings.Coins):
                response = requests.get("https://api.coinjar.com/v3/exchange_rates.json")
                datacoin = response.json()

                try:
                    temp = datacoin['exchange_rates'][coin + self.nativeCurrency]
                    self.sellAsks[i] = float(temp['ask'])
                    self.buyBids[i] = float(temp['bid'])
                    self.successfullyLoaded[i] = 1
                except:
                    self.sellAsks[i] = 1000000
                    self.buyBids[i] = .001

        else:
            print('Exchange not found')