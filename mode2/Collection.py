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
			_year = 0
			_month = int(_r[0][0])
			_day = int(_r[0][1])
			if _month > 9:
				_year = 2013
			else:
				_year = 2014
			_r = re.findall('red">(\d*)-(\d*)</b></td>', _tr)
			if isHome:
				_wScore = int(_r[0][1])
				_lScore = int(_r[0][0])
			else:
				_wScore = int(_r[0][0])
				_lScore = int(_r[0][1])
			_obj = {'y':_year, 'm':_month, 'd':_day, 'l':_lScore, 'w':_wScore}
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

def sort(obj, key):
	_items = []
	for _item in obj:
		x = _item[key]
		_items.append(x)
		
	for x in xrange(len(_items)-1):
		for y in xrange(len(_items)-1):
			if _items[y] > _items[y+1]:
				_temp = _items[y]
				_items[y] = _items[y+1]
				_items[y+1] = _temp

	return _items

def count(obj, key):
	_hScore = 0
	_lScore = 9999
	_aScore = 0
	_times  = 0

	_items = sort(obj, key)
	_num = len(_items)
	_num06 = int(_num * 0.6)
	
	if _num%2 == 0:
		if not _num06%2 == 0:
			_num06 = int(_num06+1)
	else:
		if _num06%2 == 0:
			_num06 = int(_num06+1)
	_n1 = (_num - _num06)*0.5
	_n1 = int(_n1)
	_nl = _items[_n1]
	_nh = _items[_n1-1+_num06]

	for _item in _items:
		x = _item
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
	return _eScore, _nh, _nl

def count1(obj, key):
	" mean, median, lmedian, rmedian"
	_hScore = 0
	_lScore = 9999
	_aScore = 0
	_times  = 0

	_items = sort(obj, key)


	_num = len(_items)
	_medianNum = int(_num * 0.5)
	_median = 0
	_lmedian = 0
	_rmedian = 0

	if _num <= 2:
		print 'items must more then 3'
		return 

	if _num%2 == 0:
		_median = (_items[_medianNum] + _items[_medianNum-1])*0.5
		_tempNum = int(_medianNum * 0.5)

		if _medianNum%2 == 0:
			_lmedian = _items[_tempNum]
			_rmedian = _items[(_medianNum) + _tempNum - 1]
		else:
			_lmedian = (_items[_tempNum] + _items[_tempNum+1]) * 0.5
			_rmedian = (_items[_medianNum-1+_tempNum] + _items[_medianNum+_tempNum]) * 0.5
	else:
		_median  = _items[_medianNum]
		_tempNum = int((_medianNum+1) * 0.5)
		if _medianNum%2 == 0:
			_lmedian = _items[_tempNum]
			_rmedian = _items[_medianNum + _tempNum]
		else:
			_lmedian = (_items[_tempNum] + _items[_tempNum-1])*0.5
			_rmedian = (_items[_medianNum + _tempNum] + _items[_medianNum + _tempNum-1])*0.5

	' mean '
	for _item in _items:
		x = _item
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
	mean = _aScore / float(_times)
	return mean, _median, _lmedian, _rmedian

def countOneTeam1(obj):
	_t = obj['t']
	_tw, _twm, _twlm, _twrm = count1(_t, 'w')
	_tl, _tlm, _tllm, _tlrm = count1(_t, 'l')

	_f = obj['f']
	_fw, _fwm, _fwlm, _fwrm = count1(_f, 'w')
	_fl, _flm, _fllm, _flrm = count1(_f, 'l')

	return {'t':{'w':_tw, 'wm':_twm, 'wlm':_twlm, 'wrm':_twrm, 'l':_tl, 'lm':_tlm, 'llm':_tllm, 'lrm':_tlrm}, 
			'f':{'w':_fw, 'wm':_fwm, 'wlm':_fwlm, 'wrm':_fwrm, 'l':_fl, 'lm':_flm, 'llm':_fllm, 'lrm':_flrm}
		   }

def countScore(obj):
	return count(obj, 'w'), count(obj, 'l')

def countOneTeam(obj):
	_t = obj['t']
	_tw, _twh, _twl = count(_t, 'w')
	_tl, _tlh, _tll = count(_t, 'l')

	_f = obj['f']
	_fw, _fwh, _fwl = count(_f, 'w')
	_fl, _flh, _fll = count(_f, 'l')

	return {'t':{'w':_tw, 'wh':_twh, 'wl':_twl, 'l':_tl, 'lh':_tlh, 'll':_tll}, 
			'f':{'w':_fw, 'wh':_fwh, 'wl':_fwl, 'l':_fl, 'lh':_flh, 'll':_fll}
		   }

def countAllTeam():
	''' count every team's point '''
	_allTeam = []
	for x in xrange(1,31):
		PATH = 'db/%d.dt' %x
		_json = open(PATH, 'r').read()
		_obj = json.loads(_json)

		_result = countOneTeam1(_obj) 
		_allTeam.append({str(x):_result})

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


def collectMatch1(startYear, endYear):
	m = MTool()

	for x in xrange(10,13):
		URL = 'http://liansai.500.com/lq/177/proc/980/0_%d_%d/' %(startYear, x)
		print URL
		_content = urllib2.urlopen(URL).read()
		_name = 'match/%d-%d.html' %(startYear, x)
		m.save(_name, _content)

	for x in xrange(1, 5):
		URL = 'http://liansai.500.com/lq/177/proc/980/0_%d_%d/' %(endYear, x)
		print URL
		_content = urllib2.urlopen(URL).read()
		_name = 'match/%d-%d.html' %(endYear, x)
		m.save(_name, _content)

def executMatch(_content):
	d = pq(_content)
	_tbody = d('tbody')
	
	_trs = pq(_tbody.eq(0).html())('tr')

	''' find the new game '''
	_result = []
	for x in xrange(1, len(_trs)):
		_tr = _trs.eq(x).html()
		# print _tr.encode('utf-8')
		_r = re.findall('blank">(.*)</a></td>', _tr)
		print _r[0], 'vs', _r[1]
		return '%s vs %s' %(_r[0], _r[1])


		# _r = re.findall('team/(\d*)/" ', _tr)
		# print _r[0], _r[1]
		# _r = re.findall('<td>(\d{2})-(\d{2}) ', _tr)
		# print _r[0][0], _r[0][1]
		# {'day':30, 'f':'01', 't':'24'}
		# break
		# {'2014':['1':{},'2':{},'3':{},'4':{}],'2013':[]

def collectMatch(startYear, endYear):
	m = MTool()

	for x in xrange(10,13):
		URL = 'http://liansai.500.com/lq/177/proc/980/0_%d_%d/' %(startYear, x)
		print URL
		_content = urllib2.urlopen(URL).read()
		_str = executMatch(_content)
		return _str
		# _name = 'match/%d-%d.html' %(startYear, x)
		# m.save(_name, _content)
		break
	return
	for x in xrange(1, 5):
		URL = 'http://liansai.500.com/lq/177/proc/980/0_%d_%d/' %(endYear, x)
		print URL
		_content = urllib2.urlopen(URL).read()
		_name = 'match/%d-%d.html' %(endYear, x)
		m.save(_name, _content)


def start():
	# getAverage()
	# getTr(1)
	# collectionAllTeam()
	countAllTeam()
	# countAllAverage()
	# getMatch()
	# getResult()
	# isAgain(18)

def update():
	collectionAllTeam()
	countAllTeam()
	countAllAverage()

if __name__ == '__main__':
	# start()
	# collectMatch(2013, 2014)
	# print 6.6%2
	update()