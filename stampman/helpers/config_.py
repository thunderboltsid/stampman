import collections
import typing
import json

from stampman.helpers import exceptions

ServiceConfig = collections.namedtuple("ServiceConfig",
                                       ["name", "api_key", "priority"])


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
    except Exception:
        raise Exception("Unable to load JSON file.")

    return json_obj


def extract_enabled_service_config(config_dict: typing.Dict):
    services = []
    for service, config in config_dict["services"].items():
        if config["enabled"] is True:
            services.append(ServiceConfig(name=service,
                                          api_key=config["api_key"],
                                          priority=config["priority"]))
    return services
