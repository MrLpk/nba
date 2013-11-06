#-*- coding: utf-8 -*-
'''
Created on 2013年8月17日

@author: liaopengkai
'''
import hashlib
import xml.etree.ElementTree as ET
import time

class Weixin:
    
    
    def calibration_WeiXin(self, request):
        """
                            校对微信帐号
        """
        signature = request.args.get('signature')
        timestamp = request.args.get('timestamp')
        nonce     = request.args.get('nonce')
        
        if (signature == None) or (timestamp == None) or (nonce == None):
            return False
    
        token = 'lpkpytest'
        tmplist = [token, timestamp, nonce]
        tmplist.sort()
        tmpstr = ''.join(tmplist)
        hashstr = hashlib.sha1(tmpstr).hexdigest()
    
        if hashstr == signature:
            return True
        return False
    

    def parse_msg(self, data):
        """
                            解析微信POST过来的XML
        """
        root = ET.fromstring(data)
        msg = {}
        for child in root:
            msg[child.tag] = child.text
        return msg
    
    
    def isTextMsg(self, msg):
        """
                            判断是否文字消息
        """
        return msg['MsgType'] == 'text'
    
    
    def responseTextMsg(self, msg, content):
        """
                            生成回复消息
        """
        RE_TEXT_MSG = """
        <xml>
         <ToUserName><![CDATA[%s]]></ToUserName>
         <FromUserName><![CDATA[%s]]></FromUserName>
         <CreateTime>%s</CreateTime>
         <MsgType><![CDATA[text]]></MsgType>
         <Content><![CDATA[%s]]></Content>
        </xml>
         """
    
        RE_TEXT_MSG = RE_TEXT_MSG %(msg['FromUserName'], msg['ToUserName'], str(int(time.time())), content)
        return RE_TEXT_MSG
    
    
    