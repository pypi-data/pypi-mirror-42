"""ratneshpy - Ratnesh python package for work"""

__version__ = '0.1.1'
__author__ = 'Ratnesh Kushwaha <rat.kush@gmail.com>'
__all__ = []

import logging, termcolor
logging.getLogger(__name__).addHandler(logging.NullHandler())

# print("Hi, I am Ratnesh from Emorphis Ratnesh")

termcolor.cprint('Hi, I am Ratnesh from Emorphis Technologies, Indore', 'white', 'on_red', attrs=['blink'])
class MyClass(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("package initialized")
