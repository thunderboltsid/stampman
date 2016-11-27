import typing

import sendgrid
from sendgrid.helpers import mail as sg_mail
from stampman.services import base
from stampman.helpers import mail_, config_, exceptions


class SendgridEmailService(base.AbstractEmailService):
    def __init__(self, failure_mode: bool = False,
                 config: typing.NamedTuple = None):
        self._name = "Sendgrid"
        self._failure_mode = failure_mode
        if not config or isinstance(config, config_.ServiceConfig):
            raise TypeError("Unexpected type for conf; Expected ServiceConfig")
        self._sg_client = sendgrid.SendGridAPIClient(
            apikey=config.api_key)
        self._config = config

    def send_email(self, email: mail_.Email) -> bool:
        mail = sg_mail.Mail()
        personalization = sg_mail.Personalization()
        mail.set_from(sendgrid.Email(email.sender[1], email.sender[0]))
        mail.set_subject(email.subject)
        mail.add_content(sg_mail.Content("text/plain", email.content))

        for recipient in email.recipients:
            personalization.add_to(recipient)

        for recipient in email.cc:
            personalization.add_cc(recipient)

        for recipient in email.bcc:
            personalization.add_cc(recipient)

        mail.add_personalization(personalization)
        response = self._sg_client.client.mail.send.post(
            request_body=mail.get())

        if response.status_code in [202, 250]:
            return True
        elif response.status_code == 421:
            raise exceptions.ServiceRateLimitException(self._name)
        elif response.status_code in [450, 550, 551, 552, 553]:
            exceptions.InvalidRecipientException(self._name)
        else:
            exceptions.GenericEmailServiceException(self._name)

        return False
