import json
import os
from getPwd import getPwd
import requests
from lxml import etree
import time
import verCaptcha


def nowTimestamp(digits=13):
    timestamp = time.time()
    digits = 10 ** (digits - 10)
    timestamp = int(round(timestamp * digits))
    return str(timestamp)


class autoCard:
    def __init__(self, username, password):
        self.getPwd = getPwd()
        self.__init_session()
        self.__load_sites(username, password)

    def __init_session(self):
        self.__session = requests.session()
        self.__session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ("
                                                     "KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"})

    def __load_sites(self, username, password):
        with open(os.path.join("sites.json"), "r", encoding="utf-8") as fr:
            self.__sites = json.load(fr)
        self.__set_sites("login", "data", "username", username)
        self.__set_sites("login", "data", "password", password)
        self.__set_sites("home", "data", str(self.__sites["home"]["data"]).encode("utf-8"))
        self.__set_sites("school", "data", str(self.__sites["school"]["data"]).encode("utf-8"))


    def __request(self, api, allow_redirects=True):
        site = self.__sites[api]
        return self.__session.request(
            method=site["method"],
            url=site["url"],
            data=site["data"],
            allow_redirects=allow_redirects,
            timeout=5
        ) if site["data"] != {} else \
            self.__session.request(
            method=site["method"],
            url=site["url"],
            allow_redirects=allow_redirects,
            timeout=5
        )

    def __set_sites(self, api, item, content1, content2=None):
        if content2 is None:
            self.__sites[api][item] = content1
        else:
            self.__sites[api][item][content1] = content2

    def __get_captcha(self):
        self.__set_sites("captcha", "url", self.__sites["captcha"]["url"] + nowTimestamp())
        image_json = self.__request("captcha").json()
        move_base64 = image_json['smallImage']
        bg_base64 = image_json['bigImage']
        return move_base64, bg_base64

    def __verify_captcha(self):
        move_base64, bg_base64 = self.__get_captcha()
        move_length = verCaptcha.getCapath(move_base64, bg_base64)
        self.__set_sites("verify", "url",
                         self.__sites["verify"]["url"][:self.__sites["verify"]["url"].rfind("=") + 1] + move_length)        
        verify_ans = self.__request("verify").json()
        if verify_ans['code'] != 0:
            self.__verify_captcha()
        else:
            self.__set_sites("login", "data", "sign", verify_ans['sign'])

    def __login(self):
        self.__set_sites("login", "url", self.__request("page", False).headers["Location"])
        login_html = etree.HTML(self.__request("login").text)
        self.__set_sites("login", "data", "lt", login_html.xpath('//*[@id="casLoginForm"]/div/input[1]/@value')[0])
        self.__set_sites("login", "data", "dllt", login_html.xpath('//*[@id="casLoginForm"]/div/input[2]/@value')[0])
        self.__set_sites("login", "data", "execution",
                         login_html.xpath('//*[@id="casLoginForm"]/div/input[3]/@value')[0])
        self.__set_sites("login", "data", "_eventId",
                         login_html.xpath('//*[@id="casLoginForm"]/div/input[4]/@value')[0])
        self.__set_sites("login", "data", "rmShown", login_html.xpath('//*[@id="casLoginForm"]/div/input[5]/@value')[0])
        self.__set_sites("login", "data", "password", self.getPwd.run(self.__sites["login"]["data"]["password"],
                                                                      login_html.xpath(
                                                                          '//*[@id="pwdDefaultEncryptSalt"]/@value')[
                                                                          0]))
        self.__verify_captcha()
        self.__set_sites("login", "method", "POST")
        login_response = self.__request("login", False).headers
        if "Location" not in login_response:
            return False
        self.__set_sites("ticket", "url", login_response["Location"])
        self.__request("ticket")
        self.__set_sites("path", "url", self.__sites["path"]["url"] + nowTimestamp())
        self.__set_sites("bind", "url",
                         self.__sites["bind"]["url"] + self.__request("path").json()['data'][0]['imagePath'])
        return True

    def run(self):
        if self.__login():
            status = self.__request("status").json()["data"]
            self.__session.headers.update({"content-type": "application/json"})
            if status["appliedTimes"] != 0:
                return "已经打过卡了"
            elif status["schoolStatus"] == 0:
                self.__request("home")
            elif status["schoolStatus"] == 1:
                self.__request("school")
            status = self.__request("status").json()["data"]
            if status["appliedTimes"] != 0:
                return "打卡成功"
            return "打卡异常"
        else:
            return "账号或密码错误"
