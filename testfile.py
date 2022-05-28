from notion_client import AsyncClient
import asyncio
import json
import requests

# notion = AsyncClient(auth='secret_GGzdxacFqXdY9rh4sn1JQQgGtDpei4A9hqlPI4EYvDa')
database_id = 'f7ca1c9f29ce43cfae6ff665aa1d6809'
secret = 'secret_GGzdxacFqXdY9rh4sn1JQQgGtDpei4A9hqlPI4EYvDa'


async def FetchDatabase(database_id, secret):
    url = f"https://api.notion.com/v1/databases/{database_id}/query"

    payload = {"page_size": 100}
    headers = {
        "Accept": "application/json",
        "Notion-Version": "2022-02-22",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {secret}"
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.json()['results']

# with open('./json_data.json', 'w') as f:
#     json.dump(response.json()['results'], f)




