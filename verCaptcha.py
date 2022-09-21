import cv2
import numpy as np
import base64


def getCapath(bg_base64, move_base64):
    # base64解码
    bg_data = base64.b64decode(bg_base64)
    # 转换为np数组
    bg_array = np.frombuffer(bg_data, np.uint8)
    # 转换成opencv可用格式
    bg_img = cv2.imdecode(bg_array, cv2.COLOR_RGB2BGR)
    move_data = base64.b64decode(move_base64)
    move_array = np.frombuffer(move_data, np.uint8)
    move_img = cv2.imdecode(move_array, cv2.COLOR_RGB2BGR)

    return str(calCapath(bg_img, move_img))


def calCapath(bg_img, move_img):
    # 边缘检测
    bg_edge = cv2.Canny(bg_img, 200, 400)
    move_edge = cv2.Canny(move_img, 200, 400)
    # 特征匹配
    res = cv2.matchTemplate(bg_edge, move_edge, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)  # 寻找最优匹配
    return int(max_loc[0] / 2.1)  # 返回最匹配点的x坐标/2.1 即为验证码的正确答案 下载图片长为590 而指定最长距离为280 故取590/280


