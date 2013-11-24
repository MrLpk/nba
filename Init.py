#coding=utf-8

import re
import os
import json
from PlayerScore import PlayerScore
from extlibs.MTool import MTool
from pyquery import PyQuery as pq

PLAYER_DATA_PATH = ''	

def checkPlayerData(pid, data, years, month, day, i, n, playoffs):
	'''save'''
	_path = 'db/%d/%d.db' %(n, pid)
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
	p.setPlayoffs(playoffs)

	try:
		_playerData = _json[str(pid)]
		_playerData.append(p.getObj())
		_json[pid] = _playerData
		_j = json.dumps(_json)
		f = open(_path, 'w')
		f.write(_j)
		f.close()
		print u'add player %s data success  --- %d年-%d月-%d日  ---%d次' %(pid, years, month, day, i)
	except Exception, e:
		o = [p.getObj()]
		_json[pid] = o
		_j = json.dumps(_json)
		f = open(_path, 'w')
		f.write(_j)
		f.close()
		print u'new player %s data success  --- %d年-%d月-%d日  ---%d次' %(pid, years, month, day, i)
	print '*'*40

def initPlayerData(years, smonth, emonth, n):

	# years = 2011
	month = 0
	day	  = 0
	i = 1

	'''view all years '''
	for x in xrange(smonth, emonth+1):
		_path = u'match/date/%d/%d-%d.html' %(years, years, x)

		_fileContent = open(_path, 'r').read()

		d = pq(_fileContent)
		_arr = d('tr')

		_count = 1
		''' view all month's game '''
		for y in xrange(1, len(_arr)):#224):#
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
				'''expect the normal match'''

				_r1 = re.findall(u'<td>常规赛</td>', _html)
				_r2 = re.findall(u'<td>季后赛</td>', _html)
				if len(_r1) == 1 or len(_r2) == 1:

					__path = 'match/scores/%d/%d/%d.html' %(years, month, _count)
					

					_matchContent = open(__path, 'r').read()
					'''这个正则可以拿到包括id、名字、数据'''
					__key = '''<td height="20"><a href="player_one\.php\?id=(\d*)" target="_blank">([\d\D]{1,250})</tr>'''
					__result = re.findall(__key, _matchContent)

					'''可拿详细数据,对应第一个_key'''
					for __r in __result:
						_pid = int(__r[0])
 
						_data = re.findall('<td>([\d-]*)</td>', __r[1])
						checkPlayerData(_pid, _data, years, month, day, i, n, len(_r2))


						i+=1
				else:
					print u'跳过非常规赛or季后赛场次 -- %d年-%d月-%d日' %(years, month, day)
				_count+=1

def start():
	''' 2011-2012赛季 '''
	# initPlayerData(2011, 12, 12, 1)
	# initPlayerData(2012, 1, 6, 1)

	''' 2012-2013赛季 '''
	# initPlayerData(2012, 9, 12, 2)
	# initPlayerData(2013, 1, 6, 2)

	# initPlayerData(2012, 2, 2)
if __name__ == '__main__':
	start()
