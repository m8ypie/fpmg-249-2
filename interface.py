"""
Created on Feb 20, 2015

@author: steve cassidy
"""

import re

def post_to_html(content):
    """Convert a post to safe HTML, quote any HTML code, convert
    URLs to live links and spot any @mentions or #tags and turn
    them into links.  Return the HTML string"""



    return content

def post_list(db, usernick=None, limit=50):
    """Return a list of posts ordered by date
    db is a database connection (as returned by COMP249Db())
    if usernick is not None, return only posts by this user
    return at most limit posts (default 50)

    Returns a list of tuples (id, timestamp, usernick, avatar,  content)
    """


def post_list_followed(db, usernick, limit=50):
    """Return a list of posts by user usernick and any users
    followed by them, ordered by date
    db is a database connection (as returned by COMP249Db())
    return at most limit posts (default 50)

    Returns a list of tuples (id, timestamp, usernick, avatar,  content)
    """


def post_list_mentions(db, usernick, limit=50):
    """Return a list of posts that mention usernick, ordered by date
    db is a database connection (as returned by COMP249Db())
    return at most limit posts (default 50)

    Returns a list of tuples (id, timestamp, usernick, avatar,  content)
    """



def post_add(db, usernick, message):
    """Add a new post to the database.
    The date of the post will be the current time and date.

    Return a the id of the newly created post or None if there was a problem"""


def follow_get(db, usernick):
    """Return the followers of this user as a list of nicks"""



def follow_add(db, follower, followed):
    """Add a follows relationship between these two users.
    Both must be valid users, and can't be the same user.
    If all is well, return True, otherwise return False.
    Should not add a duplicate entry, so if already followed,
    just return True."""



def user_get(db, usernick):
    """Get details of a given user
    Return a tuple (nick, avatar) or None if no such
    user can be found"""



def user_add(db, password, nick, avatar):
    """Add a new user to the database"""


def user_list(db):
    """Return a list of users
    as tuples (nick, avatar)"""


def user_clear(db):
    """Remove all users"""
