_items = [1,2,3,4,5,6,7]
_num = len(_items)
_medianNum = int(_num * 0.5)
_lmedianNum = 0
_rmedianNum = 0
_median = 0
_lmedian = 0
_rmedian = 0

if _num%2 == 0:
	_tempNum = _tempNum * 0.5 
else:
	_tempNum = (_medianNum*1) + 1
	_tempNum = int(_tempNum*0.5)
	_median = _items[_medianNum]
	if _medianNum%2 == 0:
		_lmedian = _items[_tempNum]
		_rmedianNum = _items[_medianNum + _tempNum]
	else:
		_lmedian = (_items[_tempNum] + _items[_tempNum-1])*0.5
		_rmedianNum = (_items[_medianNum + _tempNum] + _items[_medianNum + _tempNum-1])*0.5



print _items
print _num
print _medianNum
print _lmedianNum
print _rmedianNum
print _median
print _lmedian
print _rmedian