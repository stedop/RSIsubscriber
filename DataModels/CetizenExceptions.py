"""
Exceptions for the CitizenAPI
~~~~~~~~~~~~~~~
:license: MIT
:author: Stephen Dop
"""


class CitizenNotFoundException(Exception):
    """
    If a subscriber isn't found
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)