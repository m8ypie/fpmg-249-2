import unittest
from webtest import TestApp
from database import COMP249Db
import json
import main, users

from random import choice
import bottle

bottle.debug(True)

class Extra_features_functional(unittest.TestCase):

    def setUp(self):
        self.app = TestApp(main.application)
        # init database
        self.db = COMP249Db()
        self.db.create_tables()
        self.db.sample_data(random=False)
        self.users = self.db.users
        self.posts = self.db.posts

    def doRegister(self, user, password, avatar):
        response = self.app.get('/register')
        registerform = response.forms["register"]
        self.assertIsNotNone(registerform, "no register form on page")

        self.assertEqual("/register/user", registerform.action, "register form action should be /register/user")

        self.assertIn("nick", registerform.fields)
        self.assertIn("password", registerform.fields)
        self.assertIn("avatar", registerform.fields)

        registerform["nick"] = user
        registerform["password"] = password
        registerform["avatar"] = avatar

        response = registerform.submit()

        return response

    def makePost(self, post):
        response = self.app.get('/')

        self.assertIn('postform', response)

        form = response.forms['postform']
        self.assertEqual('/post', form.action, "post form action should be '/post'")

        form['post'] = post

        response = form.submit()

        return response

    def test_create_user_and_login(self):
        user = "test12"
        self.doRegister(user, "password123", "")
        mainPage = self.app.get("/")

        # and the message "Logged in as XXX"
        self.assertIn("Logged in as %s" % user, mainPage)

    def test_create_invalid_user(self):
        user = "test12???>?>?"
        self.doRegister(user, "bihsdgfuisd", "")
        mainPage = self.app.get("/")

        self.assertNotIn(users.COOKIE_NAME, self.app.cookies)

    def test_create_user_check_listing(self):
        user = "test12"
        self.doRegister(user, "password123", "")
        userPage = self.app.get("/users")
        profile_pic = "<img src=/static/psst.png class='profile'/>"
        namelink = '<div class=\'name\'><a href="/users/test12">test12</a></div>'

        self.assertIn(profile_pic, userPage)

    def test_mention_trending(self):
        user = "test12"
        self.doRegister(user, "password123", "")
        self.makePost("@Mandible @Mandible @Mandible @Mandible ...u suk")
        self.makePost("@Bobalooba @Bobalooba @Bobalooba ... u aight")
        self.makePost("@Barfoo @Barfoo ...i b watching you")
        mentioncount = self.app.get("/mentioncount")
        self.assertIn('["@Mandible"], ["@Bobalooba"], ["@Barfoo"]', mentioncount)

    def test_hashtag_trending(self):
        user = "test12"
        self.doRegister(user, "password123", "")
        self.makePost("#MandibleSuks #MandibleSuks #MandibleSuks #MandibleSuks")
        self.makePost("#BobaloobaIsAight #BobaloobaIsAight #BobaloobaIsAight")
        self.makePost("#imWatchingBarfoo #imWatchingBarfoo")
        hashtagcount = self.app.get("/hashtagcount")
        self.assertIn('["#MandibleSuks"], ["#BobaloobaIsAight"], ["#imWatchingBarfoo"]', hashtagcount)


if __name__ == "__main__":
    unittest.main()