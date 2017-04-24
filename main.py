__author__ = 'Steve Cassidy'

from bottle import Bottle, template, static_file, request, response, HTTPError, redirect
import interface
import string
import users
from database import COMP249Db

COOKIE_NAME = 'sessionid'

application = Bottle()
db = COMP249Db()

def constructPost(post, pic="/static/psst.png"):
    t = string.Template("""
        <div class='psst'>
            <div class='user'>
                <img src="$source", class='profile'/>
                <div class='name'><a href="/users/$userName">$userName</a></div>
            </div> 
            <div class="timestamp">$timestamp</div>
            <div class="message">$content</div>
        </div>
    """)
    data = {
        "source": pic,
        "timestamp": post[1],
        "userName": post[2],
        "content": interface.post_to_html(post[3])
    }
    return t.substitute(data)

def determineUser():
    user = users.session_user(db)
    result = {"logged_in": "False"}
    if user is not None:
        users.generate_session(db, user)
        pic = interface.user_get(db, user)[2]
        if pic is None:
            pic = "/static/psst.png"
        result = {"logged_in": "True", "nickname": "Logged in as "+user, "username": user, "picture": pic}
    return result


def appendAvatar(posts):
    newposts = []
    for post in posts:
        pic = interface.user_get(db, post[2])[2]
        if pic is None:
            pic = "/static/psst.png"
        newposts.append((post[1], post[2], interface.post_to_html(post[3]), pic))
    return newposts

@application.route('/')
def index(dic=None):
    if dic is None:
        dic = {"loginFailed": ""}
    posts = appendAvatar(interface.post_list(db, None))
    dic.update({"posts": posts})
    dic.update(determineUser())
    return template("main.tpl", dic)

@application.route('/users/<userName:path>')
def userPage(userName):
    posts = appendAvatar(interface.post_list(db, userName))
    dic = {"loginFailed": "False","posts": posts, "name": userName, "userpic": interface.user_get(db, userName)[2]}
    dic.update(determineUser())
    return template("user.tpl", dic)

@application.route('/about')
def about():
    dic = determineUser()
    dic.update({"loginFailed": ""})
    return template('about.tpl', dic)

@application.route('/mentions/<userName:path>')
def mentions(userName):
    posts = appendAvatar(interface.post_list_mentions(db, userName))
    dic = {"loginFailed": "False", "posts": posts, "name": userName, "userpic": interface.user_get(db, userName)[2]}
    dic.update(determineUser())
    return template("mentions.tpl", dic)

@application.route('/static/<filename:path>')
def static(filename):
    return static_file(filename=filename, root='static')


@application.post('/login')
def login():
    username = request.forms.get("nick")
    password = request.forms.get("password")
    if users.valid_user(db, username) & users.check_login(db, username, password):
        code = 302
        users.generate_session(db, username)
        return redirect('/', code)
    else:
        dic = {"loginFailed": "Login Failed, please try again"}
        return index(dic)

@application.post('/post')
def post():
    content = request.forms.get("post")
    user = users.session_user(db)
    if user is not None:
        interface.post_add(db, user, content)
    redirect('/')

@application.get('/mentioncount')
def mention_count():
    return(str(interface.get_counted_mentions()))

@application.get('/hashtagcount')
def hashtag_count():
    return(str(interface.get_counted_hashtags()))

@application.post('/logout')
def logout():
    user = users.session_user(db)
    if user is not None:
        users.delete_session(db, user)
    redirect('/', 302)
if __name__ == '__main__':
    interface.__init__(db)
    application.run(debug=True, port=8010)
