from constants import MapsConstants
import sqlite3
import random

class dateAPI:
	
	def getRandomLocaion(dateId):
		conn=sqlite3.connect('dateDatabase.db')
		curs=conn.cursor()
		resultList = []
		result = []
		for row in curs.execute("SELECT l.lat, l.lon FROM dates d INNER JOIN d2l r on r.da    teId = d.id INNER JOIN locations l on l.id = r.locId where d.id = " + str(dateId)):
			resultList.append(row)
		try:
			result = random.choice(resultList)
		except:
			return [0,0]
		conn.close()
		return result


	def getMap(locArray):
		if(locArray[0] == 0 and locArray[1] == 0):
			return MapsConstants.ERRORIMAGE 
		mapString = "https://maps.googleapis.com/maps/api/staticmap?size=400x400"
		apiKey = MapsConstants.KEY
		marker = "&markers=color:blue%7C" + str(locArray[0]) + "," + str(locArray[1])
		result = mapString + marker + apiKey
		return result

	
	def getRandomDate(isFood, isNotFood, isOutside, isNotOutside, distance, minPrice, maxPrice):
		conn=sqlite3.connect('dateDatabase.db')
		curs=conn.cursor()
		sql = "SELECT * FROM dates WHERE (price > " + str(minPrice) + " AND price < " + st    r(maxPrice) + ") "
		if(isFood == 'True' and not isNotFood == 'True'):
			sql += " AND isFood = 1"
		elif(isNotFood == 'True' and not isFood == 'True'):
			sql += " AND isFood = 0"
		if(isOutside == 'True' and not isNotOutside == 'True'):
			sql += " AND isOutside = 1"
		elif(isNotOutside == 'True' and not isOutside == 'True'):
			sql += " AND isOutside = 0"
		resultList = []
		for row in curs.execute(sql):
			resultList.append(row)
		result = random.choice(resultList)
		conn.close()
		return result

