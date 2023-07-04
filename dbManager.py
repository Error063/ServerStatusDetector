import os

import pymysql
import json


class manager:
    def __init__(self, detector=False):
        if os.path.exists("./config.json"):
            with open("./config.json", mode='r', encoding='utf8') as f:
                self.info = json.load(f)

        else:
            raise Exception("Not installed, please execute setting.py first")

        self.dbInfo = self.info['database']
        self.conn = pymysql.connect(host=self.dbInfo['host'],
                                        port=self.dbInfo['port'],
                                        user=self.dbInfo['user'],
                                        password=self.dbInfo['password'],
                                        database=self.dbInfo['database']
                                        )

        self.cursor = self.conn.cursor()
        self.detect_sites = self.info['sites']['list']
        self.sites_len = self.info['sites']['length']

        if detector:
            self.cursor.execute("delete from nowstatus")
            for i in range(self.sites_len):
                self.cursor.execute(f"insert into nowstatus(site) values(%s)", (self.detect_sites[i]['url']))

    def updateStatus(self, url: str, status: str, loadTime: float):
        self.cursor.execute("update nowstatus set status=%s, UpdateTime=now(), loadTime=%s where site=%s", (status, loadTime, url))
        self.conn.commit()

    def updateDown(self, url: str):
        self.cursor.execute("update nowstatus set lastDownTime=now() where site=%s", (url))
        self.conn.commit()

    def queryStatus(self):
        page = []
        self.cursor.execute("select * from nowstatus order by site")
        dataset = self.cursor.fetchall()
        for data in dataset:
            tmp = []
            for i in range(len(data)):
                item = str(data[i])
                if (item.startswith("http://") or item.startswith("https://")):
                    for i in range(self.sites_len):
                        if item == self.detect_sites[i]['url']:
                            break
                    tmp.append(self.detect_sites[i]['name'])
                else:
                    tmp.append(str(item))
                    if tmp[-1] == 'None':
                        tmp[-1] = '暂无记录'
            page.append(tmp)
        return page
