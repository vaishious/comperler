"""
Module : ir_generation
Function : Contains class and function definitions used to perform IR generation
"""

import debug as DEBUG

INT_DATA_TYPE, STR_DATA_TYPE, UNKNOWN_DATA_TYPE = range(3)

### Some nice wrappers for IR Code ###

class CodeIR(object):

    def __init__(self, code, prevIR=None, nextIR=None):

        self.code = code
        self.prevIR = prevIR
        self.nextIR = nextIR

    def __str__(self):
        return self.code

class ListIR(object):

    def __init__(self, code=None):

        self.head = code
        self.tail = code

    def __or__(self, other):

        if other == None:
            return self

        assert(type(other) == ListIR)

        if self.head == None:
            self.head = other.head
            self.tail = other.tail

        else:
            if other.head == None:
                return self

            self.tail.nextIR = other.head
            other.head.prevIR = self.tail

            self.tail = other.tail

        return self

    def PrintIR(self):
        curIR = self.head
        while (curIR != None):
            print curIR
            curIR = curIR.nextIR

def GenCode(string):
    return ListIR(CodeIR(string))

######################################

### Wrapper to store all attributes ###

class Attributes(object):

    def __init__(self):

        self.place = None
        self.code  = None

        # For symbol table
        self.symEntry = None

        # For dereferencing
        self.depthDeref = 0

        # For assign-sep
        self.opCode = None

        # Flags to make life easy
        self.isArrowOp = False
        

######################################

def TempVar():
    if not hasattr(TempVar, "tempVarCount"):
        TempVar.tempVarCount = 0

    TempVar.tempVarCount += 1

    return "t%d"%(TempVar.tempVarCount)

