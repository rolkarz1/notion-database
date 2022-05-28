import requests
import json
import difflib
import os

def GetLatestCoins():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    params = {
        'limit': '5000'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': os.getenv('CMC_PRO_API_KEY'),
        'Accept-Encoding': 'deflate, gzip'
    }

    response = requests.request('GET', url=url, headers=headers, params=params)

    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )

    data = response.json()['data']
    return [{'name': item['name'], 'symbol': item['symbol'], 'id': item['id'],
             'market_cap': item['quote']['USD']['market_cap']} for item in data]


def GetCoinID(data, coin_name):
    coin_names = [item.get('name') for item in data]
    result = difflib.get_close_matches(coin_name, coin_names, n=1, cutoff=0.6)

    if not result:
        raise ValueError("Coin not found")

    for item in data:
        if item.get('name') == result[0]:
            return item.get('id')


def GetCommunities(coin_id):
    url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/info'
    parameters = {
        'id': coin_id
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': os.getenv('CMC_SECRET'),
        'Accept-Encoding': 'deflate, gzip'
    }
    response = requests.request('GET', url=url, params=parameters, headers=headers)

    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )

    data = json.loads(response.text)

    return {'profile_image_url': data['data'][str(coin_id)]['logo'],
            'website': data['data'][str(coin_id)]['urls']['website'][0],
            'twitter': data['data'][str(coin_id)]['urls']['twitter'][0],
            'discord': data['data'][str(coin_id)]['urls']['chat'][0],
            'telegram': data['data'][str(coin_id)]['urls']['chat'][1]}


def GetMarketData(coin_name):

    data = GetLatestCoins()
    coin_id = GetCoinID(data, coin_name=coin_name)
    communities = GetCommunities(coin_id)

    for item in data:
        if item.get('id') == coin_id:
            return {'name': item['name'],
                    'symbol': item['symbol'],
                    'id': item['id'],
                    'market_cap': int(item['market_cap']),
                    'profile_image_url': communities['profile_image_url'],
                    'website': communities['website'],
                    'twitter': communities['twitter'],
                    'discord': communities['discord'],
                    'telegram': communities['telegram']}
    return 'N/A'


