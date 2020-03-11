from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import settings

def get_market():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'symbol': 'BTC,ETH,BCH,LTC',
        'convert': 'AUD'

    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': settings.cm_key,
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        print(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    rates = {}
    coins = ['BTC','ETH','BCH','LTC']
    for coin in coins:
        rates[coin] = data['data'][coin]['quote']['AUD']['price']
    return rates

print(get_market())