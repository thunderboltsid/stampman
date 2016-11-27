import unittest
import json

from stampman.helpers import mail_, config_


class EmailTest(unittest.TestCase):
    """Tests for the Email helper class"""

    def setUp(self):
        self._valid_sender = ("Test", "test1@sshukla.de")
        self._invalid_sender = ("Test", "this_is_not_a_valid_e_mail_address")
        self._valid_e_mail_list = ["test1@sshukla.de", "test2@sshukla.de"]
        self._invalid_e_mail_list = ["test1@sshukla.de", "t@e.c"]
        self._valid_string = "this_is_a_valid_string"

    def test_empty_sender(self):
        with self.assertRaises(TypeError):
            mail_.Email(sender="")

    def test_invalid_sender_address_length(self):
        with self.assertRaises(AssertionError):
            mail_.Email(sender=self._invalid_sender)

    def test_invalid_sender_address(self):
        with self.assertRaises(AssertionError):
            mail_.Email(sender=self._invalid_sender)

    def test_empty_recipients(self):
        with self.assertRaises(TypeError):
            mail_.Email(sender=self._valid_sender, recipients=[])

    def test_invalid_recipients(self):
        with self.assertRaises(AssertionError):
            mail_.Email(sender=self._valid_sender,
                        recipients=self._invalid_e_mail_list)

    def test_invalid_subject(self):
        with self.assertRaises(TypeError):
            mail_.Email(sender=self._valid_sender,
                        recipients=self._valid_e_mail_list, subject=1)

    def test_invalid_content(self):
        with self.assertRaises(TypeError):
            mail_.Email(sender=self._valid_sender,
                        recipients=self._valid_e_mail_list,
                        subject=self._valid_string, content=1)

    def test_invalid_cc(self):
        with self.assertRaises(TypeError):
            mail_.Email(sender=self._valid_sender,
                        recipients=self._valid_e_mail_list,
                        subject=self._valid_string, content=self._valid_string,
                        cc="")

    def test_invalid_bcc(self):
        with self.assertRaises(TypeError):
            mail_.Email(sender=self._valid_sender,
                        recipients=self._valid_e_mail_list,
                        subject=self._valid_string, content=self._valid_string,
                        cc=self._valid_e_mail_list, bcc="")

    def test_invalid_reply_to(self):
        with self.assertRaises(AssertionError):
            mail_.Email(sender=self._valid_sender,
                        recipients=self._valid_e_mail_list,
                        subject=self._valid_string, content=self._valid_string,
                        cc=self._valid_e_mail_list,
                        bcc=self._valid_e_mail_list,
                        reply_to="")

    def test_message_creation(self):
        _message = mail_.Email(sender=self._valid_sender,
                               recipients=self._valid_e_mail_list,
                               subject=self._valid_string,
                               content=self._valid_string,
                               cc=self._valid_e_mail_list,
                               bcc=self._valid_e_mail_list,
                               reply_to=self._valid_sender[1])
        self.assertEqual(self._valid_sender[0], _message._from_name)
        self.assertEqual(self._valid_sender[1], _message._from_address)
        self.assertEqual(self._valid_e_mail_list, _message._to)
        self.assertEqual(self._valid_string, _message._subject)
        self.assertEqual(self._valid_string, _message._body)
        self.assertEqual(self._valid_e_mail_list, _message._cc)
        self.assertEqual(self._valid_e_mail_list, _message._bcc)
        self.assertEqual(self._valid_sender[1], _message._reply_to)

    def test_serialization(self):
        _message = mail_.Email(sender=self._valid_sender,
                               recipients=self._valid_e_mail_list,
                               subject=self._valid_string,
                               content=self._valid_string,
                               cc=self._valid_e_mail_list,
                               bcc=self._valid_e_mail_list,
                               reply_to=self._valid_sender[1])
        expected_output_dict = {
            "sender": _message._from_address,
            "recipients": _message._to,
            "subject": _message._subject,
            "content": _message._body,
            "cc": _message._cc,
            "bcc": _message._bcc,
            "reply_to": _message._reply_to
        }
        self.assertEqual(json.dumps(expected_output_dict), str(_message))


class ConfigTest(unittest.TestCase):
    """Tests for the ServiceConfig helper namedtuple"""

    def setUp(self):
        self._valid_string = "this_is_an_api_key"
        self._valid_domain = "_mail.sshukla.de"
        self._config_file = "sample_config.json"
        self._service = "test_service"
        self._services = {
            "sendgrid": {
                "api_key": "",
                "priority": 1,
                "enabled": True
            },
            "mailgun": {
                "api_key": "",
                "priority": 2,
                "enabled": True
            },
            "mandrill": {
                "api_key": "",
                "priority": 3,
                "enabled": False
            },
            "amazon_ses": {
                "api_key": "",
                "priority": 4,
                "enabled": False
            }
        }

    def test__config_creation(self):
        config = config_.ServiceConfig(name=self._service,
                                       api_key=self._valid_string,
                                       priority=1)
        self.assertEqual(self._service, config.name)
        self.assertEqual(self._valid_string, config.api_key)
        self.assertEqual(1, config.priority)

    def test_config_load(self):
        config_dict = config_.load_json_file(self._config_file)
        services = config_.extract_enabled_service_config(config_dict)
        for service in services:
            for key, value in self._services.items():
                if key == service.name:
                    self.assertEqual(value["api_key"], service.api_key)
                    self.assertEqual(value["priority"], service.priority)
