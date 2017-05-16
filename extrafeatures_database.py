import sqlite3
import database

class COMP249Db:
    """
    Provide an interface to the database for a COMP249 web application
    """

    def __init__(self, test=False):
        """
        Construct a database connection.  If test is True, use an
        in-memory database for testing purposes,
        otherwise use a database file called comp249.db
        """

        if test:
            self.dbname = ":memory:"
        else:
            self.dbname = "comp249.db"

        self.conn = sqlite3.connect(self.dbname)

    def cursor(self):
        """Return a cursor on the database"""

        return self.conn.cursor()

    def commit(self):
        """Commit pending changes"""

        self.conn.commit()


    def create_tables(self):
        """Create and initialise the database tables
        This will have the effect of overwriting any existing
        data."""


        sql = """
            DROP TABLE IF EXISTS users;
            CREATE TABLE users (
                       nick text unique primary key,
                       password text,
                       avatar text
            );
            
            DROP TABLE IF EXISTS sessions;
            CREATE TABLE sessions (
                        sessionid text unique primary key,
                        usernick text,
                        FOREIGN KEY(usernick) REFERENCES users(nick)
            );
            
            DROP TABLE IF EXISTS posts;
            CREATE TABLE posts (
                        id integer unique primary key autoincrement,
                        timestamp text default CURRENT_TIMESTAMP,
                        usernick text,
                        content text,
                        FOREIGN KEY(usernick) REFERENCES users(nick)
            );
            
            DROP TABLE IF EXISTS votes;
            CREATE TABLE votes (
                        post text,
                        usernick text,
                        FOREIGN KEY(post) REFERENCES posts(id),
                        FOREIGN KEY(usernick) REFERENCES users(nick)
            );
            
            DROP TABLE IF EXISTS follows;
            CREATE TABLE follows (
                        follower text,
                        followed text,
                        FOREIGN KEY(follower) REFERENCES users(nick),
                        FOREIGN KEY(followed) REFERENCES users(nick)
            );
            
            DROP TABLE IF EXISTS hashtags;
            CREATE TABLE hashtags (
                        postid integer,
                        hashtag text,
                        FOREIGN KEY(postid) REFERENCES posts(id)
            );
            
            DROP TABLE IF EXISTS mentions;
            CREATE TABLE mentions (
                        postid integer,
                        mention text,
                        FOREIGN KEY(postid) REFERENCES posts(id)
            );
            
        """
        self.conn.executescript(sql)
        self.conn.commit()

    def sample_data(self):
        mention_cmd = "INSERT INTO mentions (postid, mention) VALUES (?,?)"
        hashtag_cmd = "INSERT INTO hashtags (postid, hashtag) VALUES (?,?)"
        database.COMP249Db.fixed_data(self)
        hashtags = [
            (1, '#ax'), (1, '#ax'),
            (2, '#ync'), (3, '#ync'),
            (3, '#ax'),  (3, '#ax'),
            (4, '#ync'),  (4, '#aa'),
            (5, '#aa'), (6, '#swgsdd'),
            (7, '#rucaecv'), (8, '#nrurcdrbq'),
            (8, '#gquax'), (8, '#zocpybi')
        ]

        mentions = [
            (2, '@Contrary'),
            (4, '@Bobalooba'),
            (5, '@Contrary'),
            (6, '@Jimbulator'),
            (8, '@Bean'),
            (9, '@Jimbulator')
        ]
        cur = self.cursor()

        for hashtag in hashtags:
            cur.execute(hashtag_cmd, hashtag)

        for mention in mentions:
            cur.execute(mention_cmd, mention)

        self.commit()
