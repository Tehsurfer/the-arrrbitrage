import ccxt
import time
import json
import requests
import config
import coinmarket

#Fetching rates from apifixer.io (free service)

class ExchangeRates:
    def __init__(self):
        self.coins = ['BTC','ETH','BCH','LTC']
        self.coinscurs = ['BTC','ETH','BCH','LTC','NZD','USD','GBP','EUR']
    def update(self):
        currencylayerURL = 'https://www.apilayer.net/api/live'
        payload = {'access_key': config.currencylayerkey,'source':'AUD','currencies':'USD,NZD,GBP,EUR','format':'1'}
        exchangeratesapiURL = 'https://api.exchangeratesapi.io/latest?base=AUD'

        response1 = requests.get(currencylayerURL, params=payload)
        print(response1)
        datarates1 = response1.json()

        rates = coinmarket.get_market()
        print('Rates are :')
        print('AUD->USD: ' + str(datarates1['quotes']['AUDUSD']))
        print('AUD->NZD: ' + str(datarates1['quotes']['AUDNZD']))
        print('AUD->GBP: ' + str(datarates1['quotes']['AUDGBP']))
        print('AUD->EUR: ' + str(datarates1['quotes']['AUDEUR']))
        print('BTC->AUD: ' + str(rates[0]))
        print('ETH->AUD: ' + str(rates[1]))
        print('LTC->AUD: ' + str(rates[3]))
        print('BCH->AUD: ' + str(rates[2]))

        self.USD = datarates1['quotes']['AUDUSD'] 
        self.NZD = datarates1['quotes']['AUDNZD']
        self.GBP = datarates1['quotes']['AUDGBP']
        self.EUR = datarates1['quotes']['AUDEUR']
        self.BTC = rates[0]
        self.ETH = rates[1]
        self.LTC = rates[3]
        self.BCH = rates[2]

    def totext(self):
        text = ''
        text = text + '\n\nRates are :\n'
        text = text + '\nAUD->USD: ' + str(self.USD)
        text = text + '\nAUD->NZD: ' + str(self.NZD)
        text = text + '\nAUD->GBP: ' + str(self.GBP)
        text = text + '\nAUD->EUR: ' + str(self.EUR)
        return text



    def exchangeRateToAUD(self,tag):
        if tag == 'USD': return float(1/self.USD)
        if tag == 'NZD': return float(1/self.NZD)
        if tag == 'GBP': return float(1/self.GBP)
        if tag == 'EUR': return float(1/self.EUR)
        if tag == 'BTC': return float(self.BTC)
        if tag == 'ETH': return float(self.ETH)
        if tag == 'LTC': return float(self.LTC)
        if tag == 'BCH': return float(self.BCH)
        else: return 0
