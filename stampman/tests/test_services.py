import unittest
import os

from stampman.services import pool, sendgrid, mailgun
from stampman.helpers import config_, mail_


class PoolServiceTest(unittest.TestCase):
    def test_creation(self):
        pool.PooledService()


class TestSendgridEmailService(unittest.TestCase):
    def setUp(self):
        self._config = config_.ServiceConfig("sendgrid",
                                             os.environ.get(
                                                     'SENDGRID_API_KEY'), 1)
        self._domain = os.environ.get('MAIL_DOMAIN')
        self._service = sendgrid.SendgridEmailService(config=self._config,
                                                      domain=self._domain)
        self._email = mail_.Email(sender=("Test", "sid@waveroll.io"),
                                  recipients=["thunderboltsid@gmail.com"],
                                  subject="test",
                                  content="test_sendgrid")

    def test_send_email(self):
        self._service.send_email(self._email)


class TestMailgunEmailService(unittest.TestCase):
    def setUp(self):
        self._config = config_.ServiceConfig("sendgrid",
                                             os.environ.get('MAILGUN_API_KEY'),
                                             1)
        self._domain = os.environ.get('MAIL_DOMAIN')
        self._service = mailgun.MailgunEmailService(config=self._config)
        self._email = mail_.Email(sender=("Test", "sid@waveroll.io"),
                                  recipients=["thunderboltsid@gmail.com"],
                                  subject="test",
                                  content="test_mailgun")

    @unittest.expectedFailure
    def test_send_email(self):
        self._service.send_email(self._email)
