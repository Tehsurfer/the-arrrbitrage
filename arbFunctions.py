#arbFunctions.py is various input functions that did not fit in the main thread but did not seem worthy of their own class
import smtplib
import time
from database import database
import settings

Path = str(settings.PATH)

#Sends emails to those who want alerts
def sendemails(fileStr, fileStrAlert, kt, xrp, maxArb):
    if fileStr != '' and kt % 60 == 1:
        print(fileStr)
        fileStr = '\n' + fileStr
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("jessekhora@gmail.com", "fackE3$news45")
        server.sendmail("jessekhora@gmail.com", "nametaken47@gmail.com", fileStr)
        server.sendmail("jessekhora@gmail.com", "klamboghini86@gmail.com", fileStr)
        server.quit()

    dat = database()

    if (maxArb >= dat.get_moving_average_threshold() and maxArb >= .7):
        print(fileStrAlert)
        fileStrAlert = '\n Arrrbitrage alert! \n' + fileStrAlert + '\n Check full details at... https://www.dropbox.com/s/uj6274l0m1jmxds/index.txt?dl=0'
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("jessekhora@gmail.com", "fackE3$news45")
        server.sendmail("jessekhora@gmail.com", "jessekhorasanee@gmail.com", fileStrAlert)
        server.sendmail("jessekhora@gmail.com", "dimitri@roumpos.com", fileStrAlert)
        # server.sendmail("jessekhora@gmail.com", "b.sceats@gmail.com", fileStrAlert)
        server.sendmail("jessekhora@gmail.com", "owen.m.kr@gmail.com", fileStrAlert)
        server.quit()


#updates the dropbox files for web display
def updateDropbox(fileStr, html='',html2=''):


    # Change path to reflect file location
    f = open('ArbitrageResults.txt', 'w')

    f.write(fileStr)
    f.close()
    # Update files

    contents = open('ArbitrageResults.txt', "r")
    g = open(Path + "\index.html", "w")
    html_text = '{{ partial "head" . }} {{ partial "nav" . }} <pre>' + fileStr + '</pre>'

    g.write(html_text)

    contents = open('ArbitrageResults.txt', "r")
    with open(Path + "\index.txt", "w") as yo:
        for lines in contents.readlines():
            yo.write(lines)

    f = open(Path + '\margin_table_with_depth.html', 'w')
    f.write(html)
    f.close()

    h = open(Path + '\margin_table.html', 'w')
    h.write(html2)
    h.close()


def save_prices_to_database(marketNames, buyPrices, sellPrices, coin):
    f = open(Path + '\database\prices' + coin, 'a+')
    databasetext = time.strftime('%X %x %Z') + '\t'
    for i, market in enumerate(marketNames):
        databasetext += str(buyPrices[i]) + '\t' + str(sellPrices[i]) + '\t'

    f.write(databasetext + '\n')
    f.close()


def save_arb_to_database(margin):
    f = open(Path + '\database\\arbdata', 'a+')
    text = str(time.time()) + '\t' + str(margin)
    f.write(text + '\n')
    f.close()

# collects the moving average from the database
def get_moving_average(timePeriod):
    f = open(Path + '\database\\arbdata', 'r')
    for line in f.readlines():
        g = 2


def create_database(marketNames, coin):
    f = open(Path + '\database\prices' + coin, 'w+')
    text = time.strftime('%X %x %Z') + '\t'
    for i, market in enumerate(marketNames):
        text += marketNames[i] + '\t' + marketNames[i] + '\t'
    f.write(text + '\n')
    f.close()

# The next five functions are used to organise a table of data into a format for display in html
def row_major(alist, sublen):
    return [alist[i:i + sublen] for i in range(0, len(alist), sublen)]


def col_major(alist, sublen):
    numrows = (len(alist) + sublen - 1) // sublen
    return [alist[i::sublen] for i in range(numrows)]


def html_table_basic(lol):
    text = '<table border="1">'
    for sublist in lol:
        text += '  <tr><td style ="background-color:rgb(102,255,102);">'
        text += '    </td><td style ="background-color:rgb(102,255,102);">'.join(sublist)
        text += '  </td></tr>'
    text += '</table>'
    return text


def html_table(lol, header):
    bestcolor = [0, 255, 0]
    worstcolor = [0, 26, 77]
    negativecolor = [147, 31, 31]

    text = '<table border="1">'
    text += '  <tr><th>+</th>'
    for head in header:
        text += '  <th>' + head + '</th>'
    text += '  </tr>'
    for k, sublist in enumerate(lol):
        text += '  <tr><th>' + header[k] + '</th>'
        for j, percentage in enumerate(sublist):
            color = [0, 0, 0]
            for i, col in enumerate(bestcolor):
                if percentage <= 0:
                    color[i] = negativecolor[i]
                else:
                    color[i] = bestcolor[i] * (percentage + .8) / 4 + worstcolor[i] * (1 - (percentage + .8) / 4)
                    color[i] = int(round(color[i], 0))
            print(color)
            text += '    <td style ="background-color:rgb(' + str(color[0]) + ' ,' + str(color[1]) + \
                    ', ' + str(color[2]) + ');">' + str(percentage)
        text += '  <th>' + header[k] + '</th></tr>'
    text += '  <tr><th>+</th>'
    for head in header:
        text += '  <th>' + head + '</th>'
    text += '  </tr>'

    text += '</table>'
    return text


def html_table2(lol, header, header2):
    bestcolor = [230, 255, 230]
    worstcolor = [0, 26, 77]
    negativecolor = [147, 31, 31]

    text = '<table border="1">'
    text += '  <tr><th>+</th>'
    for head in header:
        text += '  <th>' + head + '</th>'
    text += '  </tr>'
    for k, sublist in enumerate(lol):
        text += '  <tr><th>' + header2[k] + '</th>'
        for j, percentage in enumerate(sublist):
            color = bestcolor
            print(color)
            text += '    <td style ="background-color:rgb(' + str(color[0]) + ' ,' + str(color[1]) + \
                    ', ' + str(color[2]) + ');">' + str(percentage)
        text += '  <th>' + header2[k] + '</th></tr>'
    text += '  <tr><th>+</th>'
    for head in header:
        text += '  <th>' + head + '</th>'
    text += '  </tr>'

    text += '</table>'
    return text


def list_to_html_table(alist, header, sublength, color=True, header2=[], column_major=False):
    if column_major:
        lol = col_major(alist, sublength)
    else:
        lol = row_major(alist, sublength)
    if color:
        return ''.join(html_table(lol, header))
    else:
        return ''.join(html_table2(lol, header, header2))


def to_AUD(native, price, rts):
    if 'USD' in native:
        return (price / rts.USD)
    elif 'GBP' in native:
        return (price / rts.GBP)
    else:
        return price

