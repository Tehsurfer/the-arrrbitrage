#display.py used for changing all information into a human readable format
import time
import arbFunctions
import settings

class text_display:

    def __init__(self):
        self.stringOutput = ''
        self.alertsOutput = ''
        self.htmlOutput = '{{ partial "head" . }} {{ partial "nav" . }} <html><head> <b> Table of margins for a 10k AUD two way trip. We last pillaged the exchanges at:  ' + time.strftime(
            '%X  %d/%m/%y %Z') + ' <br /> </b> </head> '
        self.htmlOutput2 = '{{ partial "head" . }} {{ partial "nav" . }} <html><head> <b> Table of margins for a 10k AUD two way trip. We last pillaged the exchanges at:  ' + time.strftime(
            '%X  %d/%m/%y %Z') + ' <br /> </b> </head> '
        self.header = '{{ partial "head" . }} {{ partial "nav" . }} <html><head> <b> Table of margins for a 10k AUD two way trip. We last pillaged the exchanges at:  ' + time.strftime(
            '%X  %d/%m/%y %Z') + ' <br /> </b> </head> '

    def __add__(self, other):
        self.stringOutput += other

    def add_market_prices_table(self, MarketName, BuyPrice, SellPrice, coin):
        self.stringOutput += coin + ' Market Prices' + '\n'
        self.stringOutput += 'Exchange \t|\t Buy Bids \t|\t Sell Asks ' + '\n'
        for i in range(len(BuyPrice)):
            if (BuyPrice[i] != .001):
                self.stringOutput += MarketName[i] + '\t|\t' + str(round(BuyPrice[i], 3)) + '  \t|\t' + str(
                    round(SellPrice[i], 3)) + '\n'

        self.stringOutput += '--------------------------------------------------------------------\n'

    def add_native_prices_table(self,ValidNames,NativeSell,NativeBuy,coin):

        self.stringOutput += coin + ' Native buy prices (for validation)' + '\n'
        self.stringOutput += 'Exchange \t|\t Buy Price \t|\t SellAsks ' + '\n'
        for i in range(0, len(ValidNames)):
            self.stringOutput +=  ValidNames[i] + '\t|\t' + str(round(NativeBuy[i], 1)) + '  \t|\t' + str(round(NativeSell[i], 1)) + '\n'

        self.stringOutput += '--------------------------------------------------------------------\n'

    def margin_list(self,ValidNames,BuyBids,SellAsks,margins,coin):
        self.stringOutput += '\n\n' + coin + ' MARGIN COMBINATIONS (Trade fees and exchange rates included only)' + '\n'
        self.stringOutput += 'Direction\t\t|\t Margin' + '\n'
        for i in range (0,len(ValidNames)):
            for j in range(0, len(ValidNames)):
                if margins[i,j] > .007:
                    self.stringOutput += ValidNames[i] + ' -> ' + ValidNames[j] + ' \t|\t ' + str(
                        round(margins[i,j] * 100, 1)) + '%' + '\n'
        self.stringOutput += '--------------------------------------------------------------------\n'

    def profit_list(self, ValidNames, BuyBids, SellAsks, profits, coin):
        foundprofit = 0
        self.stringOutput += '\n\n' + coin + ' MARGIN COMBINATIONS for a 10k AUD move (All Fees included for a TWO way trip)' + '\n'
        self.stringOutput += 'Direction\t\t|\t Profit' + '\n'
        for i in range (0,len(ValidNames)):
            for j in range(0, len(ValidNames)):
                if profits[i,j] > 100:
                    foundprofit = 1
                    self.stringOutput += ValidNames[i] + ' -> ' + ValidNames[j] + ' \t|\t ' + str(
                        round(profits[i,j], 2)) + '\n'
        if not foundprofit: self.stringOutput += '--- none :( ---\n\n'


    def alerts(self, ValidNames, BuyBids, SellAsks, margins, coin, ALERTTHRESH):
        tempa = ''
        for i in range(len(ValidNames)):
            for j in range(len(ValidNames)):

                if margins[i, j] > ALERTTHRESH:
                    tempa = tempa + ValidNames[i] + ' -> ' + ValidNames[j] + ' \t|\t ' + str(
                        round(margins[i,j] * 100, 1)) + '%' + '\n'

        if tempa != '':
            self.alertsOutput += '\n' + coin + ' opportunities \n' + tempa
        # Check aussie markets for gap

        self.alertsOutput += '--------------------------------------------------------------------\n'

    def profit_table(self,profitlist, Validnames, sublength, coin):
        profitlist2 = [0]*len(profitlist)
        for i, profit in enumerate(profitlist):
            profitlist2[i] = round(profit/settings.FLOW*100,2)
        self.htmlOutput += '<body> <b> ' + str(coin) + ' </b> </body> '
        self.htmlOutput += arbFunctions.list_to_html_table(profitlist2,Validnames,sublength,color=True)

    def margin_table(self, marginlist, Validnames, sublength, coin):
        marginlist2 = [0] * len(marginlist)
        for i, margin in enumerate(marginlist):
            marginlist2[i] = round(margin*100, 1)
        self.htmlOutput2 += '<body> <b> ' + str(coin) + ' </b> </body> '
        self.htmlOutput2 += arbFunctions.list_to_html_table(marginlist2, Validnames, sublength, color=True)

