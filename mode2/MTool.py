#-*- coding: utf-8 -*-
'''
Created on 2013-8-27

@author: liaopengkai
'''
import urllib2
import os
import json
import re
import time

class MTool:
    
    def isNum(self, tempStr):
        """判断字符串是否为数字，整型和浮点型皆适用"""
        try:
            float(tempStr)
            return True
        except Exception:
            return False
        
    def save(self, filename, contents, reNew = True, path = '', path2 = ''):
        '''保存文件，参数:文件名、内容、是否覆盖更新、路径'''
        if not path == '':
            if not os.path.isdir(path):
                os.mkdir(path)
            if not os.path.isdir(path + path2):
                os.mkdir(path + path2)
            filename = path + path2 + filename
        if os.path.exists(filename):
            if not reNew:
                print 'You already have ' + filename
                return
        fh = open(filename, 'w') 
        fh.write(contents) 
        fh.close() 
#         print filename
        print 'Save '+filename+' success...'
        
    def download(self, url, path = '', reNew = True):
        '''下载并保存'''
        
        temp = url.split('/')
        name = temp[len(temp)-1]
        
        if path != '':
            filename = path + name
        if os.path.exists(filename):
            if not reNew:
                print 'You already have ' + filename
                return
            
        result = urllib2.urlopen(url).read()
        self.save(name, result, reNew, path)

    def getTime(self, _str = '%Y-%m-%d %H:%M:%S', _t = time.localtime()):
        t = time.strftime(_str, _t)
        return t

    def sumTime(self, _hour = 0, _min = 0, _sec = 0):
        t = time.time()
        t += (3600*_hour + 60*_min + _sec)
        return time.localtime(t)

    def subTime(self, _hour = 0, _min = 0, _sec = 0):
        t = time.time()
        t -= (3600*_hour + 60*_min + _sec)
        return time.localtime(t)

if __name__ == '__main__':
    pass

    
    
    
    
    
    