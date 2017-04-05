"""
Created on Mar 3, 2014

@author: steve
"""

import unittest
from webtest import TestApp

# our main application
import main


class Level1FunctionalTests(unittest.TestCase):

    def setUp(self):
        self.app = TestApp(main.application)

    def tearDown(self):
        pass

    def testHomepage(self):
        """As a visitor to the site, when I load the
         home page I see a banner with "Welcome to Psst"."""

        result = self.app.get('/')
        self.assertIn("Welcome to Psst", result)

    def testAboutSiteLink(self):
        """As a visitor to the site, when I load the home page I see a link to another page
called "About this site".
"""

        result = self.app.get('/')
        links = result.html.find_all('a')

        self.assertTrue(any(['About' in l.text for l in links]), "Can't find 'About this site' link")

    def testAboutSitePage(self):
        """As a visitor to the site, when I click on the link "About this site" I am taken to
a page that contains the site manifesto, including the words "Psst is a new, exciting,
messaging service like nothing you've seen before!"
        """

        message = "Psst is a new, exciting, messaging service like nothing you've seen before!"

        result = self.app.get('/')

        newresult = result.click(description="About")

        # now look for our message in the page
        self.assertIn(message, newresult)

    def testPageCSS(self):
        """As a visitor to the site, I notice that all the pages on the site have the same
design with the same colours and fonts used throughout.
        Interpret this as having a CSS file linked in the pages"""

        result = self.app.get('/')
        links = result.html.find_all('link', rel='stylesheet')

        self.assertGreater(len(links), 0, "No CSS stylesheet linked to home page")


if __name__ == "__main__":
    unittest.main()