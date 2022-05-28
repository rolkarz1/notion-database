import requests


def GetCoinId(coin_name):
    headers = {'accept': 'application/json'}
    params = {'query': coin_name}

    url = 'https://api.coingecko.com/api/v3/search'
    response = requests.request('GET', url=url, headers=headers, params=params).json()

    if not response['coins']:
        raise Exception("NotFound")
    else:
        return response['coins'][0]['id']


def GetCoinData(coin_id):
    headers = {'accept': 'application/json'}
    params = {'localization': 'false',
              'tickers': 'false',
              'market_data': 'true',
              'community_data': 'true',
              'developer_data': 'false',
              'sparkline': 'false'}

    url = f'https://api.coingecko.com/api/v3/coins/{coin_id}'
    response = requests.request('GET', url=url, headers=headers, params=params)

    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )

    response = response.json()
    return {'name': response['name'],
            'ticker': response['symbol'],
            'market_cap': response['market_data']['market_cap']['usd'],
            'website': response['links']['homepage'][0],
            'discord': response['links']['chat_url'][0],
            'twitter': 'https://twitter.com/' + response['links']['twitter_screen_name'],
            'telegram': 'https://t.me/' + response['links']['telegram_channel_identifier'],
            'image': response['image']['thumb']}


