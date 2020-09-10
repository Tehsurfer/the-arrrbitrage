# AritrageMain.py is the main thread path to execute all necessary features of the arbitrage
import settings
import sys
import time
import database
from display import text_display
from ExchangeRates import ExchangeRates
from PlaceChecker import PlaceChecker
import numpy as np
from arbFunctions import to_AUD
from save_files import save_files
from Exchange import Exchange, ccxtApproved, scraped
from json_export import ExportAPI
import json



class ArbMain:
    def __init__(self):
        self.html = 'First run in progress. Check back in one minute'
        self.margin_table = 'First run in progress. Check back in one minute'
        self.margin_table_depth = 'First run in progress. Check back in one minute'
        self.json_export = json.dumps({
            'last_run': 0,
            'results': {}
        })

    def start(self):
        # create local versions of global variables (all accessible in settings.py)
        WAITTIME = settings.RUNTIME
        ALERTTHRESH = settings.ALERTTHRESH
        FLOW = settings.FLOW
        CURRENCYEXCHANGEFEE = settings.CURRENCYEXCHANGEFEE
        CURRENCYEXCHANGEFLATFEE = settings.CURRENCYEXCHANGEFLATFEE
        Coins = settings.Coins
        Fiats = settings.Fiats
        ExchangeNames = settings.ExchangeNames
        Native = settings.Native
        TradeFees = settings.TradeFees
        DepositFees = settings.DepositFees
        CryptoWithdrawalRate = settings.CryptoWithdrawalRate
        WFIATFees = settings.FiatWithdrawalFees


        # Compose list of exchanges of interest (scraped exchanges and then ccxt exchanges)
        exchanges = []
        exchanges.append(scraped('coinspot', 'AUD', ))
        exchanges.append(scraped('coinspot nominal', 'AUD', ))
        exchanges.append(scraped('coinjar', 'AUD', ))
        print(len(ExchangeNames))
        print(len(Native))
        for i in range(3, len(ExchangeNames)):
            exchanges.append(ccxtApproved(ExchangeNames[i], Native[i]))
        for i, exchange in enumerate(exchanges):
            exchange.displayName = settings.DisplayNames[i]

        # initialise database
        data_base = database.database()

        rts = ExchangeRates()
        for runNumber in range(0, 1000000):

            program_start = time.time()

            # initialise display strings
            display = text_display()

            # intialise json export:
            json_export = ExportAPI()

            print('Loading Exchange rates...')
            if runNumber % 60 == 0:
                rts.update()
            # Turn withdrawal rates into flat fees based off of current price
            CryptoWithdrawalFees = []
            for rate in CryptoWithdrawalRate: CryptoWithdrawalFees.append(rate * rts.exchangeRateToAUD('BTC'))

            print('Updating exchange prices')
            for exchange in exchanges:
                exchange.update()

            maxArb = [0] * len(Coins)
            # Loop through all exchanges for each coin of interest starting here
            for i_coin, coin in enumerate(Coins):

                SellAsks = []
                BuyBids = []
                ValidNames = []
                NativeBuy = []
                NativeSell = []

                for exchange in exchanges:
                    if exchange.successfullyLoaded[i_coin]:
                        if exchange.sellAsks[i_coin] is not None and exchange.sellAsks[i_coin] != 0:
                            ValidNames.append(exchange.displayName)
                            SellAsks.append(exchange.sellAsks[i_coin])
                            BuyBids.append(exchange.buyBids[i_coin])

                print(f'sell asks: {SellAsks}')

                # Market Summary
                display.add_native_prices_table(ValidNames, SellAsks, BuyBids, coin)

                # Calculate amount of cryptocurrency you get for 10,000 AUD by getting prices from Bittrex
                coinsBought = FLOW * rts.USD / BuyBids[0]

                # check for depth of the markets (10,000 AUD)
                SellAsks = []
                BuyBids = []
                SellAsksNoDepth = []
                BuyBidsNoDepth = []
                depthpricebuys = []
                depthpricesells = []
                for i, exchange in enumerate(exchanges):
                    if exchange.displayName not in ValidNames:
                        continue
                    if settings.OrderBookNeeded[i] == 1:
                        depthpricebuy = exchange.order_book_buy(coin, coinsBought)
                        depthpricesell = exchange.order_book_sell(coin, coinsBought)
                        depthpricesells.append(depthpricesell)
                        depthpricebuys.append(depthpricebuy)
                    else:
                        depthpricebuys.append(exchange.buyBids[i_coin])
                        depthpricesells.append(exchange.sellAsks[i_coin])

                    # Convert Prices to a single currency (AUD)
                    BuyBids.append(to_AUD(exchange.nativeCurrency,depthpricebuys[-1], rts))
                    SellAsks.append(to_AUD(exchange.nativeCurrency,depthpricesells[-1], rts))
                    SellAsksNoDepth.append(to_AUD(exchange.nativeCurrency,exchange.sellAsks[i_coin], rts))
                    BuyBidsNoDepth.append(to_AUD(exchange.nativeCurrency, exchange.buyBids[i_coin], rts))

                # Add prices in AUD to the display
                display.add_market_prices_table(ValidNames, BuyBids, SellAsks, coin)

                # Search all the Exchanges for margins
                marginsNoDepth = []
                margins = np.zeros(shape=(len(ValidNames), len(ValidNames)))
                margins_no_depth = np.zeros(shape=(len(ValidNames), len(ValidNames)))
                profits = np.zeros(shape=(len(ValidNames), len(ValidNames)))
                profits_no_depth = np.zeros(shape=(len(ValidNames), len(ValidNames)))
                for i in range(0, len(ValidNames)):
                    for j in range(0, len(ValidNames)):
                        # Calculating change
                        margin = (BuyBids[j] - SellAsks[i]) / SellAsks[i]
                        # Calculating price
                        margin = margin - TradeFees[i] - TradeFees[j]
                        # Calculate price with all relevant fees
                        profit = FLOW * margin - CryptoWithdrawalFees[i] - WFIATFees[
                            j] - CURRENCYEXCHANGEFEE * FLOW - CURRENCYEXCHANGEFLATFEE
                        profits[i, j] = profit
                        margins[i, j] = profit / FLOW

                        # Calculate again without depth
                        margin_no_depth = (BuyBidsNoDepth[j] - SellAsksNoDepth[i]) / SellAsksNoDepth[i]
                        profit_no_depth_with_fees = FLOW * margin_no_depth - CryptoWithdrawalFees[i] - WFIATFees[
                            j] - CURRENCYEXCHANGEFEE * FLOW - CURRENCYEXCHANGEFLATFEE
                        margin_no_depth_with_fees = profit_no_depth_with_fees / FLOW
                        profits_no_depth[i, j] = profit_no_depth_with_fees
                        margins_no_depth[i, j] = margin_no_depth_with_fees

                # Write profits and margins into a displayable format
                display.margin_list(ValidNames, BuyBids, SellAsks, margins, coin)
                display.profit_list(ValidNames, BuyBids, SellAsks, profits, coin)
                display.depth_table(margins.flatten(),ValidNames,len(ValidNames),coin)
                display.no_depth_table(margins_no_depth.flatten(),ValidNames,len(ValidNames),coin)

                # Update api json outputs:
                json_export.update_results(coin, margins, ValidNames)

                # Check for margins worthy of an email alert
                display.alerts(ValidNames, BuyBids, SellAsks, margins, coin, ALERTTHRESH)

                # save prices to the database
                #data_base.save_prices(ValidNames, BuyBids, SellAsks, coin)
                #data_base.save_table(ValidNames, profits, coin)

                maxArb[i_coin] = margins.max()
                print(display.stringOutput)

            # Add exchange rates for visualising
            display.stringOutput += rts.totext()

            # update database and server
            g = save_files()
            g.update_data(display.stringOutput, display.marginNoDepth, display.marginWithDepth)
            g.update_templates()

            self.html = f'<pre>{display.stringOutput}</pre>'
            self.margin_table = display.marginNoDepth
            self.margin_table_depth = display.marginWithDepth
            self.json_export = json_export.export()

            # place an alert to confirm program has run with no errors
            PlaceChecker()

            program_finish = time.time()
            run_time = round(program_finish - program_start)
            print('program ran succesfuly at' + time.strftime('%X %x %Z'))
            print('progran took a total of: ' + str(run_time) + 's to run')
            sys.stdout.flush()
            time.sleep(1)

            if run_time < WAITTIME:
                print('Waiting ' + str(WAITTIME - run_time) + 'seconds before running again to meet the run every ' + str(
                    WAITTIME) + ' seconds requirement')
                time.sleep(WAITTIME - run_time - 1)
            else:
                print('Starting Arrrbitrage again...')



if __name__ == "__main__":
    ArbMain()
