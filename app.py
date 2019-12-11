from flask import Flask, render_template, request
from constants import IpConstants
from lightAPI import lightAPI as __lights__
from dateAPI import dateAPI as dates

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
	return render_template('index.html')

@app.route('/lights')
def lights():
	currentColor = __lights__.getCurrentColor()
	templateData = {
		'CurrentColor': currentColor
	}
	return render_template('lights.html', **templateData)

@app.route('/lights', methods=['POST', 'GET'])
def lightForm():
	hexCode = __lights__.getCurrentColor()
	if request.method == 'POST':
		hexCode = request.form.get('colorPick')
		__lights__.changeLights(hexCode)
	templateData = {
		'CurrentColor': hexCode
	}
	return render_template('lights.html', **templateData)

@app.route('/dates', methods=['POST', 'GET'])
def datesForm():
	date = [0, 0, 0, 0, 0]
	if request.method == 'POST':
		isFood = request.form.get('isFood')
		isNotFood = request.form.get('isNotFood')
		isOutside = request.form.get('isOutside')
		isNotOutside = request.form.get('isNotOutside')
		distance = request.form.get('distance')
		minPrice = int(request.form.get('minPrice'))
		maxPrice = int(request.form.get('maxPrice'))
		date = dates.getRandomDate(isFood, isNotFood, isOutside, isNotOutside, distance,     minPrice, maxPrice)
		templateData = {
			'ResultVisable' : "visible",
			'DateName' : date[1],
			'DatePrice' : '$' + "{:12.2f}".format(date[2]),
			'DateDescription' : 'Is food' if date[3] else 'Is not food',
			'LocationName' : 'Is outside' if date[4] else 'Is not outside',
			'GoogleMap': dates.getMap(dates.getRandomLocation(date[0]))
		}
	else:
		templateData = {
			'ResultVisable': 'hidden'
		}
	return render_template('dates.html', **templateData)



if __name__ == '__main__':
	app.run(debug=True, host=IpConstants.__IP__, port=IpConstants.__PORT__)
