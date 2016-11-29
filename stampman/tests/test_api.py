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


class TestApiDetail(unittest.TestCase):
    def setUp(self):
        main.app.config['TESTING'] = True
        self._app = main.app.test_client()
        self._pool_api_key = os.environ.get('POOL_API_KEY')
        self._admin_ai_key = os.environ.get('ADMIN_API_KEY')

    def testGetJson(self):
        response = self._app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
