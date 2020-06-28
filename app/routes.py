import json,requests,math,os
from app import app
from flask import render_template,request,redirect,url_for

WEATHER_KEY = os.environ.get('WEATHER_KEY')


def weatDictByLocation(location):
    formatted_city = '%20'.join(location.split(' '))
    wea_request = requests.get("http://api.openweathermap.org/data/2.5/weather?q={}&appid={}".format(formatted_city,WEATHER_KEY))
    return json.loads(wea_request.text)

def weatDictByCoord(lati, longi):
    wea_request = requests.get("http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}"
    .format(lati,longi,WEATHER_KEY))
    return json.loads(wea_request.text)

@app.route('/', methods=['POST','GET'])
@app.route('/index')
def index():

    ## Es posible solucionar esto obteniendo la ciudad del geoplugin y llamando a indexByCity con ese parametro
    ## Sin embargo, usar coordenadas nos asegura una medicion mas precisa de la locacion que queremos.

    if request.method == "POST":
        print (request.form)
        return redirect(url_for('indexByLocation', location = request.form["location"]))
        
    loc_request = requests.get("http://www.geoplugin.net/json.gp?")
    loc_dict = json.loads(loc_request.text)
    weat_dict = weatDictByCoord(loc_dict['geoplugin_latitude'],loc_dict['geoplugin_longitude'])

    return render_template("index.html",
    city=loc_dict['geoplugin_city'],
    image= "static/img/icons/{}.png".format(weat_dict['weather'][0]['icon']),
    description=weat_dict['weather'][0]['description'],
    temp=math.floor(weat_dict['main']['temp']-273)
    )

@app.route('/<location>', methods=['POST','GET'])
def indexByLocation(location):  

    wea_dict = weatDictByLocation(location)
    if "name" in wea_dict and "weather" in wea_dict:
        return render_template("index.html",
        city=wea_dict['name'],
        image= "static/img/icons/{}.png".format(wea_dict['weather'][0]['icon']),
        description=wea_dict['weather'][0]['description'],
        temp=math.floor(wea_dict['main']['temp']-273))
    
    return render_template("unknown.html", location =location)
    
@app.route('/about', methods=['POST','GET'])
def about():
    return render_template("about.html")