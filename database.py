#database.py
import time
import re
import numpy as np
import statistics
# import scipy.stats
import settings


Path = str(settings.PATH)

class database:

    def __init__(self):
        pass



    def save_prices(self, marketNames, buyPrices, sellPrices, coin):
        f = open(Path + '\database\prices' + coin, 'a+')
        databasetext = time.strftime('%X %x %Z') + '\t'
        for i, market in enumerate(marketNames):
         databasetext += str(buyPrices[i]) + '\t' + str(sellPrices[i]) + '\t'

        f.write(databasetext + '\n')
        f.close()

    # saves the maximum arb to the database
    def save_arb(self, margin):
        f = open(Path + '\database\\arbdata', 'a+')
        text = str(time.time()) + '\t' + str(margin)
        f.write(text + '\n')
        f.close()

    #Calculates the probability of an arb occurring given a moving average
    def get_moving_average_threshold(self, timeP=60*60*24,probability=1/(60*24)):
        f = open(Path + '\database\\arbdata', 'r')
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
    def create(self, name, marketNames, coin):
     f = open(Path + '\database\\' + name + coin, 'w+')
     text = time.strftime('%X %x %Z') + '\t'
     for i, market in enumerate(marketNames):
         text += marketNames[i] + '\t' + marketNames[i] + '\t'
     f.write(text + '\n')
     f.close()
