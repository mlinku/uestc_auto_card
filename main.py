import os

import requests
import urllib3
from autoCard import autoCard

urllib3.disable_warnings()


def wx_push(msg):
    token = "AT_W1JBkiGuFHrnxY8lyXcJ78Ow4JU6Ukhj"
    url = "http://wxpusher.zjiecode.com/api/send/message"
    body = {
        "appToken": token,
        "content": msg,
        "contentType": 1,
        "uids": [
            "UID_RVzTGvjgi7ERYrt2yfsG7bg825wg"
        ]
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url=url, headers=headers, json=body)
    print(response.text)


if __name__ == '__main__':
    username = os.environ.get("username")
    password = os.environ.get("password")
    autoCard = autoCard(username, password)
    wx_push(autoCard.run())
