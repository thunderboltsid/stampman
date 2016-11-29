import unittest
import os
import json

from stampman import main
from stampman.helpers import mail_


class TestApiList(unittest.TestCase):
    def setUp(self):
        main.app.config['TESTING'] = True
        self._app = main.app.test_client()
        self._pool_api_key = os.environ.get('POOL_API_KEY')
        self._admin_ai_key = os.environ.get('ADMIN_API_KEY')

    def test_get_json(self):
        response = self._app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self._mail_domain = os.environ.get('MAIL_DOMAIN')

    def test_redirect(self):
        response = self._app.get("")
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response.content_type, "text/html; charset=utf-8")

    def test_get_html(self):
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

    def test_redirect(self):
        response = self._app.get("/{}".format(self._mail_domain))
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response.content_type, "text/html; charset=utf-8")

    def test_get_json(self):
        response = self._app.get("/{}/".format(self._mail_domain))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")

    def test_get_html(self):
        response = self._app.get("/{}/".format(self._mail_domain),
                                 headers={"accept": "text/html"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "text/html")


class TestApiSend(unittest.TestCase):
    def setUp(self):
        main.app.config['TESTING'] = True
        self._app = main.app.test_client()
        self._pool_api_key = os.environ.get('POOL_API_KEY')
        self._admin_ai_key = os.environ.get('ADMIN_API_KEY')
        self._mail_domain = os.environ.get('MAIL_DOMAIN')

    def test_get_json(self):
        response = self._app.get("/{}/send/".format(self._mail_domain))
        self.assertEqual(response.status_code, 200)

    def test_redirect(self):
        response = self._app.get("/{}/send".format(self._mail_domain))
        self.assertEqual(response.status_code, 301)

    def test_post(self):
        response = self._app.post("/{}/send/".format(self._mail_domain),
                                  data=json.dumps(dict(
                                          pool_api_key=self._pool_api_key,
                                          from_email="sid@waveroll.io",
                                          from_name="Sid",
                                          subject="test_send_api",
                                          content="this_is_content"
                                  )), content_type="application/json")
        self.assertEqual(response.status_code, 200)
