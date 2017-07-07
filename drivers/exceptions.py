"""

software: software data load and check module.

exceptions.py: Exceptions from software module.

"""
import six

import common.service.exceptions as e


class SoftwareException(e.Error):
    if six.PY2:
        def __str__(self):
            return six.text_type(self.message).encode('UTF-8')

class ProductsLoadError(SoftwareException):
    def __init__(self, message=None):
        msg = 'Unable to load products definition from software package'
        if message:
            msg += ": " + message
        super(ProductsLoadError, self).__init__(msg)

class ProductsFormatError(ProductsLoadError):
    def __init__(self, message=None):
        msg = 'Incorrect products package format'
        if message:
            msg += ': ' + message
        super(ProductsFormatError, self).__init__(msg)

class SoftwareLoadError(SoftwareException):
    def __init__(self, message=None):
        msg = 'Unable to load software definition from package'
        if message:
            msg += ": " + message
        super(SoftwareLoadError, self).__init__(msg)


class SoftwareFormatError(SoftwareLoadError):
    def __init__(self, message=None):
        msg = 'Incorrect software package format'
        if message:
            msg += ': ' + message
        super(SoftwareFormatError, self).__init__(msg)
