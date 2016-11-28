import collections
import typing
import json

from stampman.helpers import exceptions_

ServiceConfig = collections.namedtuple("ServiceConfig",
                                       ["name", "api_key", "priority"])

Pool = collections.namedtuple("Pool", ["domain", "api_key", "services"])

Admin = collections.namedtuple("Admin", ["name", "api_key"])


def load_json_file(path_to_file: str) -> typing.Dict:
    if not isinstance(path_to_file, str):
        raise TypeError("Unexpected File path type; Expected str")

    try:
        with open(path_to_file, 'r') as file:
            json_obj = json.loads(file.read())
    except ValueError:
        raise exceptions_.JSONMarshallingError(
            "Unable to load JSON file {}; Please check the syntax".format(
                path_to_file))

    return json_obj


def get_admins(config_dict: typing.Dict) -> typing.List:
    admins = []
    for admin in config_dict["admins"]:
        admins.append(Admin(name=admin["name"], api_key=admin["api_key"]))
    return admins


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
            _service = ServiceConfig(name=service,
                                     api_key=config["api_key"],
                                     priority=config["priority"])
            services.append(_service)
    return services
