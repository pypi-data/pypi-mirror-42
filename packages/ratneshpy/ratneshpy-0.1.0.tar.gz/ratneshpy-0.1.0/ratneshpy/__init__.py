"""ratneshpy - Ratnesh python package for work"""

__version__ = '0.1.0'
__author__ = 'Ratnesh Kushwaha <rat.kush@gmail.com>'
__all__ = []

import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())


class MyClass(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("package initialized")
