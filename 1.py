import time

import requests
from lxml import etree

import verCaptcha
from getPwd import getPwd


def nowTimestamp(digits=13):
    timestamp = time.time()

    digits = 10 ** (digits - 10)

    timestamp = int(round(timestamp * digits))

    return str(timestamp)


page_url = "https://jzsz.uestc.edu.cn/"
capath_url = "https://idas.uestc.edu.cn/authserver/sliderCaptcha.do?_="
verify_url = "https://idas.uestc.edu.cn/authserver/verifySliderImageCode.do?canvasLength=280&moveLength="
user_url = "https://jzsz.uestc.edu.cn/wxvacation/api/user/getLoginUser"
check_url = "https://jzsz.uestc.edu.cn/wxvacation/api/epidemic/checkRegisterNew"
list_url = "https://jzsz.uestc.edu.cn/information-center/xd/config/getDisplays?_t="
filePath_url = "https://jzsz.uestc.edu.cn/fastdfs-util/api/fastdfs/download/image?filePath="
home_url = "https://jzsz.uestc.edu.cn/wxvacation/api/epidemic/monitorRegister"
ID = "2020090922002"
password = "2002jia0522yi"
common_header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
}

card_header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
    "content-type": "application/json",
"encode": "false"
}
session = requests.session()
response = session.get(page_url, headers=common_header, allow_redirects=False)
login_url = response.headers['Location']
response = session.get(login_url, headers=common_header)
html = etree.HTML(response.text)
salt = html.xpath('//*[@id="pwdDefaultEncryptSalt"]/@value')[0]
lt = html.xpath('//*[@id="casLoginForm"]/div/input[1]/@value')[0]
dllt = html.xpath('//*[@id="casLoginForm"]/div/input[2]/@value')[0]
execution = html.xpath('//*[@id="casLoginForm"]/div/input[3]/@value')[0]
_eventId = html.xpath('//*[@id="casLoginForm"]/div/input[4]/@value')[0]
rmShown = html.xpath('//*[@id="casLoginForm"]/div/input[5]/@value')[0]
getPwd = getPwd()
password = getPwd.run(password, salt)
response = session.get(capath_url + nowTimestamp(), headers=common_header, verify=False).json()
move_base64 = response['smallImage']
bg_base64 = response['bigImage']
length = verCaptcha.getCapath(move_base64, bg_base64)
response = session.get(verify_url + length, headers=common_header, verify=False).json()
print(response)
sign = response['sign']
login_data = {
    "username": ID,
    "password": password,
    "lt": lt,
    "dllt": dllt,
    "execution": execution,
    "_eventId": _eventId,
    "rmShown": rmShown,
    "sign": sign
}
print(login_url)
response = session.post(login_url, headers=common_header, data=login_data, allow_redirects=False, verify=False)
ticket_url = response.headers['Location']
response = session.get(ticket_url, headers=common_header, allow_redirects=False)
list_data = {"categoryId": "null", "selectFlg": "1"}
response = session.get(list_url + nowTimestamp(), headers=common_header)
response = session.get(filePath_url + response.json()['data'][0]['imagePath'], headers=common_header)
response = session.get(check_url, headers=common_header)
print(response.text)
# home_data = {"currentAddress": "广东省揭阳市普宁市光明路15号", "remark": "", "healthInfo": "正常", "healthColor": "绿色",
#              "isContactWuhan": 0, "isFever": 0, "isInSchool": 0, "isLeaveChengdu": 1, "isSymptom": 0,
#              "temperature": "36°C~36.5°C", "province": "广东省", "city": "揭阳市", "county": "普宁市", "latitude": 23.294846,
#              "longitude": 116.170402}
# home_data = {"currentAddress": "江西省南昌市青山湖区凤凰北大道598号", "remark": "", "healthInfo": "正常", "healthColor": "绿色",
#              "isContactWuhan": 0, "isFever": 0, "isInSchool": 0, "isLeaveChengdu": 1, "isSymptom": 0,
#              "temperature": "36°C~36.5°C", "province": "江西省", "city": "南昌市", "county": "南昌市", "latitude": 28.714945,
#              "longitude": 115.86689}
# response = session.post(home_url, headers=card_header, data=str(home_data).encode("utf-8"))
# print(response.json())
# print(response.request.headers)
response = session.get(check_url, headers=common_header)
print(response.text)
