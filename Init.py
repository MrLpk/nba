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
endYear	  = 2014
downTeamData = False
downMatchDate = False
downMatchResult = True

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
	
	for x in xrange(1, 2):
		_path = u'match/date/%d/%d-%d.html' %(years, years, x)
		f = open(_path, 'r').read()
		print 'f = /n', f

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

if __name__ == '__main__':
	start()
