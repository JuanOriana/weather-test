import json,requests,math,os
from app import app
from flask import render_template,request

WEATHER_KEY = os.environ.get('WEATHER_KEY')

@app.route('/')
@app.route('/index')
def index():
    loc_request = requests.get("http://www.geoplugin.net/json.gp?ip=95.172.233.72")
    loc_json = json.loads(loc_request.text)
    wea_request = requests.get("http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}"
    .format(loc_json['geoplugin_latitude'],loc_json['geoplugin_longitude'],WEATHER_KEY))
    weat_json = json.loads(wea_request.text)
    return render_template("index.html",
    city=loc_json['geoplugin_city'],
    image= "static/img/icons/{}.png".format(weat_json['weather'][0]['icon']),
    description=weat_json['weather'][0]['description'],
    temp=math.floor(weat_json['main']['temp']-273)
    )

@app.route('/about')
def about():
    return render_template("about.html")