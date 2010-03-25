# nra.py
# News Reasoning Agent (NRA)

# This agent will take parsed news arguments and return a colour to indicate
# amount of news and the amount of change in the news. Its performance is
# measured by the user, and is merged into the considerations.

#from moody.dep.bottle import *
import os
from bottle import run, route, view, send_file

class Serve:
    @route('/test/:test')
    @view('home')
    def runtest(test):
        # a simple test with no dynamic data
        # prototyping
        stuff = 'hello, you said: %s' % test

        return dict(title=test, subjects=stuff)

    #Main home router
    @route('/')
    @view('home')
    def serve():
        # The main server function
        # TODO

        return dict(title="It's magic!", subjects=['Buses', 'Maps', 'Trolley'])

    # Ajax requests
    @route('/ajax/:request')
    def serve(request):
        # This is where the jQuery will make its calls

        return request



    # Static files (css and javascript)

    #blueprint #TODO
    @route('/static/:filename#.*#')
    def static_file(filename):
        CUR = os.getcwd()
        working = CUR + '/static'
        send_file(filename, root=working)

class NRA:
    """The main News Reasoning Agent class"""

    def find_location():
        # GeoIP code
        # returns latitude and longitude as:

        #agile
        lat = 42.000
        lon = 42.000
        return lat, lon

    def news_processor(loc, prefs):
        # server code
        return news


if __name__ == "__main__":
    run(host="localhost", port=8080)
