import collections
import typing
import json

from stampman.helpers import exceptions
from stampman.services import sendgrid, mailgun, mandrill, amazon_ses

ServiceConfig = collections.namedtuple("ServiceConfig",
                                       ["name", "api_key", "priority",
                                        "email_service"])

Pool = collections.namedtuple("Pool", ["domain", "api_key", "services"])


def load_json_file(path_to_file: str) -> typing.Dict:
    if not isinstance(path_to_file, str):
        raise TypeError("Unexpected File path type; Expected str")

    try:
        with open(path_to_file, 'r') as file:
            json_obj = json.loads(file.read())
    except ValueError:
        raise exceptions.JSONMarshallingError(
            "Unable to load JSON file {}; Please check the syntax".format(
                path_to_file))

    return json_obj


def get_domain_pools(config_dict: typing.Dict) -> typing.List:
    pools = []
    for pool in config_dict["pools"]:
        pools.append(Pool(domain=pool["domain"], api_key=pool["api_key"],
                          services=extract_enabled_service_config(
                              pool["services"])))

    return pools


def extract_enabled_service_config(pool: typing.Dict) -> typing.List:
    services = []
    for service, config in pool.items():
        if config["enabled"] is True:
            services.append(ServiceConfig(name=service,
                                          api_key=config["api_key"],
                                          priority=config["priority"],
                                          email_service=get_email_service(
                                              service)))
    return services


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
