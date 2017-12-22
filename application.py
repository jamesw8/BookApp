from flask import Flask
import os
app = Flask(__name__)

from routes import *

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', debug=True, port=port)
	