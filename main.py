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
        result = {"logged_in": "True", "nickname": "Logged in as "+user}
    return result


@application.route('/')
def index(dic=None):
    if dic is None:
        dic = {"loginFailed": ""}
    allposts = '% rebase("index.tpl")\n'
    allposts += '<section class="messaging">'
    posts = interface.post_list(db, None)
    userValues = determineUser()
    dic.update(userValues)
    for post in posts:
        allposts += constructPost(post)
    allposts += '</section>'
    return template(allposts, dic)

@application.route('/users/<userName:path>')
def userPage(userName):
    usersPosts = '% rebase("index.tpl")\n'
    usersPosts += '<section class="messaging">'
    posts = interface.post_list(db, userName)
    pic = interface.user_get(db, userName)[2]
    for post in posts:
        usersPosts += constructPost(post, pic)
    usersPosts += '</section>'
    return template(usersPosts)

@application.route('/about')
def about():
    dic = determineUser()
    dic.update({"loginFailed": ""})
    return template('about.tpl', dic)

@application.route('/mentions/<userName:path>')
def mentions(userName):
    usersPosts = '% rebase("index.tpl")\n'
    usersPosts += '<section class="messaging">'
    postedMentions = interface.post_list_mentions(db, userName)
    for post in postedMentions:
        usersPosts += constructPost(post, interface.user_get(db, post[2])[2])
    usersPosts += '</section>'
    return template(usersPosts)

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



@application.post('/logout')
def logout():
    user = users.session_user(db)
    if user is not None:
        users.delete_session(db, user)
    redirect('/', 302)
if __name__ == '__main__':
    application.run(debug=True, port=8010)
