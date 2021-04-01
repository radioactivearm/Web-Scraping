# One Day Man Will Go to Mars
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# setting up connection to mars_mission db
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_mission"
mongo = PyMongo(app)

@app.route("/")
def index():
    # takes info from mongo database (mars_mission) the colletion is (mission)
    mission_info = mongo.db.mission.find_one()

    # renders the template of index.html with this info filling in the blanks
    return render_template('index.html', mission=mission_info)


@app.route("/scrape")
def rocket():
    # creating collection connection
    mission = mongo.db.mission
    # scraping
    mission_info = scrape_mars.scrape()
    # upserting into db
    mission.update({}, mission_info, upsert=True)
    # redirect back index.html page
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
