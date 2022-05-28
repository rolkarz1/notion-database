import requests


def fetchDiscordMembers(invite_url):
    invite_url = invite_url.split('invite/')[-1]

    url = f'https://discord.com/api/v9/invites/{invite_url}'

    params = {'with_counts': 'True',
              'with_expiration': 'True'
              }

    response = requests.request('GET', url=url, params=params)

    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )

    return response.json()['approximate_member_count']

