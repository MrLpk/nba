#coding=utf-8

import urllib2
import re
import json
from pyquery import PyQuery as pq
from MTool import MTool

def getAverage():
	URL = 'http://liansai.500.com/lq/177/rank/'
	_content = urllib2.urlopen(URL).read()

	d = pq(_content)
	_div = d('.t-content')
	_result = re.findall('<td>([\d\.]{4,5})</td>', _div.eq(0).html())

	''' find wrong data '''
	_temp = []
	for x in xrange(len(_result)):
		if float(_result[x]) < 50:
			_temp.append(x)

	''' del wring data'''
	for x in _temp:
		print 'del ', x, _result[x]
		del _result[x]
		
	print 'count ', len(_result)

	str1 = ''
	str2 = ''
	_win = []
	_lose = []
	for x in xrange(len(_result)):
		if not x%2 == 0:
			str2 = _result[x]
			_lose.append(_result[x])
			# print str1, str2
		else:
			str1 = _result[x]
			_win.append(_result[x])

	''' count average '''
	_wScore = 0
	for x in _win:
		_wScore+=float(x)

	_lScore = 0
	for x in _lose:
		_lScore+=float(x)

	_w = _wScore / float(len(_win))
	_l = _lScore / float(len(_lose))
	print 'win -- ', _w
	print 'lose-- ', _l

	return _w, _l

def getTr(num):
	URL = 'http://liansai.500.com/lq/177/rank/'
	_content = urllib2.urlopen(URL).read()

	_div = pq(_content)('.t-content')
	_trs = pq(_div.eq(0).html())('tr')

	# print _trs.eq(0).html()
	for x in xrange(len(_trs)):
		_tr = _trs.eq(x).html()
		_r = re.findall('href="/lq/177/team/(\d*)/"', _tr)
		if len(_r) == 1:
			if int(_r[0]) == num:
				_tds = pq(_tr)('td')
				print _tds.eq(6).html()
				print _tds.eq(7).html()


	# m = MTool()
	# m.save('1.html', _div.eq(0).html().encode('utf-8'))

def getTl():
	pass

def collectionOneTeam(HTMl, isHome = True):
	_tables = pq(HTMl)('.tb')
	_table = _tables.eq(0).html()
	_trs = pq(_table)('tr')

	_data = []
	for x in xrange(len(_trs)-1, -1, -1):
		_tr = _trs.eq(x).html()
		_result = re.findall(u'<td>常规赛</td>', _tr)
		if len(_result) == 1:
			_r = re.findall('<td>(\d{2})-(\d{2}) ', _tr)
			_month = int(_r[0][0])
			_day = int(_r[0][1])
			_r = re.findall('red">(\d*)-(\d*)</b></td>', _tr)
			if isHome:
				_wScore = int(_r[0][1])
				_lScore = int(_r[0][0])
			else:
				_wScore = int(_r[0][0])
				_lScore = int(_r[0][1])
			_obj = {'m':_month, 'd':_day, 'l':_lScore, 'w':_wScore}
			_data.append(_obj)

	return _data

def collectionAllTeam():
	''' view all teams '''
	for x in xrange(1,31):
		zhuURL = 'http://liansai.500.com/lq/177/team/%d/schedule_%d/' %(x, 1)
		keURL  = 'http://liansai.500.com/lq/177/team/%d/schedule_%d/' %(x, 2)

		_zhuContent = urllib2.urlopen(zhuURL).read()
		_keContent  = urllib2.urlopen(keURL).read()

		_zhuObj = collectionOneTeam(_zhuContent)
		_keObj  = collectionOneTeam(_keContent, False)

		_obj = {'t':_zhuObj, 'f':_keObj}
		_json = json.dumps(_obj)
		m = MTool()
		m.save('db/%d.dt' %x, _json)

def count(obj, key):
	_hScore = 0
	_lScore = 9999
	_aScore = 0
	_times  = 0
	for _item in obj:
		x = _item[key]
		_aScore += x
		if x > _hScore:
			_hScore = x
		if x < _lScore:
			_lScore = x
		_times += 1
	''' make the point more secience '''
	if len(obj) > 2:
		_aScore = _aScore - _hScore - _lScore
		_times -= 2
	_eScore = _aScore / float(_times)
	return _eScore

def countScore(obj):
	return count(obj, 'w'), count(obj, 'l')

def countOneTeam(obj):
	_t = obj['t']
	_tw, _tl = countScore(_t)

	_f = obj['f']
	_fw, _fl = countScore(_f)

	return {'t':{'w':_tw, 'l':_tl}, 'f':{'w':_fw, 'l':_fl}}

