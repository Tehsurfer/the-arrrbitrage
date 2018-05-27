import re
from ExchangeRates import ExchangeRates
import settings

path = str(settings.PATH)


class RateReader:
    def __init__(self):
        filename = "ExchangeRateInput.txt"
        inputfile = open(path + filename, 'r')

        # input is in the following order
        # RUN:
        # AUDUSD:
        # AUDGBP:
        # AUDEUR:
        # WAITTIME:
        self.results = [0, 0, 0, 0, 60]
        self.tags = ['RUN', 'AUDUSD', 'AUDGBP', 'AUDEUR', 'WAITTIME']

        j = -1

        # Gather input from input.txt and put in matrix
        for count, line in enumerate(inputfile):

            if count < 4:
                do = 0
            else:
                for i, tag in enumerate(self.tags):
                    if tag in line:
                        temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                        if temp is not None and temp != []:
                            self.results[i] = float(temp[0])


class parameterReader:
    def __init__(self):
        self.textThreshold = 0.02
        filename = 'parameters.txt'
        f = open(path + filename, 'r')
        parameterthisline = 0
        for count, line in enumerate(f):
            if parameterthisline:
                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                if temp is not None and temp != []:
                    self.textThreshold = float(temp[0]) / 100

            if 'tk' in line:
                parameterthisline = 1


class fundReader:
    def __init__(self):
        filename = "input.txt"
        coins = ['BTC', 'ETH', 'BCH', 'LTC']
        self.EXCHANGES = 8
        self.CURRENCIES = 9
        inputfile = open(path + filename, 'r')
        j = -1
        self.tags = ['BTC', 'ETH', 'LTC', 'BCH', 'AUD', 'NZD', 'USD', 'GBP', 'EUR']
        self.markets = ['ACX.io   ', 'BTC Mrkts', 'Independent Rsrv', 'Cryptopia', 'Coinspot', 'Bitfinex', 'Coinfloor',
                        'KrakenUSD', 'Bittrex\t']
        self.A = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.Aaud = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0]]

        #  A is as follows: (m currencies, n exchanges)
        #       acx.io | btcmarkets | indreserve | cryptopia | bitfinex | coinfloor | kraken | bittrex
        #   BTC
        #   ETH
        #   LTC
        #   BCH
        #   AUD
        #   NZD
        #   USD
        #   GBP
        #   EUR


        # Gather input from input.txt and put in matrix A
        for count, line in enumerate(inputfile):

            if count < 4:
                do = 0
            else:
                for i, tag in enumerate(self.tags):
                    if tag in line:
                        temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                        if temp is not None and temp != []:
                            self.A[i][j] = float(temp[0])

                if 'tk' in line:
                    j += 1
                    print(self.tags[j])

        # Convert Matrix to AUD
        ex = ExchangeRates()
        for i in range(0, self.CURRENCIES):
            for j in range(0, self.EXCHANGES):
                if self.tags[i] != 'AUD' and self.A[i][j] is not None:
                    self.Aaud[i][j] = float(self.A[i][j]) * float(ex.exchangeRateToAUD(self.tags[i]))

    def print(self):
        # print A
        for i in range(0, self.CURRENCIES):
            msg = ''
            for j in range(0, self.CURRENCIES):
                msg = msg + str(self.A[i][j]) + ' '
            print(msg)

    def fundsOf(self, tag, marketname):
        output = 0
        for i, tag2 in enumerate(self.tags):
            for j, name in enumerate(self.markets):
                if tag == tag2 and marketname == name:
                    output = self.A[i][j]

        return output

    def fundsInAUD(self, tag, marketname):
        output = 0
        for i, tag2 in enumerate(self.tags):
            for j, name in enumerate(self.markets):
                if tag == tag2 and marketname == name:
                    output = self.Aaud[i][j]

        return output
