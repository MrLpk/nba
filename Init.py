#coding=utf-8

import re
import os
import json
from extlibs.MTool import MTool

PLAYER_DATA_PATH = ''

def checkPlayerData(str1, str2):
	_path = 'db/data.d'
	if not os.path.isdir('db/'):
		os.mkdir('db/')
	if not os.path.exists(_path):
		f = open(_path, 'w')
		_content = '{}'
		f.write(_content)
		f.close()
	_file = open(_path, 'r').read()
	_json = json.loads(_file)

	try:
		_player = _json[str1]
	except Exception, e:
		_json[str1] = str2
		_j = json.dumps(_json)
		f = open(_path, 'w')
		f.write(_j)
		f.close()
		print 'add new player %s %s success' %(str1, str2)
	

def initPlayerData():
	path = 'match/scores/'

	for y in os.listdir(path):
		_pathY = path + y + '/'
		for m in xrange(1, 13):
			_pathM = _pathY + str(m) + '/'
			if os.path.isdir(_pathM):
				for i in xrange(1, len(os.listdir(_pathM))+1):
					_fileI = _pathM + str(i) + '.html'
					# print _fileI

					_fileContent = open(_fileI, 'r').read()
					# print _fileContent

					'''这个正则可以拿到包括id、名字、数据'''
					_key = '''<td height="20"><a href="player_one\.php\?id=(\d*)" target="_blank">([\d\D]{1,250})</tr>'''
					# _key = '<td height="20"><a href="player_one\.php\?id=(\d*)" target="_blank">([\d\D]{1,25})</a></td>'
					_result = re.findall(_key, _fileContent)

					'''可拿详细数据,对应第一个_key'''
					for r in _result:
						print r[0],r[1].decode('gbk')

						_keyName = '(.*)</a></td>'
						_rName = re.findall(_keyName, r[1])
						print _rName[0].decode('gbk')
						# checkPlayerData(r[0], 1)
						break

					break
			break
		break
	return 

def start():
	initPlayerData()

if __name__ == '__main__':
	start()