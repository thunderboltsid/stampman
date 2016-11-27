from stampman.services import base
from stampman.helpers import mail


class PooledService(base.AbstractEmailService):
    def __init__(self, enabled: tuple(str)):
        self._enabled_services = enabled

    def send_email(self, email: mail.Email):
        pass
