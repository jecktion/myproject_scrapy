# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class SinaSpiderPipeline(object):
#     def process_item(self, item, spider):
#         return item

import pymysql
from scrapy import signals
# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")

class SinaPipeline(object):
    def process_item(self, item, spider):
        sonUrls = item['sonUrls']

        # 文件名为子链接url中间部分，并将 / 替换为 _，保存为 .txt格式
        filename = sonUrls[7:-6].replace('/','_')
        filename += ".txt"

        fp = open(item['subFilename']+'/'+filename, 'w')
        fp.write(item['content'])
        fp.close()

        return item

class MysqlDB(object):
    def __init__(self):
        try:
            self.conn = pymysql.connect('127.0.0.1','root','root','mydb',charset='utf8')
            # self.conn = pymysql.connect('192.168.101.10', 'root', 'root', 'mydb', charset='utf8')
            self.cursor = self.conn.cursor()
        except Exception as e:
            print('连接数据库失败：%s'% str(e))

    def close(self):
        self.cursor.close()
        self.conn.close()


#插入不可更新的数据库!
class SinaPipeline(MysqlDB):
    def process_item(self,item,spider):
        sql='insert into sina(parentTitle,parentUrls,subTitle,subUrls,subFilename,sonUrls,head,content,url)'\
            'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)on duplicate key update parentTitle=VALUES(parentTitle),parentUrls = VALUES(parentUrls),'\
            'subTitle = VALUES(subTitle),subUrls = VALUES(subUrls),subFilename = VALUES(subFilename),sonUrls = VALUES(sonUrls),head = VALUES(head),content = VALUES(content),url = VALUES(url)'

        try:
            self.cursor.execute(sql,(
                item["parentTitle"],item["parentUrls"],item["subTitle"],item["subUrls"],item["subFilename"],item["sonUrls"],item["head"],item["content"],item["url"]
            ))

            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            # print(e)
            # print("执行sql语句失败")
            print("执行sql语句失败：%s" % (str(e)))
            #把错误内容写入englandshool.txt日志文件
            with open("./mysqlerror/error.txt", 'w', encoding="utf-8") as f:
                f.write(str(e) + "\n========================")
#
        return item

