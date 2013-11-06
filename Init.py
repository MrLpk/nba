#coding=utf-8

import urllib2
import re
from extlibs.MTool import MTool

def start():
	URL = 'http://nba.sports.sina.com.cn/team_match.php?month=1&years=2012&months=11&teams=27'

	html = urllib2.urlopen(URL).read()

	m = MTool()
	m.save('1.html', html)

	# print html

if __name__ == '__main__':
	start()