import typing

import requests
from stampman.services import base
from stampman.helpers import config_, mail_, exceptions_


class MailgunEmailService(base.AbstractEmailService):
    def __init__(self, config: typing.NamedTuple = None,
                 failure_mode: bool = False, domain: str = None):
        self._failure_mode = failure_mode
        if not config or not isinstance(config, config_.ServiceConfig):
            raise TypeError("Unexpected type for config; Expected "
                            "ServiceConfig")
        self._config = config
        self._api_endpoint = "https://api.mailgun.net/v3/{}".format(domain)
        self._domain = domain

    @property
    def name(self):
        return self._config.name

    @property
    def config(self):
        return self._config

    @property
    def domain(self):
        return self._domain

    @property
    def failure_mode(self):
        return self._failure_mode

    def send_email(self, email: mail_.Email):
        payload = {
            "from": "{} <{}>".format(email.sender[0], email.sender[1]),
            "to": ",".join(email.recipients),
            "subject": email.subject,
            "text": email.content,
            "cc": email.cc,
            "bcc": email.bcc
        }

        response = requests.post("{}/messages".format(self._api_endpoint),
                                 data=payload,
                                 auth=("api", self._config.api_key))

        if response.status_code == 200:
            return True
        elif response.status_code == 401:
            raise exceptions_.InvalidServiceApiKeyException(self.name)
        elif response.status_code in [400, 402, 404, 500, 502, 503, 504]:
            raise exceptions_.GenericEmailServiceException(self.name)

        return False
