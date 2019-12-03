from flask import Flask, render_template, request
from constants import IpConstants

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=True, host=IpConstants.__IP__, port=IpConstants.__PORT__)
