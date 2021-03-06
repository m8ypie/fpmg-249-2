'''
Created on Mar 26, 2012

@author: steve
'''

import bottle, hashlib, uuid, re

# this variable MUST be used as the name for the cookie used by this application
COOKIE_NAME = 'sessionid'


def check_login(db, usernick, password):
    """ Check if the provided password matches the stored hash for the given user
    :param db: The database instance
    :param usernick: The username of the user
    :param password: The password provided for comparision
    :return: True if it matches, False otherwise
    """
    cur = db.cursor()
    cur.execute("SELECT password FROM users WHERE nick=?", (usernick,))
    pw = cur.fetchone()
    answer = False
    if pw is not None:
        answer = pw[0] == hashlib.sha1(password.encode()).hexdigest()
    return answer


def valid_user(db, usernick):
    """ Determine if given user currently exists
    :param db: The database instance
    :param usernick: The username of the user
    :return: True if the user exists, False otherwise
    """
    cur = db.cursor()
    cur.execute("SELECT nick FROM users WHERE nick=?", (usernick,))
    user = cur.fetchone()
    return user is not None


def get_chunks(l, n):
    """ Split a linear list into a list of lists which contain n elements
    :param l: The linear list
    :param n: The number of elements in each list
    :return: A list of lists
    """
    for i in range(0, len(l), n):
        yield l[i:i + n]


def list_users(db, limit=50):
    """ Return a list of users within a limit (default 50)
    :param db: The database instance
    :param limit: The size limit of the retunr list
    :return: A list of lists containing 4 users
    """
    cur = db.cursor()
    cur.execute("SELECT nick, avatar FROM users")
    users = cur.fetchall()
    if len(users) > limit:
        users = users[:limit]
    return list(get_chunks(users, 4))


def getSession(db, usernick):
    """ Get the session id which corresponds to the provided username
    :param db: The database instance
    :param usernick: The username
    :return: The session id
    """
    cur = db.cursor()
    cur.execute("SELECT sessionId FROM sessions WHERE usernick=?", (usernick,))
    return cur.fetchone()


def getUser(db, session_id):
    """ Get the user who corresponds with the provided session id
    :param db: The database instance
    :param session_id: The session id
    :return: The username
    """
    cur = db.cursor()
    cur.execute("SELECT * FROM sessions")
    cur.execute("SELECT usernick FROM sessions WHERE sessionid = (?)", (session_id,))
    return cur.fetchone()


def createSession(db, usernick):
    """ Create a new session id and add it to the database
    :param db: The database instance
    :param usernick: The user for which the session id is for
    :return: The session id
    """
    session_id = str(uuid.uuid1())
    cur = db.cursor()
    cur.execute("INSERT INTO sessions (sessionid, usernick) VALUES (?,?)", (session_id, usernick))
    db.commit()
    return session_id


def user_add(db, password, nick, avatar):
    """Add a new user to the database"""
    regex = re.compile("^[a-z0-9]+", re.IGNORECASE)
    httpregex = re.compile(r'''(https?://.*.(?:png|jpg))''')
    valid = ((not valid_user(db, nick)) &
             (regex.fullmatch(nick) is not None) &
             ((len(avatar) < 1) | (httpregex.fullmatch(avatar) is not None)))
    if len(avatar) < 1:
        avatar = "/static/psst.png"
    if valid:
        hashedpw = hashlib.sha1(password.encode()).hexdigest()
        cur = db.cursor()
        cur.execute("""INSERT INTO users (nick, password, avatar) VALUES (?,?,?)""", (nick, hashedpw, avatar))
        db.commit()



def generate_session(db, usernick):
    """create a new session and add a cookie to the response object (bottle.response)
    user must be a valid user in the database, if not, return None
    There should only be one session per user at any time, if there
    is already a session active, use the existing sessionid in the cookie
    """
    response = None
    if valid_user(db, usernick):
        session_id = getSession(db, usernick)
        if session_id is None:
            session_id = createSession(db, usernick)
        else:
            session_id = session_id[0]
        response = bottle.response
        response.set_cookie(COOKIE_NAME, str(session_id), path='/')
    return response


def delete_session(db, usernick):
    """remove all session table entries for this user"""
    cur = db.cursor()
    cur.execute("DELETE FROM sessions WHERE usernick=?", (usernick,))
    db.commit()



def session_user(db):
    """try to
    retrieve the user from the sessions table
    return usernick or None if no valid session is present"""
    user = session_id = bottle.request.get_cookie(COOKIE_NAME)
    if session_id is not None:
        user = getUser(db, session_id)
        if user is not None:
            user = user[0]
    return user

