# -*- coding:utf-8 -*-
import requests
import time
import random
import logging
import os
"""
cron: 10 13 * * *
new Env('微嘉园');

阅读、点赞、视频
青龙变量:MicroCk

用#号隔开账号
用&隔开openid与token
格式: openid1&token1#openid2&token2
"""

logger = logging.getLogger(name=None)  # 创建一个日志对象
logging.Formatter("%(message)s")  # 日志内容格式化
logger.setLevel(logging.INFO)  # 设置日志等级
logger.addHandler(logging.StreamHandler())  # 添加控制台日志

# logger.addHandler(logging.FileHandler(filename="text.log", mode="w"))  # 添加文件日志
userList = os.environ["MicroCk"].split("#")


class MicroHome:
    def __init__(self, openidVal,tokenIdVal):
        self.openid = openidVal
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MI 5 Build/MXB48T; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.62 XWEB/2853 MMWEBSDK/20210501 Mobile Safari/537.36 MMWEBID/5986 MicroMessenger/8.0.6.1900(0x28000653) Process/appbrand0 WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android',
            'content-type': 'application/json', 'token-id': tokenIdVal,'openid':openidVal}
        self.NewsList = []
        self.tieziList = []
        self.getNewsIndex()
        self.getTieziIndex()

    def getNewsIndex(self):
        NewsIndexUrl = 'https://swzfw1.jiaxing.gov.cn/api/news/index'
        data = {"code": "330411104209", "openid": self.openid, "type": 1, "page": 1}
        response = requests.post(url=NewsIndexUrl, headers=self.headers, json=data)
        dataList = response.json()['data']['data']
        for data in dataList:
            tid = data['id']
            title = data['title']
            self.NewsList.append([tid, title])

    def getTieziIndex(self):
        NewsIndexUrl = 'https://swzfw1.jiaxing.gov.cn/shequ_api/tiezi/tiezi'
        for i in range(5):
            data = {"openid": self.openid, "page": i, "bianma": "330411104209"}
            response = requests.post(url=NewsIndexUrl, headers=self.headers, json=data)
            dataList = response.json()['data']['data']
            for data in dataList:
                tid = data['id']
                self.tieziList.append(tid)
        new_list = list(dict.fromkeys(self.tieziList))

    def zan(self):
        zanUrl = 'https://swzfw1.jiaxing.gov.cn/api/news/zan'
        index = 1
        for News in self.NewsList:
            data = {"tid": News[0], "openid": self.openid}
            response = requests.post(url=zanUrl, headers=self.headers, json=data)
            logger.info(response.text)
            if response.json()['msg'] == "点赞成功":
                index += 1
            if index > 3:
                logger.info("点赞任务执行完成...")
                break

    def shequZan(self):
        zanUrl = 'https://swzfw1.jiaxing.gov.cn/shequ_api/tiezi/dianzan'
        for News in self.tieziList:
            data = {"tid": News, "openid": self.openid}
            response = requests.post(url=zanUrl, headers=self.headers, json=data)
            logger.info(response.text)
            if response.json()['msg'] == "点赞成功":
                logger.info("点赞任务执行完成...")
                break

    def read(self):
        readUrl = 'https://swzfw1.jiaxing.gov.cn/api/news/read'
        for News in self.NewsList:
            data = {"openid": self.openid, "id": News[0], "title": News[1]}
            response = requests.post(url=readUrl, headers=self.headers, json=data)
            logger.info(response.text)
            if response.json()['msg'] == "今日积分已领取完毕":
                logger.info("阅读任务执行完成...")
                break

    def shiping(self):
        for _ in range(5):
            shipingUrl = 'https://swzfw1.jiaxing.gov.cn/shequ_api/Jiaxing/shiping'
            data = {"openid": self.openid}
            response = requests.post(url=shipingUrl, headers=self.headers, json=data)
            logger.info(response.text)
            if response.json()['msg'] == "今日积分已领取完毕":
                logger.info("视频任务执行完成...")
                break

    def Score(self):
        ScoreUrl = 'https://swzfw1.jiaxing.gov.cn/api/My/user'
        data = {"openid": self.openid}
        response = requests.post(url=ScoreUrl, headers=self.headers, json=data)
        logger.info("当前账户:"+str(response.json()['data']['mobile'])+"\n积分:"+str(response.json()['data']['score']))

    def check(self):
        self.Score()
        checkUrl = 'https://swzfw1.jiaxing.gov.cn/api/My/my_score'
        data = {"openid": self.openid}
        response = requests.post(url=checkUrl, headers=self.headers, json=data)
        for data in response.json()['data']:
            if data['type'] == '2' : # 阅读任务
                if data['info'] == 2:
                    logger.info("今天已经做过阅读文章拉...")
                else:
                    self.read()
            elif data['type'] == '3' : # 视频任务
                if data['info'] == 2:
                    logger.info("今天已经做过视频学习拉...")
                else:
                    self.shiping()
            elif data['type'] == '4' : # 点赞
                if data['info'] >= 1:
                    logger.info("今天已经做过点赞拉...")
                else:
                    self.zan()
                    self.shequZan()
        logger.info("-"*30)



def main():
    for user in userList:
        user = user.split("&")
        openid = user[0]
        tokenId = user[1]
        rTime = random.randrange(30, 120)
        qd = MicroHome(openid,tokenId)
        qd.check()
        logger.info(f"\n下一个账号将在{rTime}s后运行")
        time.sleep(rTime)


if __name__ == '__main__':
    main()
