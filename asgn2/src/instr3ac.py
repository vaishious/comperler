"""

MODULE  : instr3ac.py

Purpose : * Class used to represent an individual instruction in 3AC format 

"""

# List of Imports Begin
import debug as DEBUG
# List of Imports End


class InstrType(object):
    """ Instruction Types : ASSIGN, IFGOTO, GOTO, CALL, RETURN, PRINT """ # Add more afterwards

    # Enum for holding these values
    ASSIGN, IFGOTO, GOTO, CALL, RETURN, PRINT = range(6)

    typeMap = { 
                "="      : ASSIGN,        "assign" : ASSIGN,
                "ifgoto" : IFGOTO,
                "goto"   : GOTO,          "jmp"    : GOTO,
                "call"   : CALL,
                "ret"    : RETURN,        "return" : RETURN,
                "print"  : PRINT,         "printf" : PRINT
              }

    def __init__(self, inpType):
        self.inpType = inpType      # Will be a string

        if not InstrType.typeMap.has_key(inpType):
            raise DEBUG.InputError3AC(inpType, "Instruction type not recognized")
        
        self.instrType = InstrType.typeMap[inpType]

    def is_ASSIGN(self) : return self.instrType == InstrType.ASSIGN
    def is_IFGOTO(self) : return self.instrType == InstrType.IFGOTO
    def is_GOTO(self)   : return self.instrType == InstrType.GOTO
    def is_CALL(self)   : return self.instrType == InstrType.CALL
    def is_RETURN(self) : return self.instrType == InstrType.RETURN
    def is_PRINT(self)  : return self.instrType == InstrType.PRINT


class OperationType(object):
    """ Operation Types : PLUS, MINUS, MULT, DIV, LT, GT, LEQ, GEQ, EQ """ # Will add more later

    # Set up an enum
    PLUS, MINUS, MULT, DIV, LT, GT, LEQ, GEQ, EQ = range(9)

    typeMap = {
                "+"     : PLUS,          "plus"     : PLUS,
                "-"     : MINUS,         "minus"    : MINUS,
                "*"     : MULT,          "mult"     : MULT,       "multiply"    : MULT,
                "/"     : DIV,           "div"      : DIV,        "divide"      : DIV,
                "<"     : LT,            "lt"       : LT,
                ">"     : GT,            "gt"       : GT,
                "<="    : LEQ,           "leq"      : LEQ,
                ">="    : GEQ,           "geq"      : GEQ,
                "=="    : EQ,            "eq"       : EQ
              }

    def __init__(self, inpType):
        self.inpType = inpType      # Will be a string

        if not OperationType.typeMap.has_key(inpType):
            raise DEBUG.InputError3AC(inpType, "Operation type not recognized")
        
        self.opType = OperationType.typeMap[inpType]

    def is_PLUS(self)   : return self.opType == OperationType.PLUS
    def is_MINUS(self)  : return self.opType == OperationType.MINUS
    def is_MULT(self)   : return self.opType == OperationType.MULT
    def is_DIV(self)    : return self.opType == OperationType.DIV
    def is_LT(self)     : return self.opType == OperationType.LT
    def is_GT(self)     : return self.opType == OperationType.GT
    def is_LEQ(self)    : return self.opType == OperationType.LEQ
    def is_GEQ(self)    : return self.opType == OperationType.GEQ
    def is_EQ(self)     : return self.opType == OperationType.EQ

class Instr3AC(object):
    """ An object of this class represents a single instruction in 3AC format """

    # Defining enum-like mnemonics for all instruction types

    def __init__(self, inpTuple):
        self.inpTuple = inpTuple
