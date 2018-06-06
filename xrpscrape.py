from bs4 import BeautifulSoup
from prettytable import PrettyTable
import requests
import urllib
import re


def findPrice(exchangeName, marketname, goodstuff):
    indi = 0
    found = 0
    foundExchange = 0
    for line in goodstuff.split('\n'):
        indi = indi + 1
        if foundExchange == 1:
            if marketname in line:
                indi = 0
                found = 1
            foundExchange = 0
        if exchangeName in line:
            foundExchange = 1

        if found == 1 and indi == 8:
            tempe = re.findall(r"[-+]?\d*\.\d+|\d+", line)
            price = float(tempe[0])


    return (price)


class xrpscrape:

    def __init__(self):
        url = 'https://coinmarketcap.com/currencies/ripple/#markets'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

        marketName = []
        exchangeName = []
        exchangeName.append("Gatehub")
        exchangeName.append("Gatehub")
        exchangeName.append("Bittrex")
        exchangeName.append("BTC Markets")
        marketName.append("XRP/USD")
        marketName.append("XRP/BTC")
        marketName.append("XRP/BTC")
        marketName.append("XRP/AUD")

        try:
            result = requests.get(url, headers=headers)
        except urllib.error.HTTPError as e:
            print(e.code)
            print(e.read())
        # print(result.content.decode())
        thetext = result.content.decode()

        soup = BeautifulSoup(thetext, 'html.parser')
        soup.prettify()
        goodstuff = soup.get_text()

        marketPrice = []
        for i, market in enumerate(marketName):
            print(market)
            marketPrice.append(findPrice(exchangeName[i],market, goodstuff))

        if len(marketPrice) != 4:
            h = 1

        self.names = []
        for i , m in enumerate(marketName):
            self.names.append(exchangeName[i] + m)
        self.prices = marketPrice

    def totext(self):
        msg = ''
        msg = msg + '\n--------XRP ARBITRAGES--------\n'
        tab = PrettyTable(['Market', 'Price'])
        for i in range(0, 4):
            tab.add_row([str(self.names[i]), str(self.prices[i])])
        msg = msg + tab.__str__()
        return msg

    def arbAvailable(self):
        for i in range(0, 3):
            if self.prices[i] * 1.15 < self.prices[3]:
                return 1

        return 0
