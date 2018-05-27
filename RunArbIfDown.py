import time
import settings
import ArbitrageMain

#Time in seconds
DOWNTIME = ArbitrageMain.WAITTIME+1

Path = str(settings.PATH)
for i in range(0,1000000):

    filename = 'check.txt'
    f = open(Path + filename, "r")
    line = f.readline()
    print(line)
    f.close()

    if (time.time() - float(line)) > DOWNTIME :
        print('REBOOTING THE ARBITRAGE')
        try:
            ArbitrageMain.main()
        except:
            print('ARBITRAGE hit an error')
            pass

    else:
        print('ARBITRAGE IS STILL RUNNING')
        print('waiting the following seconds:')
        print(DOWNTIME)
    print('program was checked if running at' + time.strftime('%X %x %Z'))
    time.sleep(DOWNTIME)