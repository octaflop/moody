# nra.py
# News Reasoning Agent (NRA)

# This agent will take parsed news arguments and return a colour to indicate
# amount of news and the amount of change in the news. Its performance is
# measured by the user, and is merged into the considerations.

#from moody.dep.bottle import *
import os
import urllib
from bottle import run, route, view, send_file, debug, template, validate, request, post

#Main home router
@route('/')
@view('home')
def serve():
    # The main server function
    # TODO

    return dict(title="It's magic!", subjects=['Buses', 'Maps', 'Trolley'])

# Ajax requests

@route('/ajax/bus/times/:byid')
@validate(byid=int)
def serve_times(byid):
    api_req = "http://m.translink.ca/api/stops/?s=%s" % str(byid)
    api_resp = urllib.urlopen(api_req).read()
    #weird gotcha:
    false = False
    return {'idinfo': eval(api_resp)}

def serve_closest(lat,lon):
    # Prep the API request
    lon = str(round(float(lon), 5))
    lat = str(round(float(lat), 5))
    #(somehow got this backwards)
    api_req = "http://m.translink.ca/api/stops/?f=json&lng=%s&lat=%s" % (lon, lat)
    api_response = urllib.urlopen(api_req).read()
    return eval(api_response)

@route('/ajax/bus/ids/loc/:lat/:lon')
@validate(lat=float, lon=float)
def bus_ids(lat, lon):
    """
    # shows the 5 closest bus stops
    #lat = request.POST['lat']
    #lon = request.POST['lon']       list the next times
    """
    close = serve_closest(lat, lon)
    ids = []
    # get each stop by id
    for i in (range(0,len(close)-1)):
	ids.append(close[i][0])
    #times = []
    # get all times by id
    #for i in range(0,len(ids)-1):
    #    times.append(serve_times(ids[i]))
    
    return {'busids': ids}

# Static files (css and javascript)

#blueprint etc
@route('/static/:filename#.*#')
def static_file(filename):
    CUR = os.getcwd()
    working = CUR + '/static'
    send_file(filename, root=working)

class NRA:
    """The main News Reasoning Agent class"""

    def make_headline(loc, prefs):
        # server code
        return headline

    def make_status_colour(prefs):
        return headline

    def compile_preference():
        return prefs


if __name__ == "__main__":
    #run(host="localhost", port=8080)
    import bottle
    bottle.debug(True)
    run(host="0.0.0.0", port=8080), reloader=True)
