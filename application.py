from flask import Flask
import os
app = Flask(__name__)

from routes import *

if __name__ == '__main__':
	port = os.environ.get('PORT', 5000)
	app.run(debug=True, port=port)
	