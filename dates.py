#Importing a few important tools:
#Flask handles being a server
#Constants are so sensitive info isn't uploaded to github
#Sqlite3 is our database software
#Random for rng generation, mostly for random.choice()
from flask import Flask, render_template, request
from constants import IpConstants, MapsConstants
import sqlite3
import random

#defines the app
app = Flask(__name__)

#Param dateId: The id in the database for the date, picks a randomly linked location.
#Returns result[]: Contains latitude and logitude for the location or 0,0 on error.
def getRandomLocation(dateId):
	conn=sqlite3.connect('dateDatabase.db')
	curs=conn.cursor()
	resultList = []
	result = []
	#SQL selects the lat and lon of any location that is linked to dateId
	for row in curs.execute("SELECT l.lat, l.lon FROM dates d INNER JOIN d2l r on r.dateId = d.id INNER JOIN locations l on l.id = r.locId where d.id = " + str(dateId)):
		resultList.append(row)
	#Picks a random location, if none returns 0,0
	try:
		result = random.choice(resultList)
	except:
		return [0,0]
	conn.close()
	return result

#Param locArray: an array formatted lat, lon (like getRandomLocation returns)
#Returns result: a google static maps api key for the location requested.
def getMap(locArray):
	#If no location was found, use errorimage
	if(locArray[0] == 0 and locArray[1] == 0):
		return MapsConstants.ERRORIMAGE 
	mapString = "https://maps.googleapis.com/maps/api/staticmap?size=400x400"
	#Hiding the api key is good practice
	apiKey = MapsConstants.KEY
	marker = "&markers=color:blue%7C" + str(locArray[0]) + "," + str(locArray[1])
	result = mapString + marker + apiKey
	return result

#Params: bool, bool, bool, bool, int, int, int. Bools denote food/outside, int is distace and price.
#Return result: an object containing all information about a random date.
def getRandomDate(isFood, isNotFood, isOutside, isNotOutside, distance, minPrice, maxPrice):
	conn=sqlite3.connect('dateDatabase.db')
	curs=conn.cursor()
	#sql begining, selects a date object where price is between min and max
	sql = "SELECT * FROM dates WHERE (price > " + str(minPrice) + " AND price < " + str(maxPrice) + ") "
	#logic to decide if only food/outside or no food/outside
	#if both buttons are left unchecked or are both checked the result is anything
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
	#Pick a random date from the possible results
	result = random.choice(resultList)
	conn.close()
	return result

#Default loading (denoted by '/')  sets result to hidden until a date is chosen
@app.route('/')
def index():
	templateData = {
		'ResultVisable' : "hidden",
		
	}
	#render the website with template data replacing data in index.html
	return render_template('index.html', **templateData)

#Loads when a POST is submitted, as in when a input type of submit has been generated
@app.route('/', methods=['POST', 'GET'])
def formSubmit():
	#Placeholder incase getRandomDate fails.
	date = [0, 0, 0, 0, 0]
	#checks if form was posted, then gets all info from the form.
	if request.method == 'POST':
		isFood = request.form.get('isFood')
		isNotFood = request.form.get('isNotFood')
		isOutside = request.form.get('isOutside')
		isNotOutside = request.form.get('isNotOutside')
		distance = request.form.get('distance')
		minPrice = int(request.form.get('minPrice'))
		maxPrice = int(request.form.get('maxPrice'))
		#gets a random date with the form info
		date = getRandomDate(isFood, isNotFood, isOutside, isNotOutside, distance, minPrice, maxPrice)
	#setting result to visible, then formatting the data.
	templateData = {
		'ResultVisable' : "visible",
		'DateName' : date[1],
		'DatePrice' : '$' + "{:12.2f}".format(date[2]),
		'DateDescription' : 'Is food' if date[3] else 'Is not food',
		'LocationName' : 'Is outside' if date[4] else 'Is not outside',
		'GoogleMap': getMap(getRandomLocation(date[0]))
	}
	return render_template('index.html', **templateData)

#starts the server, protecting IP and PORT info, but also making production/testing environments interchangable.
if __name__ == '__main__':
	app.run(debug=True, host=IpConstants.___IP___, port=IpConstants.___PORT___)
