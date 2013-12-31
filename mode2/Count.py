#coding=utf-8
import Collection as COL
from MTool import MTool
import urllib2
from pyquery import PyQuery as pq
import re, json
from datetime import datetime
import time

m = MTool()

def update():
	COL.collectionAllTeam()
	COL.countAllTeam()
	COL.countAllAverage()

def save(_content):
	f = open('cof', 'w')
	f.write(str(_content))
	f.close()

def isNeedUpdate():
	_sYTime = open('cof', 'r').read()
	
	_temps = datetime.today()
	_temp = _temps.replace(hour = 15, minute = 0, second = 0)
	_sSTime = time.mktime(_temp.timetuple())

	_nSubTime = _sSTime - float(_sYTime)
	_nCHour = str(_temps.time()).split(':')[0]
	_nCHour = int(_nCHour)
	if _nSubTime >= 86400:
		save(time.mktime(_temps.timetuple()))
		return True, m.getTime(_t = _temps.timetuple())
	elif _nSubTime <86400 and _nSubTime >=0:
		if _nCHour >= 15:
			save(time.mktime(_temps.timetuple()))
			return True, m.getTime(_t = _temps.timetuple())
	return False, m.getTime(_t = time.localtime(float(_sYTime)))

def checkData():
	_var , _t = isNeedUpdate()
	if _var:
		print 'start to update version...'
		update()
		print 'update version success,the version is', _t
	else:
		print 'The version is newest', _t
		


def getOneTeamPoint(team, isHome):
	_AScore = open('AScore.dt', 'r').read()
	_obj = json.loads(_AScore)

	_wPoint = 0
	_lPoint = 0
	if isHome:
		_wPoint = _obj[int(team)-1][team]['t']['w']
		_lPoint = _obj[int(team)-1][team]['t']['l']
	else:
		_wPoint = _obj[int(team)-1][team]['f']['w']
		_lPoint = _obj[int(team)-1][team]['f']['l']

	_tObj = _obj[int(team)-1][team]['t']
	_fObj = _obj[int(team)-1][team]['f']
	return _wPoint, _lPoint

def getAveragePoint():
	_Average = open('Average.dt', 'r').read()
	_obj = json.loads(_Average)
	return _obj['tl'], _obj['fl']

def getPan(wantR = False):
	URL = 'http://trade.500.com/jclq/index.php?playid=277'
	_content = urllib2.urlopen(URL).read()

	if not wantR:
		_content = pq(_content)('.dc_table').eq(1).html()

	return _content

def getPanPoint(teamF, teamT):
	_content = getPan()
	_trs = pq(_content)('tr')
	for x in xrange(len(_trs)):
		_tr = _trs.eq(x).html()
		_r = re.findall('177/team/(\d*)/', _tr)
		# print 'f', _r[0]
		# print 't', _r[1]
		# print _tr.encode('utf-8')
		if len(_r) < 2:
			continue
		if _r[0] == teamF and _r[1] == teamT:
			_r = re.findall('<strong class="eng variable">([\d.]*)</strong>', _tr)
			return _r[0]

def countOneMatch(teamF, teamT):
	_tw, _tl = getOneTeamPoint(teamT, True)
	_fw, _fl = getOneTeamPoint(teamF, False)
	_atl, _afl = getAveragePoint()
	_sum = _tw + (_fl - _afl) + _fw + (_tl - _atl)
	_pan = 0
	try:
		_pan = getPanPoint(teamF, teamT)
	except Exception, e:
		_pan = 0
		print 'getPan failed'
		print e

	if _pan == None:
		_pan = 0
		print 'getPan failed'
		
	_sub = float(_sum) - float(_pan)

	print '%s\t\twin - %.2f,\tlose - %.2f' %(teamF, _fw, _fl)
	print '%s\t\twin - %.2f,\tlose - %.2f' %(teamT, _tw, _tl)
	print 'average\t\ttl - %.2f,\tfl - %.2f' %(_atl, _afl)
	print 'sum point\t%.2f' %_sum
	# print _sum 
	# print 'pan point\t%.2f' %_pan
	# print _pan
	print 'sub\t\t%.2f:' %_sub
	if _sub > 0:
		print u'预测大'
	elif _sub < 0:
		print u'预测小'
	else:
		print u'平分'
	# isAgain(teamF)
	# isAgain(teamT)
	print '*'*50

def countAllMatch(_match):

	if len(_match) == 0:
		print 'not match today'
		return

	for x in _match:
		_r = re.findall('blank">(.*)</a></td>', x)
		print _r[0], 'vs', _r[1]
		_r = re.findall('team/(\d*)/" ', x)
		countOneMatch(_r[0], _r[1])

def itos(num):
	if num == 0:
		return '0'
	elif num < 10:
		return '0%d' %num
	else:
		return str(num)

def getMatch(_year = 0, _month = 0, _day = 0):

	_cMatch 	  = []
	_content	  = ''
	_sNewGameDate = ''
	# URL = 'http://liansai.500.com/lq/177/proc/'
	if _year == 0 or _month == 0 or _day == 0:
		URL = 'http://liansai.500.com/lq/177/proc/980/0_2013_12/'
		_content = urllib2.urlopen(URL).read()
		_sNewGameDate = m.getTime('%m-%d', m.sumTime(24))
	else:
		_content = open('match/%d-%d.html' %(_year, _month), 'r').read()
		_sNewGameDate = '%s-%s' %(itos(_month), itos(_day))

		
	d = pq(_content)
	_tbody = d('tbody')
	
	_trs = pq(_tbody.eq(0).html())('tr')
	''' find the new game '''
	for x in xrange(len(_trs)):
		_tr = _trs.eq(x).html()
		_r = re.findall('<td>%s ' %_sNewGameDate, _tr)
		if len(_r) == 1:
			''' add the game '''
			_cMatch.append(_tr)

	return _cMatch

def getResult():
	_match = getMatch(2014, 1, 1)
	countAllMatch(_match)

def count():
	checkData()
	getResult()

if __name__ == '__main__':
	count()
	# update()
	# _sYDate = open('cof', 'r').read()



	# COL.collectMatch(2013, 2014)

	