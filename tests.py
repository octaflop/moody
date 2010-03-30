# tests.py

# sandbox

from bottle import route, run, view
@route('/')
@view('home')
def build_subject():
    subjects = ['Buses', 'Schedules', 'News']
    return dict(title='Hello World', subjects=subjects)

    @route('/test/:test')
    @view('home')
    def runtest(test):
        # a simple test with no dynamic data
        # prototyping
        stuff = 'hello, you said: %s' % test

        return dict(title=test, subjects=stuff)
        
            @route('/ajax/:requested')
    def serve(request):
        # This is where the jQuery will make its calls
        # Testing reqest
        response = (int(requested) * int(requested) * int(requested)) * 45
        return str(response)

    @route('/ajax/loc:loc')
    @validate(loc=lambda x: map(float, x.split(',')))
    def find_location(loc):
        # GeoIP code
        # returns latitude and longitude as a tuple
        #agile stuff
        # TODO: add postal-code conversion
        lat, lon = loc[0], loc[1]

        return (round(lat, 5), round(lon, 5))
        
        @route('/ajax/bus/')
    def bus_stop_ids():
        # show the closest stop-ids

        lat = 49.27914
        lon = -122.91611
        lon = str(round(float(lon), 5))
        lat = str(round(float(lat), 5))
        api_req = "http://m.translink.ca/api/stops/?f=json&lng=%s&lat=%s" % (lon, lat)
        api_response = urllib.urlopen(api_req).read()
        return eval(api_response)
    
    #@route('/ajax/bus/loc', method='POST')
#@post('/ajax/bus/loc')
#def bus_time():
    """
    # shows the 5 closest bus stops
    #lat = request.POST['lat']
    #lon = request.POST['lon']       list the next times
    """
    # lat, lon = get_location()
    
    #return str(request.POST.getone('lat', '').strip()) + "<br />" + str(request.POST.getone('lon', '').strip())
    #return str(request.POST.get('lat', '').strip()) + "<br />" + str(request.POST.get('lon', '').strip())
#    return str(bottle.request.POST.get('lat', '').strip()) + "<br />" + str(bottle.request.POST.get('lon' ,'').strip())
    #return str(request.POST('lat')) + "<br />" + str(request.POST('lon'))
    #return request.params()

run(host='localhost', port=8080)
