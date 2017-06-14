"""

service: service module.

exceptions.py: Exceptions from service module.

"""

_FATAL_EXCEPTION = False


class Error(Exception):
    def __init__(self, message=None):
        super(Error, self).__init__(message)


class ServiceException(Exception):
    """
    Base Exception class.

    """
    msg = "An unknown exception occurred"

    def __init__(self, **kwargs):
        try:
            self._error_string = self.msg % kwargs

        except Exception:
            if _FATAL_EXCEPTION:
                raise
            else:
                self._error_string = self.msg

    def __str__(self):
        return self._error_string


class UnsupportedType(ServiceException):
    # example {"type":"ECOM"}
    msg = "Unsupported type %(type)s"


