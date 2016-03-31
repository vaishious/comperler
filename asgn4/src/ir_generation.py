"""
Module : ir_generation
Function : Contains class and function definitions used to perform IR generation
"""

import debug as DEBUG

INT_DATA_TYPE, STR_DATA_TYPE, UNKNOWN_DATA_TYPE = range(3)

NextInstr = 0
InstrMap = [0]

### Some nice wrappers for IR Code ###

class CodeIR(object):

    def __init__(self, code, prevIR=None, nextIR=None):

        self.code = code
        self.prevIR = prevIR
        self.nextIR = nextIR

        global InstrMap, NextInstr
        InstrMap[NextInstr-1] = self # It has already been increased by 1

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
    global NextInstr, InstrMap

    string = str(NextInstr) + ", " + string
    NextInstr += 1
    InstrMap += [0]

    return ListIR(CodeIR(string))

def Label(string):
    global NextInstr, InstrMap

    string = str(NextInstr) + ", " + string
    NextInstr += 1
    InstrMap += [0]

    return ListIR(CodeIR("label, %s"%(string)))

######################################

### Wrapper to store all attributes ###

class Attributes(object):

    def __init__(self):

        self.place = None
        self.code  = None
        self.booleanExprCode = None

        # For symbol table
        self.symEntry = None

        # For dereferencing
        self.depthDeref = 0

        # For assign-sep
        self.opCode = None

        # For backpatching
        self.truelist = []
        self.falselist = []
        self.nextlist = []
        self.instr = None

        # For backpatching in loops
        self.loop_next_list = {}
        self.loop_last_list = {}
        self.loop_continue_list = {}
        self.loop_redo_list = {}
        self.loopID = ''


        # Flags to make life easy
        self.isArrowOp = False
        self.isBooleanExpression = False

    def DuplicateTo(self, other):
        other.place = self.place
        other.code = self.code
        other.booleanExprCode = self.code
        other.symEntry = self.symEntry
        other.depthDeref = self.depthDeref
        other.opCode = self.opCode
        other.truelist = self.truelist[:]
        other.falselist = self.falselist[:]
        other.nextlist = self.nextlist[:]
        other.instr = self.instr
        other.isArrowOp = self.isArrowOp
        

######################################

######## Backpatching Functions ######

# Let's be inefficient

def MakeList(i):
    return [i]

def Merge(p1, p2):
    return list(set(p1 + p2))

def BackPatch(p, i):
    global InstrMap

    for numInstr in p:
        instr = InstrMap[numInstr]
        instr.code = instr.code.replace('LABEL#REQUIRED', str(i))

######################################

def TempVar():
    if not hasattr(TempVar, "tempVarCount"):
        TempVar.tempVarCount = 0

    TempVar.tempVarCount += 1

    return "t%d"%(TempVar.tempVarCount)

def NewLabel():
    if not hasattr(NewLabel, "labelCount"):
        NewLabel.labelCount = 0

    NewLabel.labelCount += 1

    return "Label%d"%(NewLabel.labelCount)

######################################

