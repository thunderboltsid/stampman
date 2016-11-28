class BaseServiceException(Exception):
    def __init__(self, service: str = None):
        self._service = service

    def __str__(self):
        return "Exception occurred in {}".format(self._service)


class InvalidServiceApiKeyException(BaseServiceException):
    def __str__(self):
        return "{}: {}".format("Invalid Service API Key",
                               super(InvalidServiceApiKeyException,
                                     self).__str__())


class ServiceRateLimitException(BaseServiceException):
    def __str__(self):
        return "{}: {}".format("Reached a rate limit",
                               super(ServiceRateLimitException,
                                     self).__str__())


class InvalidRecipientException(BaseServiceException):
    def __str__(self):
        return "{}: {}".format("Recipient is invalid (or blocked)",
                               super(InvalidRecipientException,
                                     self).__str__())


class GenericEmailServiceException(BaseServiceException):
    def __str__(self):
        return "{}: {}".format("Error with routing E-mail",
                               super(GenericEmailServiceException,
                                     self).__str__())


class JSONMarshallingError(Exception):
    pass
