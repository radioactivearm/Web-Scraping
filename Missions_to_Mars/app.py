# One Day Man Will Go to Mars
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

app = Flask(__name__)

# setting up connection to mars_mission db
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_mission"
mongo = PyMongo(app)

@app.route("/")
def index():


@app.route("/scrape")
def rocket():


if __name__ == "__main__":
    app.run(debug=True)
