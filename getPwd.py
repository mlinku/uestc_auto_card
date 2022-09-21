import execjs


def js_from_file(file_name):
    with open(file_name, "r", encoding="UTF-8") as file:
        result = file.read()
    return result


class getPwd:
    def __init__(self):
        self.js = js_from_file("encrypt.js")

    def run(self, password, salt):
        ctx = execjs.compile(self.js, cwd="crypto-js")  # 定义js 模块的绝对路径
        return ctx.call("encryptAES", password, salt)
