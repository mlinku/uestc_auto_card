import requests
import urllib3
from autoCard import autoCard

urllib3.disable_warnings()


def weixin_notification(msg):
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


def main_handler(event, context):
    autocard = autoCard()
    result = autocard.run()
    weixin_notification(result)
    return result


if __name__ == '__main__':
    autoCard = autoCard("2020010907003","3895823abc")
    weixin_notification(autoCard.run())
