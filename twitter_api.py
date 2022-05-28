import requests
import os


def create_url(profile_url):
    profile_url = profile_url.split('/')[-1]
    return 'https://api.twitter.com/2/users/by/username/{}'.format(profile_url)


def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {os.getenv('TWITTER_SECRET')}"
    r.headers["User-Agent"] = "v2FollowersLookupPython"
    return r


def connect_to_endpoint(url):

    params = {'user.fields': 'profile_image_url,public_metrics,url'}
    response = requests.request("GET", url, auth=bearer_oauth, params=params)

    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )

    return response.json()


def getTwitterParams(response, url):
    return {'name': response['data']['name'],
            'followers_count': response['data']['public_metrics']['followers_count'],
            'profile_image_url': response['data']['profile_image_url'],
            'website': response['data']['url'],
            'twitter': url
            }


def getTwitterInfo(url):
    json_response = connect_to_endpoint(create_url(url))
    return getTwitterParams(json_response, url)
