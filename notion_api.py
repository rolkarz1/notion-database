import json
import requests
import os


def createPage(response):
    url = 'https://api.notion.com/v1/pages'
    token = os.getenv('NOTION_SECRET')

    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json',
        'Notion-Version': '2022-02-22'
    }

    body = {
        "parent": {"database_id": os.getenv('NOTION_DATABASE')},
        "icon": {
            'type': 'external',
            'external': {
                'url': response['profile_image_url']
            }
        },
        "properties": {
            "Coin": {
                "title": [
                    {
                        "text": {
                            "content": response['name']
                        }
                    }
                ]
            },
            "Market": {
                "select": {
                    "name": "market_name"
                }
            },
            "Network": {
                "select": {
                    "name": "network_name"
                }
            },
            "Market Cap": {
                "number": response['market_cap']
            },
            "Ticker": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": response['ticker']
                        }
                    }
                ]
            },
            "Website": {
                "url": response['website']
            },
            "Twitter": {
                "url": response['twitter']
            },
            "Discord": {
                "url": response['discord']
            },
            "Telegram": {
                "url": response['telegram']
            },
            "Discord members": {
                'number': response['discord_members']
            },
            "Twitter followers": {
                'number': response['twitter_followers']
            },
            "Telegram members": {
                'number': response['telegram_members']
            }
        }
    }

    data = json.dumps(body)
    res = requests.request("POST", url=url, headers=headers, data=data)
    return res.status_code


def FetchDatabase():
    url = f"https://api.notion.com/v1/databases/{os.getenv('NOTION_DATABASE')}/query"

    payload = {"page_size": 100}
    headers = {
        "Accept": "application/json",
        "Notion-Version": "2022-02-22",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('NOTION_SECRET')}"
    }

    response = requests.post(url=url, json=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )

    return response.json()


def SaveDatabase(filename):
    with open(f'./{filename}.json', 'w') as f:
        json.dump(FetchDatabase(), f)


def FetchNewEntries():
    with open('./notion-database.json', 'r') as f:
        current_db = json.load(f)

    new_db = FetchDatabase()

    return [id for id in new_db['results'] if id not in current_db['results']]


def UpdatePage(page_id, response):
    url = f"https://api.notion.com/v1/pages/{page_id}"

    for key in response:
        if response[key] == '':
            response[key] = 'N/A'

    headers = {
        "Accept": "application/json",
        "Notion-Version": "2022-02-22",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('NOTION_SECRET')}"
    }

    body = {
        "icon": {
            'type': 'external',
            'external': {
                'url': response['profile_image_url']
            }
        },
        "properties": {
            "Coin": {
                "title": [
                    {
                        "text": {
                            "content": response['name']
                        }
                    }
                ]
            },
            "Market Cap": {
                "number": response['market_cap']
            },
            "Ticker": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": response['ticker']
                        }
                    }
                ]
            },
            "Website": {
                "url": response['website']
            },
            "Twitter": {
                "url": response['twitter']
            },
            "Discord": {
                "url": response['discord']
            },
            "Telegram": {
                "url": response['telegram']
            },
            "Discord members": {
                "number": response['discord_members']
            },
            "Twitter followers": {
                "number": response['twitter_followers']
            },
            "Telegram members": {
                "number": response['telegram_members']
            }
        }
    }

    response = requests.patch(url=url, headers=headers, data=json.dumps(body))

    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )

    return response.json()


