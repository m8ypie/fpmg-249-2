import unittest

from extrafeatures_database import COMP249Db

# import the modules to be tested
import users, interface
from bottle import request, response


class Test(unittest.TestCase):

    def setUp(self):
        # open an in-memory database for testing
        self.db = COMP249Db(':memory:')
        self.db.create_tables()
        self.db.sample_data()

    def test_hashtags_count(self):
        counted_hashtags = interface.get_counted_hashtags(self.db)
        ordered_hashtags = ['#ax', '#ync', '#aa', '#gquax', '#nrurcdrbq', '#rucaecv', '#swgsdd', '#zocpybi']
        for counted_hashtag, ordered_hashtag in zip(counted_hashtags, ordered_hashtags):
            self.assertEqual(counted_hashtag[0], ordered_hashtag)

    def test_mentions_count(self):
        counted_mentions = interface.get_counted_mentions(self.db)
        ordered_mentions = ['@Contrary', '@Jimbulator', '@Bean', '@Bobalooba']
        for counted_mention, ordered_mention in zip(counted_mentions, ordered_mentions):
            self.assertEqual(counted_mention[0], ordered_mention)

    def test_mentions_track(self):
        message = """
             @Bean @Bean @Bean @Bean @Bean @Jimbulator @Jimbulator @Jimbulator
        """
        interface.post_add(self.db, "Bobalooba", message)
        counted_mentions = interface.get_counted_mentions(self.db)
        ordered_mentions = ['@Bean', '@Jimbulator', '@Contrary', '@Bobalooba']
        for counted_mention, ordered_mention in zip(counted_mentions, ordered_mentions):
            self.assertEqual(counted_mention[0], ordered_mention)

    def test_hashtag_track(self):
        message = """
            #test #test #test #test #test #test #test #test #test #ync #ync #ync #ync 
        """
        interface.post_add(self.db, "Bobalooba", message)
        counted_hashtags = interface.get_counted_hashtags(self.db)
        ordered_hashtags = ['#test', '#ync', '#ax', '#aa', '#gquax', '#nrurcdrbq', '#rucaecv', '#swgsdd', '#zocpybi']
        for counted_hashtag, ordered_hashtag in zip(counted_hashtags, ordered_hashtags):
            self.assertEqual(counted_hashtag[0], ordered_hashtag)

    "TODO - user login"
    "TODO - user list"