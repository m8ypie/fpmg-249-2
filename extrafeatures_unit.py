import unittest
import hashlib
from extrafeatures_database import COMP249Db

# import the modules to be tested
import users, interface
from bottle import request, response


class Extra_features_unit(unittest.TestCase):

    def setUp(self):
        # open an in-memory database for testing
        self.db = COMP249Db(':memory:')
        self.db.create_tables()
        self.db.sample_data()

    def test_hashtags_count(self):
        """Test that hashtags are organised and counted correctly"""
        counted_hashtags = interface.get_counted_hashtags(self.db)
        ordered_hashtags = ['#ax', '#ync', '#aa', '#gquax', '#nrurcdrbq', '#rucaecv', '#swgsdd', '#zocpybi']
        for counted_hashtag, ordered_hashtag in zip(counted_hashtags, ordered_hashtags):
            self.assertEqual(counted_hashtag[0], ordered_hashtag)

    def test_mentions_count(self):
        """Test that mentions are organised and counted correctly"""
        counted_mentions = interface.get_counted_mentions(self.db)
        ordered_mentions = ['@Contrary', '@Jimbulator', '@Bean', '@Bobalooba']
        for counted_mention, ordered_mention in zip(counted_mentions, ordered_mentions):
            self.assertEqual(counted_mention[0], ordered_mention)

    def test_mentions_track(self):
        """Test that mentions are organised and counted correctly after a post that contains mentions is added"""
        message = """
             @Bean @Bean @Bean @Bean @Bean @Jimbulator @Jimbulator @Jimbulator
        """
        interface.post_add(self.db, "Bobalooba", message)
        counted_mentions = interface.get_counted_mentions(self.db)
        ordered_mentions = ['@Bean', '@Jimbulator', '@Contrary', '@Bobalooba']
        for counted_mention, ordered_mention in zip(counted_mentions, ordered_mentions):
            self.assertEqual(counted_mention[0], ordered_mention)

    def test_hashtag_track(self):
        """Test that hashtags are organised and counted correctly after a post that contains hashtags is added"""
        message = """
            #test #test #test #test #test #test #test #test #test #ync #ync #ync #ync 
        """
        interface.post_add(self.db, "Bobalooba", message)
        counted_hashtags = interface.get_counted_hashtags(self.db)
        ordered_hashtags = ['#test', '#ync', '#ax', '#aa', '#gquax', '#nrurcdrbq', '#rucaecv', '#swgsdd', '#zocpybi']
        for counted_hashtag, ordered_hashtag in zip(counted_hashtags, ordered_hashtags):
            self.assertEqual(counted_hashtag[0], ordered_hashtag)

    def test_user_valid_login(self):
        """ Test that a valid username and password can be added to user database"""
        user = "test1"
        pw = "pwtest1"
        users.user_add(self.db, pw, user, "")
        cmd = "SELECT * FROM users WHERE nick = ?"
        cur = self.db.cursor()
        cur.execute(cmd, (user,))
        registered_user = cur.fetchall()
        self.assertEqual(len(registered_user), 1)
        registered_user = registered_user[0]
        self.assertEqual(registered_user[0], user)
        self.assertEqual(registered_user[1], hashlib.sha1(pw.encode()).hexdigest())
        self.assertEqual(registered_user[2], "/static/psst.png")

    def test_user_valid_image(self):
        """ Test that a valid username and password and url to image can be added to user database"""
        user = "test1"
        pw = "pwtest1"
        url = "https://upload.wikimedia.org/wikipedia/commons/1/1a/Image_upload_test.jpg"
        users.user_add(self.db, pw, user, url)
        cmd = "SELECT * FROM users WHERE nick = ?"
        cur = self.db.cursor()
        cur.execute(cmd, (user,))
        registered_user = cur.fetchall()
        self.assertEqual(len(registered_user), 1)
        registered_user = registered_user[0]
        self.assertEqual(registered_user[0], user)
        self.assertEqual(registered_user[1], hashlib.sha1(pw.encode()).hexdigest())
        self.assertEqual(registered_user[2], url)

    def test_user_invalid_login_user_exists(self):
        """ Test that a invalid username and password cannot be added to user database"""
        user = "Bobalooba"
        pw = "pwtest1"
        users.user_add(self.db, pw, user, "")
        users.user_add(self.db, pw, user, "")
        cmd = "SELECT * FROM users WHERE nick = ?"
        cur = self.db.cursor()
        cur.execute(cmd, (user,))
        registered_user = cur.fetchall()
        self.assertEqual(len(registered_user), 1)

    def test_user_invalid_login_illegal_username(self):
        """ Test that a invalid username and password cannot be added to user database"""
        user = "test3>>???>?"
        pw = "pwtest1"
        users.user_add(self.db, pw, user, "")
        cmd = "SELECT * FROM users WHERE nick = ?"
        cur = self.db.cursor()
        cur.execute(cmd, (user,))
        registered_user = cur.fetchall()
        self.assertEqual(len(registered_user), 0)

    def test_user_invalid_login_illegal_url(self):
        """ Test that a invalid username and password cannot be added to user database"""
        user = "Bobalooba"
        pw = "pwtest1"
        url = "https://upload.wikimedia.org/wikipedia/commons/1/1a/Image_upload_test"
        users.user_add(self.db, pw, user, url)
        cmd = "SELECT * FROM users WHERE nick = ?"
        cur = self.db.cursor()
        cur.execute(cmd, (user,))
        registered_user = cur.fetchall()
        self.assertEqual(len(registered_user), 0)
