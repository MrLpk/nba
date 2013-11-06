#coding=utf-8
'''
Created on 2013年8月17日

@author: liaopengkai
'''

import MySQLdb
from sae.const import (MYSQL_HOST, #MYSQL_HOST_S,
    MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_DB
)

from flask import g

class MySQLSAE:
    
    
    def r(self):
        g.db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASS,MYSQL_DB, port=int(MYSQL_PORT))
        self.c = g.db.cursor()
        # 临时改MYSQL编码,由于修改不了SAE上MYSQL的配置，因此每次使用MYSQL时都需临时设置一遍，以防中文字符编码出现问题
        self.c.execute('set names utf8')
    
    def insertDB(self, sql):
        self.r()
        self.c.execute(sql.encode('utf-8'))
        if hasattr(g, 'db'): 
            g.db.close()
        
    def selectDB(self, sql):
        self.r()
        self.c.execute(sql.encode('utf-8'))
        msgs = list(self.c.fetchall())
        if hasattr(g, 'db'): 
            g.db.close()
        return msgs