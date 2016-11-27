import abc
import typing

from stampman.helpers import mail


class AbstractEmailService(object):
    __metaclass__ = abc.ABCMeta

    _name = "Abstract Service"
    _failure_mode = False
    _config = {}

    @abc.abstractmethod
    def send_email(self, email: mail.Email) -> typing.Dict:
        pass

    def toggle_failure(self) -> bool:
        self._failure_mode = not self._failure_mode
        return self._failure_mode
