import requests
import os


def GetMemeberCount(channel_name):
    url = f"https://api.telegram.org/{os.getenv('TELEGRAM_SECRET')}/getChatMemberCount?chat_id=@{channel_name}"

    response = requests.request('GET', url=url)

    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()['result']