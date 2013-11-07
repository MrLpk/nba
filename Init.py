#coding=utf-8

import urllib2
import re
import cookielib
from extlibs.MTool import MTool

teamCount = 1 #nba球队数量
startYear = 2011
endYear	  = 2011

def downloadData(teams, years, months):
	URL = 'http://nba.sports.sina.com.cn/team_match.php?month=1&years=%d&months=%d&teams=%d' %(years, months, teams)

	# html = urllib2.urlopen(URL).read()

	req = urllib2.Request(URL)
	req.add_header("Host", "nba.sports.sina.com.cn")
	req.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
	req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 5.1; rv:25.0) Gecko/20100101 Firefox/25.0")

	html = urllib2.urlopen(req).read()
	m = MTool()
	name = u'%d年-%d月.html' %(years, months)
	path = '%d/' %teams
	m.save(name, html, True, path)

def start():

	'''启用cookie'''
	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	urllib2.install_opener(opener)


	for x in xrange(1,teamCount+1):
		for y in xrange(startYear, endYear+1):
			for z in xrange(1,13):
				downloadData(x, y, z)

	# print html

if __name__ == '__main__':
	# start()
	downloadData(5, 2012, 4)