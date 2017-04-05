__author__ = 'Steve Cassidy'

from bottle import Bottle, template, static_file, request, response, HTTPError, redirect
import interface
import users
from database import COMP249Db

COOKIE_NAME = 'sessionid'

application = Bottle()


@application.route('/')
def index():
    info = {
        'title': 'This is the Title',
        'content': 'This is the content.'
    }
    return template('index', info)


@application.route('/static/<filename:path>')
def static(filename):
    return static_file(filename=filename, root='static')


if __name__ == '__main__':
    application.run(debug=True, port=8010)
