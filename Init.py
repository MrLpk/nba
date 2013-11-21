#coding=utf-8

import re
import os
import json
from PlayerScore import PlayerScore
from extlibs.MTool import MTool
from pyquery import PyQuery as pq

PLAYER_DATA_PATH = ''	

def checkPlayerData(pid, data, years, month, day):
	_path = 'db/data.db'
	if not os.path.isdir('db/'):
		os.mkdir('db/')
	if not os.path.exists(_path):
		f = open(_path, 'w')
		_content = '{}'
		f.write(_content)
		f.close()
	_file = open(_path, 'r').read()
	_json = json.loads(_file)

	p = PlayerScore(data)
	p.setDate(years, month, day)

	try:
		_playerData = _json[str(pid)]
		_playerData.append(p.getObj())
		_json[pid] = _playerData
		_j = json.dumps(_json)
		f = open(_path, 'w')
		f.write(_j)
		f.close()
		print 'add player %s data success' %pid
	except Exception, e:
		o = [p.getObj()]
		_json[pid] = o
		_j = json.dumps(_json)
		f = open(_path, 'w')
		f.write(_j)
		f.close()
		print 'new player %s data success' %pid
	print '*'*40

def initPlayerData():

	years = 2011
	month = 0
	day	  = 0

	'''view all years '''
	for x in xrange(1, 2):
		_path = u'match/date/%d/%d-%d.html' %(years, years, x)

		_fileContent = open(_path, 'r').read()

		d = pq(_fileContent)
		_arr = d('tr')

		_count = 1
		''' view all month's game '''
		for y in xrange(1, 12):#len(_arr)):
			_html = _arr.eq(y).html()
			_key = '<td width="90" height="25">'
			_result = re.findall(_key, _html)
			if len(_result) == 1:
				'''it include date'''
				_k = u'([\d]{2})月([\d]{2})日'
				_r = re.findall(_k, _html)
				
				month = int(_r[0][0])
				day   = int(_r[0][1])
				# print '-'*20
			else:
				'''it include match score'''
				__path = 'match/scores/%d/%d/%d.html' %(years, month, _count)
				
				_count+=1

				_matchContent = open(__path, 'r').read()
				'''这个正则可以拿到包括id、名字、数据'''
				__key = '''<td height="20"><a href="player_one\.php\?id=(\d*)" target="_blank">([\d\D]{1,250})</tr>'''
				__result = re.findall(__key, _matchContent)

				'''可拿详细数据,对应第一个_key'''
				for __r in __result:
					_pid = int(__r[0])
 
					_data = re.findall('<td>([\d-]*)</td>', __r[1])
					# print _pid
					# print __r[1].decode('gbk')
					# print _data
					checkPlayerData(_pid, _data, years, month, day)
				

def start():
	initPlayerData()

if __name__ == '__main__':
	start()
