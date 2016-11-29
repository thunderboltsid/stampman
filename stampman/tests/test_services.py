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
        self._service = sendgrid.SendgridEmailService(config=self._config,
                                                      domain="mail.waveroll.io"
                                                      )
        self._email = mail_.Email(sender=("Test", "me@sshukla.de"),
                                  recipients=["thunderboltsid@gmail.com"],
                                  subject="test",
                                  content="test_content")

    def test_send_email(self):
        self._service.send_email(self._email)


class TestMailgunEmailService(unittest.TestCase):
    def setUp(self):
        self._config = config_.ServiceConfig("sendgrid",
                                             os.environ.get('MAILGUN_API_KEY'),
                                             1)
        self._service = mailgun.MailgunEmailService(config=self._config)
        self._email = mail_.Email(sender=("Test", "spam@sshukla.de"),
                                  recipients=["test@sshukla.de"],
                                  subject="test",
                                  content="test_content")

    @unittest.expectedFailure
    def test_send_email(self):
        self._service.send_email(self._email)
