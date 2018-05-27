from bs4 import BeautifulSoup
import cfscrape
import re


class coinspotscrape:
    def __init__(self):

        coins = ['Bitcoin', 'Ethereum', 'Cash', 'Litecoin', 'Omise', 'TRON']
        self.coins = ['BTC', 'ETH', 'BCH', 'LTC', 'OMG', 'TRX']

        scraper = cfscrape.CloudflareScraper()  # Coinspot uses cloudflare

        page = scraper.get("https://www.coinspot.com.au/tradecoins")
        soup = BeautifulSoup(page.content, 'html.parser')
        listgroup = soup.find_all('div', class_='col-md-12')
        fulllist = soup.find_all('li', class_="hidden-xs hidden-sm list-group-item tradeitem")
        pricelist = soup.find_all('div', class_="col-sm-2")

        foundcoin = [0] * len(coins)
        buyPrice = [0] * len(coins)
        sellPrice = [0] * len(coins)
        for i, element in enumerate(pricelist):
            for j, coin in enumerate(coins):
                if coin in element.get_text() and foundcoin[j] is 0:
                    print('\nFOUND: ' + coin)
                    print(pricelist[i + 1].get_text())
                    print(pricelist[i + 2].get_text())
                    tempe = re.findall(r"[-+]?\d*\.\d+|\d+", pricelist[i + 1].get_text())
                    buyPrice[j] = float(tempe[0])
                    tempe = re.findall(r"[-+]?\d*\.\d+|\d+", pricelist[i + 2].get_text())
                    sellPrice[j] = float(tempe[0])
                    foundcoin[j] = 1
        self.buyPrice = buyPrice
        self.sellPrice = sellPrice
        print(self.buyPrice)

    def bid(self, coinreq):
        for i, coin in enumerate(self.coins):
            if coin == coinreq:
                return self.buyPrice[i]

    def ask(self, coinreq):
        for i, coin in enumerate(self.coins):
            if coin == coinreq:
                return self.sellPrice[i]


                # Debugging help
                # i = 0
                # for i in range (0,10):
                #     for coin in coins:
                #         if fulllist[i].get_text().find(coin):
                #             print('Found: ' + coin)
                #             print(fulllist[i].get_text())
