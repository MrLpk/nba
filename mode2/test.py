

_items = [1,2,3,4,5,6,7,8,9,10,11,12]
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

if __name__ == '__main__':
	start()