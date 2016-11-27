import collections
import typing

ServiceConfig = collections.namedtuple("ServiceConfig",
                                       ["api_key", "priority", "domain"])
