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
        self.db.sample_data(random=False)
        self.users = self.db.users
        self.posts = self.db.posts

    def test_mentions(self):
        counted_mentions = interface.get_counted_mentions(self)
        for mentions in counted_mentions:
