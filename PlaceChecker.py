#PlaceChecker.py a few file placers for recording when the arbitrage last ran and sent texts
import time
import settings
Path = settings.PATH
def PlaceChecker():
    filename = 'check.txt'
    f = open(Path / filename, "w")
    f.seek(0)
    f.truncate()
    f.write(str(time.time()) + '\n')
    f.close()
def PlaceTextTime():
    filename = 'last_text.txt'
    f = open(Path / filename, "w")
    f.seek(0)
    f.truncate()
    f.write(str(time.time()) + '\n')
    f.close()
def ReadTextTime():
    filename = 'last_text.txt'
    f = open(Path / filename, "r")
    line = f.readline()
    print(line)
    f.close()
    return (float(line))


