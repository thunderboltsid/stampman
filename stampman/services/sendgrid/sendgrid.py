import typing

from stampman.services import base
from stampman.helpers import mail, config


class SendgridEmailService(base.AbstractEmailService):
    def __init__(self, failure_mode: bool=False,
                 conf: typing.NamedTuple=None):
        self._name = "Sendgrid"
        self._failure_mode = failure_mode
        if not conf or isinstance(conf, config.ServiceConfig):
            raise TypeError("Unexpected type for conf; Expected ServiceConfig")
        else:
            self._config = conf

    def send_email(self, email: mail.Email) -> typing.Dict:
        pass
