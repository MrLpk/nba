import json

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
	_items = sort(obj, key)
	# _items = [1,2,3,4,5,6,7,8,9,10,11,12]
	_num = len(_items)
	_medianNum = int(_num * 0.5)
	_median = 0
	_lmedian = 0
	_rmedian = 0

	if _num <= 2:
		print 'items must more then 3'
		# return 

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

	print _items
	print _num
	print _medianNum
	print _median
	print _lmedian
	print _rmedian

def countOneTeam(obj):
	_t = obj['t']
	# _tw, _twm, _twlm, _twrm = count1(_t, 'w')
	# _tl, _tlm, _tllm, _tlrm = count1(_t, 'l')
	count(_t, 'w')
	count(_t, 'l')

	_f = obj['f']
	# _fw, _fwm, _fwlm, _fwrm = count1(_f, 'w')
	# _fl, _flm, _fllm, _flrm = count1(_f, 'l')
	count(_f, 'w')
	count(_f, 'l')
	# return {'t':{'w':_tw, 'wm':_twm, 'wlm':_twlm, 'wrm':_twrm, 'l':_tl, 'lm':_tlm, 'llm':_tllm, 'lrm':_tlrm}, 
	# 		'f':{'w':_fw, 'wm':_fwm, 'wlm':_fwlm, 'wrm':_fwrm, 'l':_fl, 'lm':_flm, 'llm':_fllm, 'lrm':_flrm}
	# 	   }

def start(_teamNum):
	'test median lmedian rmedian'
	PATH = 'db/%d.dt' %_teamNum
	_json = open(PATH, 'r').read()
	_obj = json.loads(_json)

	_result = countOneTeam(_obj)

if __name__ == '__main__':
	start(15)