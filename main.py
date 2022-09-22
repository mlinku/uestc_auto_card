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
    requests.post(url=url, headers=headers, json=body)


if __name__ == '__main__':
    username = os.environ.get("USERNAME")
    password = os.environ.get("PASSWORD")
    token = os.environ.get("TOKEN")
    uids = os.environ.get("UIDS")
    if len(username)!=0 and len(password) !=0:
        autoCard = autoCard(username, password)
        msg = autoCard.run()
        if len(token)!=0 and len(uids) !=0:
            wx_push(msg, token, uids)

