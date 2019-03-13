# AritrageMain.py is the main thread path to execute all necessary features of the arbitrage
import settings
import time
import database
from display import text_display
from ExchangeRates import ExchangeRates
from PlaceChecker import PlaceChecker
from xrpscrape import xrpscrape
import numpy as np
from arbFunctions import sendemails, updateDropbox, to_AUD
from git_hub import git_hub
# from git_hub2 import git_hub2
from Exchange import Exchange, ccxtApproved, scraped




def main():
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

    for runNumber in range(0, 1000000):

        program_start = time.time()

        # initialise display strings
        display = text_display()

        print('Loading Exchange rates...')
        rts = ExchangeRates()

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
                    ValidNames.append(exchange.displayName)
                    SellAsks.append(exchange.sellAsks[i_coin])
                    BuyBids.append(exchange.buyBids[i_coin])

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
                    depthpricebuy = exchange.order_book_sell(coin, coinsBought)
                    depthpricesell = exchange.order_book_buy(coin, coinsBought)
                    depthpricesells.append(depthpricesell)
                    depthpricebuys.append(depthpricebuy)
                    # fileStr += ValidNames[i] + '  \t|\t' + str(round(depthpricebuy, 0)) + '  \t|\t' + str(
                    #     round(depthpricesell, 0)) + '\n'
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

            profits = np.zeros(shape=(len(ValidNames), len(ValidNames)))
            for i in range(0, len(ValidNames)):
                for j in range(0, len(ValidNames)):
                    # Calculating change
                    margin = (BuyBids[j] - SellAsks[i]) / SellAsks[i]
                    # Calculating price
                    margin = margin - TradeFees[i] - TradeFees[j]
                    margins[i, j] = margin
                    # Calculate price with all relevant fees
                    profit = FLOW * margin - CryptoWithdrawalFees[i] - WFIATFees[
                        j] - CURRENCYEXCHANGEFEE * FLOW - CURRENCYEXCHANGEFLATFEE
                    profits[i, j] = profit

                    marginsNoDepth.append((BuyBids[j] - SellAsks[i]) / SellAsks[i])

            # Write profits and margins into a displayable format
            display.margin_list(ValidNames, BuyBids, SellAsks, margins, coin)
            display.profit_list(ValidNames, BuyBids, SellAsks, profits, coin)
            display.profit_table(profits.flatten(),ValidNames,len(ValidNames),coin)
            display.margin_table(marginsNoDepth,ValidNames,len(ValidNames),coin)

            # Check for margins worthy of an email alert
            display.alerts(ValidNames, BuyBids, SellAsks, margins, coin, ALERTTHRESH)

            # save prices to the database
            data_base.save_prices(ValidNames, BuyBids, SellAsks, coin)
            data_base.save_table(ValidNames, profits, coin)

            maxArb[i_coin] = margins.max()
            print(display.stringOutput)

        data_base.save_arb(max(maxArb))

        # Check XRP for arbitrage opportunities
        # xrp = xrpscrape()
        # display.stringOutput += xrp.totext()
        # if xrp.arbAvailable():
        #     display.alertsOutput += xrp.totext()
        #     display.stringOutput += xrp.totext()
        #     display.htmlOutput += xrp.totext()

        # Add exchange rates for visualising
        display.stringOutput += rts.totext()

        #send email alerts if valuable arbs pop up
        # sendemails(display.stringOutput, display.alertsOutput, runNumber, xrp, max(maxArb))

        #update the dropbox display and
        updateDropbox(display.stringOutput, display.htmlOutput, display.htmlOutput2)
        time.sleep(2)

        # update javascript display every 3 minutes.
        # if runNumber % 3 == 0:
        #     data_base.javascript_arb_array()
        #     g2 = git_hub2()
        #     g2.update()

        # update github
        g = git_hub()
        g.update()

        # place an alert to confirm program has run with no errors
        PlaceChecker()

        program_finish = time.time()
        run_time = round(program_finish - program_start)
        print('program ran succesfuly at' + time.strftime('%X %x %Z'))
        print('progran took a total of: ' + str(run_time) + 's to run')
        time.sleep(1)

        if run_time < WAITTIME:
            print('Waiting ' + str(WAITTIME - run_time) + 'seconds before running again to meet the run every ' + str(
                WAITTIME) + ' seconds requirement')
            time.sleep(WAITTIME - run_time - 1)
        else:
            print('Starting Arrrbitrage again...')



if __name__ == "__main__":
    main()
