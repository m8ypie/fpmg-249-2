"""
Created on Feb 20, 2015

@author: steve cassidy
"""

import re
import html
import six


def track(regex, message):
    mentions = []
    mention = regex.findall(message)
    if len(mention) > 0:
        for m in mention:
            mentions.append(m)
    return mentions

def track_mentions(db, message, id):
    global countedMentions
    regex = re.compile(r'''((?:@)[A-Za-z]+(\.[A-Za-z]+)?)''')
    mentions = track(regex, message)
    cur = db.cursor()
    for mention in mentions:
        print(mention)
        cur.execute("INSERT INTO mentions (postid, mention) VALUES (?,?)", (id, mention[0]))
    db.commit()

def track_hashtags(db, message, id):
    global countedHashtags
    regex = re.compile(r'''((?:#)[^ <>'"{}|\\^`[\]]*)''')
    mentions = track(regex, message)
    cur = db.cursor()
    print(mentions)
    for mention in mentions:
        cur.execute("INSERT INTO hashtags (postid, hashtag) VALUES (?,?)", (id, mention))
    db.commit()


def track_tags(db, message, id):
    track_mentions(db, message, id)
    track_hashtags(db, message, id)

def post_to_html(content):
    """Convert a post to safe HTML, quote any HTML code, convert
    URLs to live links and spot any @mentions or #tags and turn
    them into links.  Return the HTML string"""
    content = html.escape(content, False)
    content = re.compile(r'''((?:http://)[^ <>'"{}|\\^`[\]]*)''').sub(r"<a href='\1'>\1</a>", content)
    content = re.compile(r'''((?:@)[A-Za-z]+(\.[A-Za-z]+)?)''').sub(r"<a href='/users/\1'>\1</a>", content)
    content = content.replace("/users/@","/users/")
    content = re.compile(r'''((?:#)[^ <>'"{}|\\^`[\]]*)''').sub(r"<strong class='hashtag'>\1</strong>", content)
    return content


def post_list(db, usernick=None, limit=50):
    """Return a list of posts ordered by date
    db is a database connection (as returned by COMP249Db())
    if usernick is not None, return only posts by this user
    return at most limit posts (default 50)

    Returns a list of tuples (id, timestamp, usernick, avatar,  content)
    """
    cur = db.cursor()
    if usernick is not None:
        cur.execute("SELECT * FROM posts WHERE usernick=? ORDER BY timestamp DESC", (usernick,))
    else:
        cur.execute("SELECT * FROM posts ORDER BY timestamp DESC")
    posts = cur.fetchall()
    if len(posts) > limit:
        posts = posts[:limit]
    return posts


def post_list_followed(db, usernick, limit=50):
    """Return a list of posts by user usernick and any users
    followed by them, ordered by date
    db is a database connection (as returned by COMP249Db())
    return at most limit posts (default 50)

    Returns a list of tuples (id, timestamp, usernick, avatar,  content)
    """
    cur = db.cursor()
    posts = post_list(db, usernick, limit)
    followers = cur.execute("SELECT follower FROM follows WHERE followed=?", (usernick,)).fetchall()
    for follower in followers:
        posts.append(post_list(db, follower[0], limit))
    return posts


def post_list_mentions(db, usernick, limit=50):
    """Return a list of posts that mention usernick, ordered by date
    db is a database connection (as returned by COMP249Db())
    return at most limit posts (default 50)

    Returns a list of tuples (id, timestamp, usernick, avatar,  content)
    """
    cur = db.cursor()
    allposts = cur.execute("SELECT * FROM posts").fetchall()
    mentions = []
    for post in allposts:
        if post[3].find("@"+usernick) > -1:
            mentions.append(post)
    if len(mentions) > limit:
        mentions = mentions[:mentions]
    return mentions


def post_add(db, usernick, message):
    """Add a new post to the database.
    The date of the post will be the current time and date.

    Return a the id of the newly created post or None if there was a problem"""
    cur = db.cursor()
    if len(message) <= 150:
        cur.execute("""INSERT INTO posts (usernick, content) VALUES (?,?)""", (usernick, message))
        db.commit()
        id = cur.lastrowid
        track_tags(db, message, id)
    return id


def get_counted_hashtags(db,limit=10):
    cur = db.cursor()
    cur.execute("""SELECT hashtag 
                   FROM hashtags 
                   GROUP BY hashtag 
                   ORDER BY COUNT(hashtag) DESC""")
    hashtags = cur.fetchall()
    if len(hashtags) > limit:
        hashtags = hashtags[:limit]
    print("sending hashtags: ", hashtags)
    return hashtags


def get_counted_mentions(db,limit=10):
    cur = db.cursor()
    cur.execute("""SELECT mention 
                   FROM mentions 
                   GROUP BY mention 
                   ORDER BY COUNT(mention) DESC""")
    hashtags = cur.fetchall()
    if len(hashtags) > limit:
        hashtags = hashtags[:limit]
    print("sending mentions: ", hashtags)
    return hashtags

def get_hashtags(db, hashtag, limit=50):
    cur = db.cursor()
    cur.execute("""SELECT *
                   FROM posts
                   WHERE hashtags.hashtag=?
                   AND hashtags.postid=posts.id""", hashtag)
    posts = cur.fetchall()
    if len(posts) > limit:
        posts = posts[:limit]
    return posts

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
    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE nick=?", (usernick,))
    return cur.fetchone()


def user_list(db):
    """Return a list of users
    as tuples (nick, avatar)"""


def user_clear(db):
    """Remove all users"""
