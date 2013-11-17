#coding=utf-8

import urllib2
import re
import cookielib
import time
import os
import json
from extlibs.MTool import MTool

startTeam = 1
teamCount = 30 #nba球队数量
startYear = 2011
endYear	  = 2011
downTeamData = False
downMatchDate = False
downMatchResult = False
isCreatePlayer = False
isInitPlayerData = True

def downloadTeamData(teams, years, months):
	# time.sleep(1)
	strMonth = ''
	if months < 10:
		strMonth = '0%s' %months
	else:
		strMonth = '%s' %months
	URL = 'http://nba.sports.sina.com.cn/team_match.php?month=1&years=%d&months=%s&teams=%d' %(years, strMonth, teams)
	      
	# print 'URL----',URL
	html = urllib2.urlopen(URL).read()

	m = MTool()
	name = u'%d年-%d月.html' %(years, months)
	path = '%d/' %teams
	path2 = '%d/' %years
	m.save(name, html, True, path, path2)

def downloadMatchDate(years, months):

	strMonth = ''
	if months < 10:
		strMonth = '0%s' %months
	else:
		strMonth = '%s' %months
	URL = 'http://nba.sports.sina.com.cn/match_result.php?day=0&years=%d&months=%s&teams=' %(years, strMonth)
	

	html = urllib2.urlopen(URL).read()

	m = MTool()
	name = u'%d-%d.html' %(years, months)
	if not os.path.isdir('match/'):
		os.mkdir('match/')
	path = 'match/date/'
	path2 = '%d/' %years
	m.save(name, html, True, path, path2)

def downloadMatchResult(years):

	INDEX = 'http://nba.sports.sina.com.cn/look_scores.php?id='
	m = MTool();

	if not os.path.isdir('match/scores/'):
		os.mkdir('match/scores/')

	if not os.path.isdir('match/scores/%d/' %years):
		os.mkdir('match/scores/%d/' %years)

	for x in xrange(2, 13):

		# print 'sleep 10 second...'
		# time.sleep(10)

		_path = u'match/date/%d/%d-%d.html' %(years, years, x)
		f = open(_path, 'r').read()
		# key1 = '<td width="90" height="25">(.*)</td>'
		key1 = '<a href="look_scores\.php\?id=(.*)" target="_blank">'

		r1 = re.findall(key1, f)
		
		i = 1
		for y in r1:
			name = '%s.html' %i
			path = 'match/scores/%d/%d/' %(years, x)
			filename = path + name
			if not os.path.exists(filename):
				_url = INDEX + y
				html = urllib2.urlopen(_url).read()
				m.save(name, html, False, path)
			else:
				print 'You already have ' + filename

			i+=1
			# break


		# print 'lll--%d' %len(r1)
def checkPlayer(str1, str2):
	if not os.path.isdir('db/'):
		os.mkdir('db/')
	if not os.path.exists('db/player.d'):
		f = open('db/player.d', 'w')
		_content = '{"num": 0, "player": []}'
		f.write(_content)
		f.close()
	_file = open('db/player.d', 'r').read()
	_json = json.loads(_file)
	_player = _json['player']
	_num = _json['num']
	# print _file
	# print _player
	# print _num

	hasMember = False
	for x in xrange(_num):
		if _player[x]['pid'] == int(str1):
			hasMember = True
			break
	if not hasMember:
		_num+=1
		_obj = {"pid" : int(str1), "name" : str2.decode('gbk')}
		_player.append(_obj)

		_odb = {"num":_num, "player":_player}
		_j = json.dumps(_odb)

		f = open('db/player.d', 'w')
		f.write(_j)
		f.close()
		print 'add new player %s %s success' %(str1, str2)


def createPlayer():
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
					# _key = '''<td height="20"><a href="player_one\.php\?id=(\d*)" target="_blank">([\d\D]{1,250})</tr>'''
					_key = '<td height="20"><a href="player_one\.php\?id=(\d*)" target="_blank">([\d\D]{1,25})</a></td>'
					_result = re.findall(_key, _fileContent)

					'''可拿详细数据,对应第一个_key'''
					# for r in _result:
					# 	print r[0],r[1].decode('gbk')

					# 	_keyName = '(.*)</a></td>'
					# 	_rName = re.findall(_keyName, r[1])
					# 	print _rName[0].decode('gbk')
					# 	# break

					for r in _result:
						# print r
						# print r[0],r[1].decode('gbk')
						_keyName = '[^\r\n\t\t]*'
						_rName = re.findall(_keyName, r[1])
						# print r[0], _rName[3]#.decode('gbk')
						checkPlayer(r[0], _rName[3])

						# break
					
					# break
	# 		break
	# 	break
	# return 


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
	if downTeamData:
		for x in xrange(startTeam,teamCount+1):
			for y in xrange(startYear, endYear+1):
				for z in xrange(1,13):
					downloadTeamData(x, y, z)

	if downMatchDate:
		for x in xrange(startYear, endYear+1):
			for y in xrange(1,13):
				downloadMatchDate(x, y)
		
	if downMatchResult:
		for x in xrange(startYear, endYear+1):
			downloadMatchResult(x)
	# print html

	if isCreatePlayer:
		createPlayer()

	if isInitPlayerData:
		initPlayerData()

if __name__ == '__main__':
	start()
