# coinspotscrape.py | A web scraper to get prices from coinspot

from bs4 import BeautifulSoup
import cfscrape



class coinspotscrape:
    def __init__(self):

        coins = ['Bitcoin', 'Ethereum', 'Cash', 'Litecoin', 'Omise', 'TRON']
        self.coins = ['BTC', 'ETH', 'BCH', 'LTC', 'OMG', 'TRX']

        scraper = cfscrape.CloudflareScraper()  # Coinspot uses cloudflare

        page = scraper.get("https://www.coinspot.com.au/tradecoins")
        soup = BeautifulSoup(page.content, 'html.parser')
        pricelist = soup.find_all('tr', class_="tradeitem showrow")

        foundcoin = [0] * len(coins)
        buyPrice = [0] * len(coins)
        sellPrice = [0] * len(coins)
        for i, element in enumerate(pricelist):
            for j, coin in enumerate(coins):
                if coin in element.get_text() and foundcoin[j] is 0:
                    print('\nFOUND: ' + coin)
                    table_elements = element.find_all('td')
                    buyPrice[j] = float(table_elements[1].attrs['data-value'])
                    sellPrice[j] = float(table_elements[2].attrs['data-value'])
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
