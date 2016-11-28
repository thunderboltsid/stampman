import unittest
import json

import requests
from stampman import main


class TestAPIRoot(unittest.TestCase):
    def setUp(self):
        self._port = "8000"
        self._path = "http://0.0.0.0"
        main.app.config['TESTING'] = True
        self._app = main.app.test_client()

    def testGetJson(self):
        response = self._app.get("/")
        expected_response = [
            {
                "services": [
                    {
                        "name": "mailgun",
                        "priority": 2
                    },
                    {
                        "name": "sendgrid",
                        "priority": 1
                    }
                ],
                "url": "http://localhost/mail.sshukla.de",
                "domain": "mail.sshukla.de"
            }
        ]
        response_dict = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response_dict, expected_response)
