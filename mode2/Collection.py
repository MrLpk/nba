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

def getMatch():
	URL = 'http://liansai.500.com/lq/177/proc/'
	_lDate = ''
	_cDate = ''
	_lMatch = []
	_cMatch = []
	_content = urllib2.urlopen(URL).read()

	d = pq(_content)
	_tbody = d('tbody')
		
	_trs = pq(_tbody.eq(0).html())('tr')
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

	for x in _cMatch:
		print x


	# m = MTool()
	# m.save('1.html', _tbody.eq(0).html().encode('utf-8'))

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
		print 'x --', x
	if len(obj) > 2:
		_aScore = _aScore - _hScore - _lScore
		_times -= 2
	_eScore = _aScore / float(_times)
	return _eScore

def countScore(obj):
	return count(obj, 'w'), count(obj, 'l')

def countOneTeam(obj):
	_t = obj['t']
	_tw = count(_t, 'w')
	# _tw, _tl = countScore(_t)

	# print '%f -- %f' %(_tw, _tl)

	# _f = obj['f']
	# _fw, _fl = countScore(_t)
	# print '%f -- %f' %(_fw, _fl)

def countAllTeam():
	for x in xrange(1,31):
		PATH = 'db/%d.dt' %x
		_json = open(PATH, 'r').read()
		_obj = json.loads(_json)

		countOneTeam(_obj) 


		break

def start():
	# getAverage()
	# getMatch()
	# getTr(1)
	# collectionAllTeam()
	countAllTeam()

if __name__ == '__main__':
	start()