# tests.py

# sandbox

from bottle import route, run, view
@route('/')
@view('home')
def build_subject():
    subjects = ['Buses', 'Schedules', 'News']
    return dict(title='Hello World', subjects=subjects)

run(host='localhost', port=8080)
