import discord_api
import twitter_api
import telegram_api
from discord_api import fetchDiscordMembers
import coingecko_api
import notion_api
import coinmarketcap_api as cmc
from dotenv import load_dotenv
import json


def configure():
    load_dotenv()


def DeleteEmptyRecords(records):
    coins = []
    for record in records:
        try:
            if record['properties']['Coin']['title'][0]['text']['content']:
                coins.append(record)
        except:
            pass

    return coins


def main():
    configure()

    new_records = DeleteEmptyRecords(notion_api.FetchNewEntries())
    coin_id = []
    discord_members = 0
    telegram_members = 0
    twitter_followers = 0

    for record in new_records:
        coin_name = record['properties']['Coin']['title'][0]['text']['content']
        try:
            coin_id.append((coingecko_api.GetCoinId(coin_name), record['id']))
        except:
            print('Not Found')

    for coin in coin_id:
        coin_details = coingecko_api.GetCoinData(coin[0])
        try:
            discord_members = discord_api.fetchDiscordMembers(coin_details['discord'])
        except:
            discord_members = 0
        try:
            twitter_params = twitter_api.getTwitterInfo(coin_details['twitter'])
            twitter_followers = twitter_params['followers_count']
        except:
            pass
        try:
            telegram_members = telegram_api.GetMemeberCount(coin_details['telegram'].split('/')[-1])
        except:
            telegram_members = 0

        response = {'name': coin_details['name'],
                    'ticker': '$' + coin_details['ticker'].upper(),
                    'market_cap': coin_details['market_cap'],
                    'profile_image_url': coin_details['image'],
                    'website': coin_details['website'],
                    'discord': coin_details['discord'],
                    'twitter': coin_details['twitter'],
                    'telegram': coin_details['telegram'],
                    'discord_members': discord_members,
                    'twitter_followers': twitter_followers,
                    'telegram_members': telegram_members}

        notion_api.UpdatePage(page_id=coin[1], response=response)

        notion_api.SaveDatabase('notion-database')



main()

