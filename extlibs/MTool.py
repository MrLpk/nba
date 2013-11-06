#-*- coding: utf-8 -*-
'''
Created on 2013-8-27

@author: liaopengkai
'''
import urllib2
import os
import json

class MTool:
    
    def isNum(self, tempStr):
        """判断字符串是否为数字，整型和浮点型皆适用"""
        try:
            float(tempStr)
            return True
        except Exception:
            return False
        
    def save(self, filename, contents, reNew = True, path = ''):
        '''保存文件，参数:文件名、内容、是否覆盖更新、路径'''
        if not path == '':
            if not os.path.isdir(path):
                os.mkdir(path)
            filename = path + filename
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
        
if __name__ == '__main__':
    pass
#     url = 'http://www.111kj.com/kjjg/2012.htm'
    m = MTool()
#     m.download(url, 't/')
    obj = [
           {'year':2012, 
            'data':[
                    {'no':1,'num':[1,2,3,4,5,6],'special':7},
                    {'no':2,'num':[11,12,13,14,15,16],'special':18}
                    ]
            }
           ]
    abc = json.dumps(obj)
#     print abc
    m.save('t.json', abc)
    
    f = open('t.json', 'r')
    content = f.read()
    
    cc = json.loads(content)
    print cc[0]
    
    
    
    
    
    