import unittest
import os

from stampman import main


class TestApiList(unittest.TestCase):
    def setUp(self):
        main.app.config['TESTING'] = True
        self._app = main.app.test_client()
        self._pool_api_key = os.environ.get('POOL_API_KEY')
        self._admin_ai_key = os.environ.get('ADMIN_API_KEY')

    def testGetJson(self):
        response = self._app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self._mail_domain = os.environ.get('MAIL_DOMAIN')

    def testGetJsonWithoutTrailingSlash(self):
        response = self._app.get("")
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response.content_type, "text/html; charset=utf-8")

    def testGetHtml(self):
        response = self._app.get("/", headers={
            "accept": "text/html"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "text/html")


class TestApiDetail(unittest.TestCase):
    def setUp(self):
        main.app.config['TESTING'] = True
        self._app = main.app.test_client()
        self._pool_api_key = os.environ.get('POOL_API_KEY')
        self._admin_ai_key = os.environ.get('ADMIN_API_KEY')
        self._mail_domain = os.environ.get('MAIL_DOMAIN')

    def testGetJsonWithoutTrailingSlash(self):
        response = self._app.get("/{}".format(self._mail_domain))
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response.content_type, "text/html; charset=utf-8")

    def testGetJson(self):
        response = self._app.get("/{}/".format(self._mail_domain))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")

    def testGetHtml(self):
        response = self._app.get("/{}/".format(self._mail_domain),
                                 headers={"accept": "text/html"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "text/html")
