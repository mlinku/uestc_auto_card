import os
import requests
import urllib3
from autoCard import autoCard

urllib3.disable_warnings()


def wx_push(msg, token, uids):
    url = "http://wxpusher.zjiecode.com/api/send/message"
    body = {
        "appToken": token,
        "content": msg,
        "contentType": 1,
        "uids": [
            uids
        ]
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url=url, headers=headers, json=body)


if __name__ == '__main__':
    username = os.environ.get("USERNAME")
    password = os.environ.get("PASSWORD")
    token = os.environ.get("TOKEN")
    uids = os.environ.get("UIDS")
    if username is not None and password is not None:
        autoCard = autoCard(username, password)
    if token is not None and uids is  not None:
        wx_push(autoCard.run(), token, uids)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!")
