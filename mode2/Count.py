#coding=utf-8
import Collection as COL
from MTool import MTool
import urllib2
from pyquery import PyQuery as pq
import re, json

m = MTool()
m_sDate = m.getTime('%m-%d-%H')
m_lDate = m_sDate.split('-')

def updata():
	COL.collectionAllTeam()

def checkDate():
	_cof = open('cof', 'r').read()
	_temp = _cof.split('-')
	if _temp[0] == m_lDate[0] and _temp[1] == m_lDate[1] and int(_temp[2]) >=15:
		print 'The version is newest --', _cof
	else:
		print 'local version --', _cof
		print 'start to update version...'
		updata()
		f = open('cof', 'w')
		f.write(str(m_sDate))
		f.close()
		print 'update version success, now the version is,', m_sDate

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
	try:
		_pan = getPanPoint(teamF, teamT)
	except Exception, e:
		_pan = 0
		print 'getPan failed'
		print e
	_sub = float(_sum) - float(_pan)

	print teamF, ':', 'win -', _fw, ',lose -', _fl
	print teamT, ':', 'win -', _tw, ',lose -', _tl
	print 'average:', 'tl -', _atl, ',fl -', _afl
	print 'sum point'
	print _sum 
	print 'pan point'
	print _pan
	print 'sub :', _sub
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
		_sNewGameDate = '%s-%s' %(itos(_year), itos(_month))

		
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
	_match = getMatch()
	countAllMatch(_match)

def count():
	checkDate()
	getResult()

if __name__ == '__main__':
	count()






	# COL.collectMatch(2013, 2014)

	