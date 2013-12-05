#coding=utf-8
import Collection as COL
from MTool import MTool

m = MTool()
date = m.getTime('%m-%d')

def updata():
	COL.collectionAllTeam()

def checkDate():
	_cof = open('cof', 'r').read()
	if _cof == str(date):
		print 'The version is newest --', _cof
	else:
		print 'local version --', _cof
		print 'start to update version...'
		updata()
		f = open('cof', 'w')
		f.write(str(date))
		f.close()
		print 'update version success, now the version is,', date

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
	# isAgain(teamF)
	# isAgain(teamT)
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

def count():
	checkDate()
	getResult()

if __name__ == '__main__':
	count()