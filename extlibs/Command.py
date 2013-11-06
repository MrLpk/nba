#coding=UTF-8
'''
Created on 2013年8月17日

@author: liaopengkai
'''
from MTool import MTool

class Command:
    
    COM_UNKNOW      = 0
#   SF_COMMAND    0-49
    COM_SF_ADD      = 1
    COM_SF_CHECK    = 2
    COM_SF_CLEAN    = 3
    
    #SIGN_COMMAND  50-69
    COM_SIGN_START  = 50
    COM_SIGN_STOP   = 51
    
    mt = MTool() 
    # 解析命令
    def analyzeCommand(self, msg):
        text = msg['Content']
        text = text.split(' ')
        
        #print len(text)
        if text[0] == u'宿费' or text[0] == u'sf' or text[0] == u'SF' or text[0] == u'舍费':
            if self.mt.isNum(text[1]):
                print 'COM_SF_ADD!!'
                return self.COM_SF_ADD
            elif text[1] == u'check':
                print 'COM_SF_CHECK!!'
                return self.COM_SF_CHECK
            elif text[1] == u'clean':
                print 'COM_SF_CLEAN!!'
                return self.COM_SF_CLEAN
            else:
                print 'UNKNOW_COMMAND'
                return self.COM_UNKNOW
        elif text[0] == u'bd' or text[0] == u'BD' or text[0] == 'baidu':
            if text[1] == 'run' or text[1] == 'r' or text[1] == 'start' or text[1] == 'b' or text[1] == 'begin':
                print 'COM_SIGN_START!!'
                return self.COM_SIGN_START
            elif text[1] == 'stop' text[1] == 's' text[1] == 'S':
                print 'COM_SIGN_STOP!!'
                return self.COM_SIGN_STOP
            else:
                print 'UNKNOW_COMMAND'
                return self.COM_UNKNOW
        else:
            print 'UNKNOW_COMMAND'
            return self.COM_UNKNOW
