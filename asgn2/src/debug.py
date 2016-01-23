"""

MODULE  : debug.py

Purpose : * All exceptions are defined here.
          * Any debugging/logging functions are defined here.

"""

# List of Imports Begin
# List of Imports End

# Definitions of the exception classes

# Three-Address-Code Exceptions

class InputError3AC(Exception):
    """ Wrong input to instantiate an object of the class Instr3AC """

    def __init__(self, inputTuple, msg=""): # Optional msg
        self.inputTuple = inputTuple
        self.msg = msg

    def __str__(self):
        return repr(self.inputTuple) + " " + self.msg + "\n"
