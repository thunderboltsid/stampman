import typing

import sendgrid
from sendgrid.helpers import mail as sg_mail
from stampman.services import base
from stampman.helpers import mail_, config_, exceptions_


class SendgridEmailService(base.AbstractEmailService):
    def __init__(self, config: typing.NamedTuple = None,
                 failure_mode: bool = False, domain: str = None):
        self._failure_mode = True
        if not config or not isinstance(config, config_.ServiceConfig):
            raise TypeError("Unexpected type for config; Expected "
                            "ServiceConfig")
        self._sg_client = sendgrid.SendGridAPIClient(
            apikey=config.api_key)
        self._config = config
        self._domain = domain

    @property
    def failure_mode(self):
        return self._failure_mode

    @property
    def name(self):
        return self._config.name

    @property
    def config(self):
        return self._config

    @property
    def domain(self):
        return self._domain

    def send_email(self, email: mail_.Email) -> bool:
        mail = sg_mail.Mail()
        personalization = sg_mail.Personalization()
        mail.set_from(sendgrid.Email(email.sender[1], email.sender[0]))
        mail.set_subject(email.subject)
        mail.add_content(sg_mail.Content("text/plain", email.content))

        for recipient in email.recipients:
            personalization.add_to(sendgrid.Email(recipient))

        if email.cc:
            for recipient in email.cc:
                personalization.add_cc(sendgrid.Email(recipient))

        if email.bcc:
            for recipient in email.bcc:
                personalization.add_bcc(sendgrid.Email(recipient))

        mail.add_personalization(personalization)
        response = self._sg_client.client.mail.send.post(
            request_body=mail.get())

        if response.status_code in [202, 250]:
            return True
        elif response.status_code == 421:
            raise exceptions_.ServiceRateLimitException(self.name)
        elif response.status_code in [450, 550, 551, 552, 553]:
            exceptions_.InvalidRecipientException(self.name)
        else:
            exceptions_.GenericEmailServiceException(self.name)

        return False
