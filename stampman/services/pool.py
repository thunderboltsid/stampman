from stampman.services import base, sendgrid, mailgun, mandrill, amazon_ses
from stampman.helpers import mail_, config_


class PooledService(base.AbstractEmailService):
    def __init__(self):
        config_dict = config_.load_json_file("sample_config.json")
        self._pools = config_.get_domain_pools(config_dict)

    def send_email(self, email: mail_.Email):
        pass
