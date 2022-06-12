from crypt import methods
from flask import Flask
from flask_pymongo import pymongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/flaskmongodb'

mongo = pymongo(app)

if __name__ == "__main__":
    app.run(debug=True)