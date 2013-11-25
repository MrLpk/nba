#coding=utf-8

import os
import json
from extlibs.MTool import MTool

class P(object):
	"""docstring for P"""
	def __init__(self):
		self.a = 0
		self.b = 0
		self.f = 0
		self.p = 0
		self.s = 0
		self.r = 0
		self.t = 0
		self.path = 'db/wu.db'

	def count_playoffs(self, items):
		_score = 0
		_hscore = 0
		_lscore = 9999
		_times = 0

		for item in items:
			_s = (item['a']*self.a + item['b']*self.b + item['f']*self.f + item['p']*self.p + item['s']*self.s + item['r']*self.r + item['t']*self.t)
			if _s > _hscore:
				_hscore = _s
			if _s < _lscore:
				_lscore = _s

			_score += _s
			_times += 1

			if len(items) > 2:
				_score = _score - _hscore - _lscore
				_times -= 2
		''' 计算平均分 '''
		print ' tt -- ', _times
		_point = _score / float(_times)

		return _point

	def count(self, items):
		_score = 0
		_hscore = 0
		_lscore = 9999
		_times = 0

		for item in items:
			if item['po'] == 0:
				_s = (item['a']*self.a + item['b']*self.b + item['f']*self.f + item['p']*self.p + item['s']*self.s + item['r']*self.r + item['t']*self.t)
				if _s > _hscore:
					_hscore = _s
				if _s < _lscore:
					_lscore = _s

				_score += _s
				_times += 1

				if len(items) > 2:
					_score = _score - _hscore - _lscore
					_times -= 2
		''' 计算平均分 '''
		print ' tt -- ', _times
		_point = _score / float(_times)

		return _point

	def start(self):
		_path = 'db/1/'
		_data = []
		_count = 1

		for x in os.listdir(_path):
			if x == '.DS_Store':
				continue
			_p = _path + '3704.db'
			# print 'path:',  _p
			_f = open(_p, 'r').read()
			_json = json.loads(_f)

			'''view one player'''
			for i in _json:
				_point = self.count(_json[i])
				_playoffsP = self.count_playoffs(_json[i])
				_o = {i:[{'n':_point}, {'o':_playoffsP}]}
				_data.append(_o)
			 	print u'%s -- %f -- %d times' %(i, _point, _count)
			 	print u'%s -- %f -- %d times' %(i, _playoffsP, _count)
			 	_count+=1
			# break
			return
		_json = json.dumps({'p':_data})
		m = MTool()
		m.save(self.path, _json)

	def case1(self):
		self.a = 2
		self.b = 1
		self.f = -1.3
		self.p = 1
		self.s = 0.7
		self.r = 0.65
		self.t = -0.8
		self.path = 'db/case1.db'

if __name__ == '__main__':
	# start()
	p = P()
	p.case1()
	p.start()
	print p.p