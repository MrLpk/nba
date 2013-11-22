#coding=utf-8

class PlayerScore(object):
	"""docstring for PlayerScore"""
	def __init__(self, arg):
		super(PlayerScore, self).__init__()

		self.time  			= arg[0]	#上场时间
		self.shoot 			= arg[1]	#投篮
		self.three 			= arg[2]	#三分
		self.freeThrow 		= arg[3]	#罚球
		self.frontRebound	= arg[4]	#前场篮板
		self.backRebound	= arg[5]	#后场篮板
		self.allRebound		= arg[6]	#总篮板
		self.assists		= arg[7]	#助攻
		self.steal			= arg[8]	#抢断
		self.black			= arg[9]	#盖帽
		self.turnOver		= arg[10]	#失误
		self.fouls			= arg[11]	#犯规
		self.points			= arg[12]	#得分
		
	def setDate(self, year, month, day):
		self.year	= year
		self.month	= month
		self.day	= day
	
	def getObj(self):
		obj = {
				# 'time':self.time,
				# 'shoot':self.shoot,
				# 'three':self.three,
				# 'freeThrow':self.freeThrow,
				# 'frontRebound':self.frontRebound,
				# 'backRebound':self.backRebound,
				'r':int(self.allRebound),
				'a':int(self.assists),
				's':int(self.steal),
				'b':int(self.black),
				't':int(self.turnOver),
				'f':int(self.fouls),
				'p':int(self.points),
				'y':int(self.year),
				'm':int(self.month),
				'd':int(self.day),
			}
		return obj

	def getAllObj(self):
		obj = {
				'time':self.time,
				'shoot':self.shoot,
				'three':self.three,
				'freeThrow':self.freeThrow,
				'frontRebound':self.frontRebound,
				'backRebound':self.backRebound,
				'allRebound':self.allRebound,
				'assists':self.assists,
				'steal':self.steal,
				'black':self.black,
				'turnOver':self.turnOver,
				'fouls':self.fouls,
				'points':self.points,
				'year':self.year,
				'month':self.month,
				'day':self.day,
			}
		return obj