def countAllTeam():
	''' count every team's point '''
	_allTeam = []
	for x in xrange(1,31):
		PATH = 'db/%d.dt' %x
		_json = open(PATH, 'r').read()
		_obj = json.loads(_json)

		_result = countOneTeam(_obj) 
		_allTeam.append({str(x):_result})
		# break
	_json = json.dumps(_allTeam)
	m = MTool()
	m.save('AScore.dt', _json)

def countAllAverage():
	''' count the average of all '''
	PATH = 'AScore.dt'
	_twAllScore = 0
	_tlAllScore = 0
	_fwAllScore = 0
	_flAllScore = 0
	_times = 0
	_content = open(PATH, 'r').read()
	_object = json.loads(_content)
	for _item in _object:
		for x in _item:
			x = _item[x]
			# print x
			_twAllScore += x['t']['w']
			_tlAllScore += x['t']['l']
			_fwAllScore += x['f']['w']
			_flAllScore += x['f']['l']
			_times += 1

	_twAverageScore = _twAllScore / float(_times)
	_tlAverageScore = _tlAllScore / float(_times)
	_fwAverageScore = _fwAllScore / float(_times)
	_flAverageScore = _flAllScore / float(_times)

	_str = {'tw':_twAverageScore,
			'tl':_tlAverageScore,
			'fw':_fwAverageScore,
			'fl':_flAverageScore
			}
	_json = json.dumps(_str)
	m = MTool()
	m.save('Average.dt', _json)

def getMatch():
	# URL = 'http://liansai.500.com/lq/177/proc/'
	URL = 'http://liansai.500.com/lq/177/proc/980/0_2013_12/'
	_lDate = ''
	_cDate = ''
	_lMatch = []
	_cMatch = []
	_content = urllib2.urlopen(URL).read()

	d = pq(_content)
	_tbody = d('tbody')
		
	_trs = pq(_tbody.eq(0).html())('tr')
	''' find the new game '''
	for x in xrange(len(_trs)):
		_tr = _trs.eq(x).html()
		_r = re.findall('<td>VS</td>', _tr)
		if len(_r) == 1:
			_r = re.findall('<td>([\d-]*) ', _tr)
			if _cDate == '':
				''' make sure today '''
				_cDate = _r[0]
				_cMatch.append(_tr)

				''' make sure yesterday '''
				if x == 1:
					print "it's first day now,you have not fix it"
				else:
					pass
			elif _r[0] == _cDate:
				_cMatch.append(_tr)

	return _cMatch

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
		# print _tr
		if _r[0] == teamF and _r[1] == teamT:
			_r = re.findall('<strong class="eng variable">([\d.]*)</strong>', _tr)
			return _r[0]

def isAgain(num):
	''' see the team has match yesterday '''
	_content = getPan(True)
	_content = pq(_content)('#seldate').eq(0).html()
	_r = re.findall('<option value="(.*)"', _content)[1]
	URL = 'http://trade.500.com/jclq/index.php?playid=277&date=%s' %_r

	_content = urllib2.urlopen(URL).read()
	_content = pq(_content)('.dc_table').eq(1).html()
	_trs = pq(_content)('tr')
	for x in xrange(len(_trs)):
		_tr = _trs.eq(x).html()
		_r = re.findall('177/team/(\d*)/', _tr)
		if _r[0] == str(num) or _r[1] == str(num):
			print num, 'has match yesterday'
			return True

def countOneMatch(teamF, teamT):
	_tw, _tl = getOneTeamPoint(teamT, True)
	_fw, _fl = getOneTeamPoint(teamF, False)
	_pan = getPanPoint(teamF, teamT)
	_atl, _afl = getAveragePoint()
	_sum = _tw + (_fl - _afl) + _fw + (_tl - _atl)
	_sub = float(_sum) - float(_pan)

	print teamF, ':', 'win -', _fw, ',lose -', _fl
	# print _fw, _fl
	print teamT, ':', 'win -', _tw, ',lose -', _tl
	# print _tw, _tl
	print 'average:', 'tl -', _atl, ',fl -', _afl
	# print _atl, _afl
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
	isAgain(teamF)
	isAgain(teamT)
	print '*'*50

def countAllMatch(_match):
	for x in _match:
		_r = re.findall('blank">(.*)</a></td>', x)
		print _r[0], 'vs', _r[1]
		_r = re.findall('team/(\d*)/" ', x)
		countOneMatch(_r[0], _r[1])
		# break

def getResult():
	_match = getMatch()
	countAllMatch(_match)

def start():
	# getAverage()
	# getTr(1)
	# collectionAllTeam()
	# countAllTeam()
	# countAllAverage()
	# getMatch()
	getResult()
	# isAgain(18)


if __name__ == '__main__':
	start()