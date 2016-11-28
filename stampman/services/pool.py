import sys
import logging
import typing

from stampman.services import base, sendgrid, mailgun, mandrill, amazon_ses
from stampman.helpers import mail_, config_, exceptions_


def get_email_service(name: str):
    if name == "sendgrid":
        return sendgrid.SendgridEmailService
    elif name == "mailgun":
        return mailgun.MailgunEmailService
    elif name == "mandrill":
        return mandrill.MandrillEmailService
    elif name == "amazon_ses":
        return amazon_ses.AmazonSESEmailService
    else:
        raise Exception("Unknown and Unsupported service: {}".format(name))


class PooledService(base.AbstractEmailService):
    def __init__(self):
        self._name = "Service Pool"
        self._service_map = {}
        try:
            config_dict = config_.load_json_file("config.json")
            self._pools = config_.get_domain_pools(config_dict)
            for pool in self._pools:
                services = []
                for service in pool.services:
                    services.append(get_email_service(service.name)(
                        config=service))
                self._service_map[pool.api_key] = services

            self._admins = config_.get_admins(config_dict)
            logging.info("Successfully loaded config file.")
        except Exception as e:
            logging.error(
                "Fatal error loading configuration file. {}".format(str(e)))
            sys.exit(1)

    @property
    def pools(self):
        return self._pools

    @property
    def admins(self):
        return self._admins

    def get_pool_from_api_key(self, key: str) -> typing.NamedTuple:
        for pool in self._pools:
            if key == pool.api_key:
                return pool
        raise exceptions_.InvalidServiceApiKeyException(self._name)

    def send_email(self, email: mail_.Email, pool_api_key: str = None):
        enabled_services = self._service_map[pool_api_key]
        unsuccessful_services = {}
        for service in enabled_services:
            if service.failure_mode:
                unsuccessful_services[service.name] = "Failure Mode"
                continue
            try:
                service.send_email(email)
                return {"status": "success",
                        "services_fail": unsuccessful_services,
                        "service_used": service.name}
            except Exception as e:
                logging.exception(e)
                unsuccessful_services[service.name] = str(e)

        return {"status": "failure", "services_fail": unsuccessful_services}
