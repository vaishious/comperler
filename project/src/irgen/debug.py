"""
Module : debug
Function : Contains all exception handling and wrappers for error messagess
"""

class PerlTypeError(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return str(self.msg) + "\n"

class PerlNameError(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return str(self.msg) + "\n"

class PerlError(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return str(self.msg) + "\n"
