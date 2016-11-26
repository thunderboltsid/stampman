import typing
import json

import validate_email


def _validate_email(email_address: str, verify: bool = False):
    """Wraps validate_email with some extra validaton."""

    # No E-mail address can be shorter than 6 characters unless root zone
    # and TLD zone enable email addresses.
    if len(email_address) < 6:
        raise AssertionError(
                "Invalid length of E-mail address; E-mail address can not "
                "be less than 6 digits")

    is_valid = validate_email.validate_email(email_address, verify=verify)

    if not is_valid:
        raise AssertionError(
                "E-Mail address is not a valid E-mail address as per RFC-2822: "
                "https://www.ietf.org/rfc/rfc2822.txt")

    return True


class Email(object):
    """Helper Class for creating Email messages."""

    def __init__(self, sender: typing.Tuple[str, str] = None,
                 recipients: typing.List[str] = None,
                 subject: str = None,
                 content: str = None,
                 cc: typing.List[str] = None,
                 bcc: typing.List[str] = None,
                 reply_to: str = None,
                 verify_sender: bool = False,
                 verify_recipients: bool = False,
                 verify_reply_to: bool = False):

        # Enforce the Type of sender
        if not isinstance(sender, tuple) or len(sender) < 2 or len(sender) > 2:
            raise TypeError(
                    "Unexpected type for sender; Expected tuple[name:str, "
                    "email_address:str]")

        # Basic E-mail validation
        _validate_email(sender[1], verify=verify_sender)

        self._from_name = sender[0]
        self._from_address = sender[1]

        # Enforce the Type of recipients
        if not isinstance(recipients, list) or len(recipients) < 1:
            raise TypeError(
                    "Unexpected type for recipients; Expected list["
                    "address:str]")

        # Basic E-mail validation
        for recipient in recipients:
            _validate_email(recipient, verify=verify_recipients)

        self._to = recipients

        # Enforce the Type of subject
        if isinstance(subject, str):
            self._subject = subject
        else:
            raise TypeError("Unexpected type for subject; Expected str")

        # Enforce the Type of E-mail body
        if isinstance(content, str):
            self._body = content
        else:
            raise TypeError("Unexpected type for E-mail content; Expected str")

        # Basic E-mail validation
        if cc is not None:
            # Enforce the Type of CC
            if not isinstance(cc, list):
                raise TypeError(
                        "Unexpected type for CC; Expected list["
                        "address:str]")

            for recipient in cc:
                _validate_email(recipient, verify=verify_recipients)

        self._cc = cc

        if bcc is not None:
            # Enforce the Type of BCC
            if not isinstance(bcc, list):
                raise TypeError(
                        "Unexpected type for BCC; Expected list["
                        "address:str]")

            # Basic E-mail validation
            for recipient in bcc:
                _validate_email(recipient, verify=verify_recipients)

        self._bcc = bcc

        if reply_to is not None:
            _validate_email(reply_to, verify=verify_reply_to)
        self._reply_to = reply_to

    def __str__(self):
        result = {
            "sender": self._from_address,
            "recipients": self._to,
            "subject": self._subject,
            "content": self._body,
            "cc": self._cc,
            "bcc": self._bcc,
            "reply_to": self._reply_to
        }
        return json.dumps(result)
