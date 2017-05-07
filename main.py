__author__ = 'Steve Cassidy'

from bottle import Bottle, template, static_file, request, response, HTTPError, redirect
import interface
import string
import users
from database import COMP249Db

COOKIE_NAME = 'sessionid'

application = Bottle()
db = COMP249Db()

def determineUser():
    user = users.session_user(db)
    result = {"logged_in": "False"}
    if user is not None:
        users.generate_session(db, user)
        pic = interface.user_get(db,user)[2]
        result = {"logged_in": "True", "nickname": user, "username": user, "picture": pic}
    return result


def get_recent_posts(posts):
    newposts = []
    for post in posts:
        pic = interface.user_get(db, post[2])[2]
        newposts.append((post[1], post[2], interface.post_to_html(post[3]), pic))
    return newposts

@application.route('/')
def index(dic=None):
    if dic is None:
        dic = {"loginFailed": ""}
    posts = get_recent_posts(interface.post_list(db, None))
    dic.update({"posts": posts})
    dic.update(determineUser())
    return template("main.tpl", dic)

@application.route('/users')
def listUsers():
    user = users.list_users(db)
    print("here:",user)
    dic = {
        "loginFailed": "False",
        "users": user
    }
    dic.update(determineUser())
    print(dic)
    return template("listUsers.tpl", dic)

@application.route('/users/<userName:path>')
def userPage(userName):
    posts = get_recent_posts(interface.post_list(db, userName))
    dic = {
            "loginFailed": "False",
            "posts": posts,
            "name": userName,
            "userpic": interface.user_get(db, userName)[2]
          }
    dic.update(determineUser())
    return template("user.tpl", dic)

@application.route('/about')
def about():
    dic = determineUser()
    dic.update({"loginFailed": ""})
    return template('about.tpl', dic)

@application.route("/register")
def register():
    dic = determineUser()
    dic.update({"loginFailed": ""})
    return template("register.tpl", dic)

@application.route('/mentions/<userName:path>')
def mentions(userName):
    posts = get_recent_posts(interface.post_list_mentions(db, userName))
    dic = {"loginFailed": "False", "posts": posts, "name": userName, "userpic": interface.user_get(db, userName)[2]}
    dic.update(determineUser())
    return template("mentions.tpl", dic)

@application.route('/hashtags/<hashtag:path>')
def hashtags(hashtag):
    posts = get_recent_posts(interface.get_hashtags(db, "#" + hashtag))
    dic = {"loginFailed": "False", "posts": posts}
    dic.update(determineUser())
    return template('hashtag.tpl', dic)

@application.route('/static/<filename:path>')
def static(filename):
    return static_file(filename=filename, root='static')

@application.post('/register/user')
def register_user():
    username = request.forms.get("nick")
    password = request.forms.get("password")
    avatar = request.forms.get("avatar")
    users.user_add(db, password, username, avatar)
    return login()

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

@application.post('/register/validation')
def validation():
    username = request.json["nick"]
    result = {}
    if users.valid_user(db, username):
        response.status = 200
        result = {"invalid": "User already exists"}
    else:
        response.status = 200
    return result

@application.get('/mentioncount')
def mention_count():
    return dict(mentions=interface.get_counted_mentions(db))

@application.get('/hashtagcount')
def hashtag_count():
    return dict(hashtags=interface.get_counted_hashtags(db))

@application.post('/logout')
def logout():
    user = users.session_user(db)
    if user is not None:
        users.delete_session(db, user)
    redirect('/', 302)
if __name__ == '__main__':
    application.run(debug=True, port=8010)
