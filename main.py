__author__ = 'Steve Cassidy'

from bottle import Bottle, template, static_file, request, response, redirect
import interface
import users
from database import COMP249Db

COOKIE_NAME = 'sessionid'

application = Bottle()
db = COMP249Db()


def determine_user():
    """ Determines if the current request contains a session id cookie.
    If so append the user details to a dictionary.
    :return: User details in dictionary
    """
    user = users.session_user(db)
    result = {"logged_in": "False"}
    if user is not None:
        users.generate_session(db, user)
        pic = interface.user_get(db,user)[2]
        result = {
                    "logged_in": "True",
                    "nickname": user,
                    "username": user,
                    "picture": pic
                  }
    return result


def get_recent_posts(posts):
    """ Append user information to each post
    :param posts: The most current posts
    :return: List of posts with user data
    """
    new_posts = []
    for post in posts:
        pic = interface.user_get(db, post[2])[2]
        new_posts.append((post[1], post[2], interface.post_to_html(post[3]), pic))
    return new_posts


@application.route('/')
def index(dic=None):
    """ Return homepage with most current posts from users
    :param dic: Dictionary containing previous request data
    :return: Homepage
    """
    if dic is None:
        dic = {"loginFailed": ""}
    posts = get_recent_posts(interface.post_list(db, None))
    dic.update({"posts": posts})
    dic.update(determine_user())
    return template("main.tpl", dic)


@application.route('/users')
def list_users():
    """ Lists users registered with pssst
    :return: Page listing users
    """
    user = users.list_users(db)
    dic = {
        "loginFailed": "False",
        "users": user
    }
    dic.update(determine_user())
    return template("listUsers.tpl", dic)


@application.route('/users/<user_name:path>')
def user_page(user_name):
    """ Gets user page with all recent posts
    :param user_name: The username of the user
    :return: The users page
    """
    posts = get_recent_posts(interface.post_list(db, user_name))
    dic = {
            "loginFailed": "False",
            "posts": posts,
            "name": user_name,
            "userpic": interface.user_get(db, user_name)[2]
          }
    dic.update(determine_user())
    return template("user.tpl", dic)


@application.route('/about')
def about():
    """ The about page
    :return: The about page
    """
    dic = determine_user()
    dic.update({"loginFailed": ""})
    return template('about.tpl', dic)


@application.route("/register")
def register():
    """ The page used to register a new user
    :return: The register page
    """
    dic = determine_user()
    dic.update({"loginFailed": ""})
    return template("register.tpl", dic)


@application.route('/mentions/<user_name:path>')
def mentions(user_name):
    """ Page that contains all posts with the given mention
    :param user_name: The username used in the mention
    :return: A page with posts containing the mention
    """
    posts = get_recent_posts(interface.post_list_mentions(db, user_name))
    dic = {
        "loginFailed": "False",
        "posts": posts,
        "name": user_name,
        "userpic": interface.user_get(db, user_name)[2]
    }
    dic.update(determine_user())
    return template("mentions.tpl", dic)


@application.route('/hashtags/<hashtag:path>')
def hashtags(hashtag):
    """ Page that contains all posts with the given hashtag
    :param hashtag: The hashtag
    :return: A page with posts containing the hashtag
    """
    posts = get_recent_posts(interface.get_hashtags(db, "#" + hashtag))
    dic = {
        "loginFailed": "False",
        "posts": posts
    }
    dic.update(determine_user())
    return template('hashtag.tpl', dic)


@application.route('/static/<filename:path>')
def static(filename):
    """ Serves all files within the static folder
    :param filename: The file wished to be served
    :return: The file
    """
    return static_file(filename=filename, root='static')


@application.post('/register/user')
def register_user():
    """ Register a new user to the site.
    If the data is invalid fail silently as
    someone is hitting this endpoint directly,
    not through the register page.
    Clientside validation should stop invalid data.
    :return: The main page, with the user logged in.
    """
    username = request.forms.get("nick")
    password = request.forms.get("password")
    avatar = request.forms.get("avatar")
    users.user_add(db, password, username, avatar)
    return login()


@application.post('/login')
def login():
    """ Attempts to login with provided form data.
    If valid set cookie and redirect to homepage.
    If invalid redirect to homepage with login failed message.
    :return: Home page
    """
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
    """ Saves provided post to database
    :return: Home page
    """
    content = request.forms.get("post")
    user = users.session_user(db)
    if user is not None:
        interface.post_add(db, user, content)
    redirect('/')


@application.post('/register/validation')
def validation():
    """ Validation endpoint for frontend registration validation.
    Checks if username exists
    :return: json with invalid field if invalid
    """
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
    """ Gets trending mentions
    :return: List of trending mentions
    """
    return dict(mentions=interface.get_counted_mentions(db))


@application.get('/hashtagcount')
def hashtag_count():
    """ Gets trending hashtags
    :return: List of trending hashtags
    """
    return dict(hashtags=interface.get_counted_hashtags(db))


@application.post('/logout')
def logout():
    """ Removes cookie from user
    :return: The homepage
    """
    user = users.session_user(db)
    if user is not None:
        users.delete_session(db, user)
    redirect('/', 302)


if __name__ == '__main__':
    application.run(debug=True, port=8010)
