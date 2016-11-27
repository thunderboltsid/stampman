from stampman.services import base, sendgrid, mailgun, mandrill, amazon_ses
from stampman.helpers import mail_


class PooledService(base.AbstractEmailService):
    def __init__(self):
        pass

    def send_email(self, email: mail_.Email):
        pass
