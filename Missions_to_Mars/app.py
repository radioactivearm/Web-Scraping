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
    mission_info = mongo.db.mission.find_one()
    return (render_template("index.html", article_title=mission_info['article_title'],
        article_teaser=mission_info['article_teaser'], featured_url=mission_info['featured_url'],
        table=mission_info['table'], title=mission_info['hemisphere']['title'], img_url=mission_info['hemisphere']['img_url']))


@app.route("/scrape")
def rocket():
    mission = mongo.db.mission
    mission_info = scrape_mars.scrape()
    mission.update({}, mission_info, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)