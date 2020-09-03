#database.py | Saves the found arbitrage margins to files.
# This should ideally be done in a SQL style database but I never got around to implementing it
import time
import re
import statistics
import settings
import json


Path = settings.PATH

class database:

    def __init__(self):
        self.table_dict = self.get_template()


    def save_table(self, marketNames, profits, coin):

        #Adjust our template table
        for i, market1 in enumerate(marketNames):
            for j,  market2 in enumerate(marketNames):
                self.table_dict['margin'][coin][market1][market2] = round(profits[i,j]/settings.FLOW*100,2)

    def save_prices(self, marketNames, buyPrices, sellPrices, coin):
        f = open(Path / 'database\prices' / coin, 'a+')
        databasetext = time.strftime('%X %x %Z') + '\t'
        for i, market in enumerate(marketNames):
         databasetext += str(buyPrices[i]) + '\t' + str(sellPrices[i]) + '\t'

        f.write(databasetext + '\n')
        f.close()

    # saves the maximum arb to the database
    def save_arb(self, margin):
        f = open(Path / 'database\\arbdata', 'a+')
        text = str(time.time()) + '\t' + str(margin)
        f.write(text + '\n')
        f.close()

        with open(Path / 'database\profit_recordings.json', 'a+') as f2:
            f2.write(json.dumps(self.table_dict, indent=4, sort_keys=False))


    #Calculates the probability of an arb occurring given a moving average
    def get_moving_average_threshold(self, timeP=60*60*24,probability=1/(60*24)):
        f = open(Path / 'database\\arbdata', 'r')
        arblist = []
        for line in f.readlines():
            readNumbers = re.findall(r"[-+]?\d*\.\d+|\d+", line)
            moment = float(readNumbers[0])
            arb = float(readNumbers[1])
            if moment > (time.time()-timeP):
                arblist.append(arb)

        sd = statistics.stdev(arblist)
        mean = statistics.mean(arblist)

        # stdamount = scipy.stats.norm.ppf(1-probability)
        stdamount = 5
        thresholdValue = mean + sd*stdamount
        print(arblist)
        print(probability)
        print(sd)
        print(mean)
        print(stdamount)
        print('Threshold value is: ' + str(thresholdValue))
        return thresholdValue

    # WARNING, this will overate any existing database file with the same name
    def create_database(self, name, marketNames, coin):
        f = open(Path / str('database\\' + name + coin), 'w+')
        text = time.strftime('%X %x %Z') + '\t'
        for i, market in enumerate(marketNames):
            text += marketNames[i] + '\t' + marketNames[i] + '\t'
        f.write(text + '\n')
        f.close()

    def get_template(self):
        with open('template.json', 'r') as f:
            return json.load(f)
