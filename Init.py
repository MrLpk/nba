#coding=utf-8

import urllib2
import re
import cookielib
import time
import os
from extlibs.MTool import MTool

startTeam = 1
teamCount = 30 #nba球队数量
startYear = 2011
endYear	  = 2011
downTeamData = False
downMatchDate = False
downMatchResult = False
isCreatePlayer = True

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

					# _key = '''<td height="20"><a href="player_one\.php\?id=(\d*)" target="_blank">([\d\D]*)</td></tr>'''
					_key = '<table width="702" border="0" align="center" cellpadding="0" cellspacing="1" class="text">([\d\D]*)</table></td></tr>'
					_result = re.findall(_key, _fileContent)

					print _result
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

if __name__ == '__main__':
	start()
