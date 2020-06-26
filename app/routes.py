import json,requests,math,os
from app import app
from flask import render_template,request

WEATHER_KEY = "os.environ.get('WEATHER_KEY')"

@app.route('/')
@app.route('/index')
def index():
    loc_json = json.loads("http://www.geoplugin.net/json.gp?")
    wea_request = requests.get("http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}"
    .format(loc_json['geoplugin_latitude'],loc_json['geoplugin_longitude'],WEATHER_KEY))
    weat_json = json.loads(wea_request.text)
    return render_template("index.html",
    city=loc_json['geoplugin_city'],
    weather=weat_json['weather'][0]['main'],
    temp=math.floor(weat_json['main']['temp']-273)
    )

@app.route('/about')
def about():
    return render_template("about.html")