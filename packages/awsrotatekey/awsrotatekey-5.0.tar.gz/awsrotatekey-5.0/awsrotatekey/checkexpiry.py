from datetime import datetime
from expdict import *

class Expiry:

	def checkexpiry(self, user, validdays):
		
		if(obj3.dateList[1] > obj3.dateList[0]):
			createdate = obj3.dateList[0]
		else:
			createdate = obj3.dateList[1]
		currentdate = datetime.now().replace(microsecond=0)
		delta = currentdate - createdate
		if int(delta.days) >= int(validdays):
			return True
		return False


obj5=Expiry()
