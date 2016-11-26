import unittest
import json

from stampman.helpers import mail


class TestEmail(unittest.TestCase):
    """Tests for the Email helper class"""

    def setUp(self):
        self._valid_sender = ("Test", "test1@sshukla.de")
        self._invalid_sender = ("Test", "this_is_not_a_valid_email_address")
        self._valid_email_list = ["test1@sshukla.de", "test2@sshukla.de"]
        self._invalid_email_list = ["test1@sshukla.de", "t@e.c"]
        self._valid_string = "this_is_a_valid_string"

    def test_empty_sender(self):
        with self.assertRaises(TypeError):
            mail.Email(sender="")

    def test_invalid_sender_address_length(self):
        with self.assertRaises(AssertionError):
            mail.Email(sender=self._invalid_sender)

    def test_invalid_sender_address(self):
        with self.assertRaises(AssertionError):
            mail.Email(sender=self._invalid_sender)

    def test_empty_recipients(self):
        with self.assertRaises(TypeError):
            mail.Email(sender=self._valid_sender, recipients=[])

    def test_invalid_recipients(self):
        with self.assertRaises(AssertionError):
            mail.Email(sender=self._valid_sender,
                       recipients=self._invalid_email_list)

    def test_invalid_subject(self):
        with self.assertRaises(TypeError):
            mail.Email(sender=self._valid_sender,
                       recipients=self._valid_email_list, subject=1)

    def test_invalid_content(self):
        with self.assertRaises(TypeError):
            mail.Email(sender=self._valid_sender,
                       recipients=self._valid_email_list,
                       subject=self._valid_string, content=1)

    def test_invalid_cc(self):
        with self.assertRaises(TypeError):
            mail.Email(sender=self._valid_sender,
                       recipients=self._valid_email_list,
                       subject=self._valid_string, content=self._valid_string,
                       cc="")

    def test_invalid_bcc(self):
        with self.assertRaises(TypeError):
            mail.Email(sender=self._valid_sender,
                       recipients=self._valid_email_list,
                       subject=self._valid_string, content=self._valid_string,
                       cc=self._valid_email_list, bcc="")

    def test_invalid_reply_to(self):
        with self.assertRaises(AssertionError):
            mail.Email(sender=self._valid_sender,
                       recipients=self._valid_email_list,
                       subject=self._valid_string, content=self._valid_string,
                       cc=self._valid_email_list, bcc=self._valid_email_list,
                       reply_to="")

    def test_message_creation(self):
        _message = mail.Email(sender=self._valid_sender,
                              recipients=self._valid_email_list,
                              subject=self._valid_string,
                              content=self._valid_string,
                              cc=self._valid_email_list,
                              bcc=self._valid_email_list,
                              reply_to=self._valid_sender[1])
        self.assertEqual(self._valid_sender[0], _message._from_name)
        self.assertEqual(self._valid_sender[1], _message._from_address)
        self.assertEqual(self._valid_email_list, _message._to)
        self.assertEqual(self._valid_string, _message._subject)
        self.assertEqual(self._valid_string, _message._body)
        self.assertEqual(self._valid_email_list, _message._cc)
        self.assertEqual(self._valid_email_list, _message._bcc)
        self.assertEqual(self._valid_sender[1], _message._reply_to)

    def test_serialization(self):
        _message = mail.Email(sender=self._valid_sender,
                              recipients=self._valid_email_list,
                              subject=self._valid_string,
                              content=self._valid_string,
                              cc=self._valid_email_list,
                              bcc=self._valid_email_list,
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
