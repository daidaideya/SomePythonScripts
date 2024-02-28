# -*- coding:utf-8 -*-
import time
import requests
import os
import logging

"""
new Env('太太乐餐饮服务');
cron: 5 10,12,14,16,18 * * *

青龙变量:ttl_count

用#号隔开每个账号
用&隔开账号密码是
格式: user1&pass1#user2&pass2

如需换话费 下载太太乐APP积分兑换话费

"""

logger = logging.getLogger(name=None)  # 创建一个日志对象
logging.Formatter("%(message)s")  # 日志内容格式化
logger.setLevel(logging.INFO)  # 设置日志等级
logger.addHandler(logging.StreamHandler())  # 添加控制台日志
# logger.addHandler(logging.FileHandler(filename="text.log", mode="w"))  # 添加文件日志

ttlHost = 'https://www.ttljf.com/ttl_chefHub/'

userList = os.environ["ttl_count"].split("#")

headers = {"Host": "www.ttljf.com", "Connection": "keep-alive",
           "Accept": "application/json, text/plain, */*", "content-type": "application/json",
           "Cookie": "JSESSIONID=498D43BB7C04562432FB5AD3FB5AAABF; agreePrivacy=false",
           "X-Requested-With": "XMLHttpRequest",
           "Accept-Encoding": "gzip,compress,br,deflate",
           "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.17(0x1800112e) NetType/WIFI Language/zh_CN",
           "Referer": "https://servicewechat.com/wxe9aa8f1c4a77ddf5/21/page-frame.html"}


def login(usernameVal, passwordVal):
    body = {"mthd": "login", "platform": "wx_mini", "userName": usernameVal, "password": passwordVal}
    loginRes = requests.post(url='https://www.ttljf.com/ttl_chefHub/login/restaurant', headers=headers, json=body)
    token = loginRes.json()['data']['token']
    return token


def main(tkVal, usernameVal):
    logger.info(f"\n正在运行太太乐第{index}个号\n用户名为:{usernameVal}")

    headers["token"] = tkVal
    # share
    body = {"id": "A35D575F-C004-4717-AABC-ED9D1979C3FA", "type": "blog"}
    shareRes = requests.put(url=ttlHost + 'Common/share/A35D575F-C004-4717-AABC-ED9D1979C3FA/blog', headers=headers,
                            json=body)
    logger.info("分享:" + shareRes.json()['message'])
    if shareRes.json()['message'] == "请先登录":
        logger.info("cookie失效了！")
    else:
        logger.info("等待10s")
        time.sleep(10)

        # sign
        signRes = requests.put(url=ttlHost + 'user/api/sign/today', headers=headers)
        logger.info("签到:" + signRes.json()['message'])

        # integral
        myRes = requests.get(url=ttlHost + 'user/api/my', headers=headers)
        logger.info("积分:" + str(myRes.json()['data']['integral']))


if __name__ == '__main__':
    index = 0
    for user in userList:
        index += 1
        user = user.split("&")
        username = user[0]
        password = user[1]
        tk = login(username, password)
        main(tk, username)
