__author__ = 'Steve Cassidy'

from bottle import Bottle, template, static_file, request, response, HTTPError, redirect
import interface
import string
import users
from database import COMP249Db

COOKIE_NAME = 'sessionid'

application = Bottle()
db = COMP249Db()

def constructPost(post):
    t = string.Template("""
        <div class='psst'>
            <div class='user'>
                <img class='profile', src="$source"/>
                <div class='name'><a href="/users/$userName">$userName</a></div>
            </div> 
            <div class="message">$content</div>
        </div>
    """)
    return t.substitute({
        "source":"",
        "userName":post[2],
        "content":interface.post_to_html(post[3])
    })

@application.route('/')
def index():
    allposts = '% rebase("index.tpl")\n'
    allposts += '<section class="messaging">'
    posts = interface.post_list(db, None)
    for post in posts:
        allposts += constructPost(post)
    allposts += '</section>'
    return template(allposts)

@application.route('/about')
def about():
    return template('about.tpl')

@application.route('/static/<filename:path>')
def static(filename):
    return static_file(filename=filename, root='static')


if __name__ == '__main__':
    application.run(debug=True, port=8010)
