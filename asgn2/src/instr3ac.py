"""

MODULE  : instr3ac.py

Purpose : * Class used to represent an individual instruction in 3AC format 

"""

# List of Imports Begin
import debug as DEBUG
# List of Imports End


class InstrType(object):
    """ Instruction Types : ASSIGN, IFGOTO, GOTO, CALL, RETURN, PRINT, NOP, LABEL """ # Add more afterwards

    # Enum for holding these values
    ASSIGN, IFGOTO, GOTO, CALL, RETURN, PRINT, LABEL, NOP = range(8)

    typeMap = { 
                "="      : ASSIGN,        "assign" : ASSIGN,
                "ifgoto" : IFGOTO,
                "goto"   : GOTO,          "jmp"    : GOTO,
                "call"   : CALL,
                "ret"    : RETURN,        "return" : RETURN,
                "print"  : PRINT,         "printf" : PRINT,
                "label"  : LABEL,         "Label"  : LABEL,
                "nop"    : NOP,           ""       : NOP
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
    def is_LABEL(self)  : return self.instrType == InstrType.LABEL
    def is_NOP(self)    : return self.instrType == InstrType.NOP


class OperationType(object):
    """ Operation Types : PLUS, MINUS, MULT, DIV, LT, GT, LEQ, GEQ, EQ, NONE """ # Will add more later

    # Set up an enum
    PLUS, MINUS, MULT, DIV, LT, GT, LEQ, GEQ, EQ, NONE = range(10)

    typeMap = {
                "+"     : PLUS,          "plus"     : PLUS,
                "-"     : MINUS,         "minus"    : MINUS,
                "*"     : MULT,          "mult"     : MULT,       "multiply"    : MULT,
                "/"     : DIV,           "div"      : DIV,        "divide"      : DIV,
                "<"     : LT,            "lt"       : LT,
                ">"     : GT,            "gt"       : GT,
                "<="    : LEQ,           "leq"      : LEQ,
                ">="    : GEQ,           "geq"      : GEQ,
                "=="    : EQ,            "eq"       : EQ,
                ""      : NONE
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
    def is_NONE(self)   : return self.opType == OperationType.NONE

class Instr3AC(object):
    """ 
        An object of this class represents a single instruction in 3AC format

        Member Variables :

        * Instruction Type : ASSIGN, IFGOTO, GOTO, CALL, RETURN, PRINT

        * Operation Type   : PLUS, MINUS, MULT, DIV, LT, GT, LEQ, GEQ, EQ 

        * Destination      : Where the result is to be stored (Eg: LHS in an assign)

        * Inp1             : Input 1 for the operation

        * Inp2             : Input 2 for the operation. May be omitted

        * Jump Target      : Line ID to jump to in case the type is GOTO or IFGOTO

        * Line ID          : The line id of this instruction 

    """

    def __init__(self, inpTuple):
        self.inpTuple = inpTuple

        # Initialize everything to default values
        self.instrType = InstrType("") 
        self.opType    = OperationType("")
        self.dest      = ""
        self.inp1      = ""
        self.inp2      = ""
        self.lineID    = 0
        self.jmpTarget = None

        # Set line id
        self.lineID    = int(inpTuple[0])                    # Value error raised if input is not an integer
        # Set instruction type
        self.instrType = InstrType(str(inpTuple[1]))         # Custom exception raised in case of error

        if self.instrType.is_IFGOTO(): 
            # Line Number, IFGOTO, OP, inp1, inp2, Target
            DEBUG.Assert(len(inpTuple) == 6, "Expected 6-tuple for ifgoto") 
            self.opType     =  OperationType(str(inpTuple[2]))
            self.inp1       =  str(inpTuple[3])
            self.inp2       =  str(inpTuple[4])
            self.jmpTarget  =  int(inpTuple[5])

        elif self.instrType.is_GOTO():
            # Line Number, Goto, Target
            DEBUG.Assert(len(inpTuple) == 3, "Expected 3-tuple for goto")                       
            self.jmpTarget  = int(inpTuple[2])

        elif self.instrType.is_CALL():
            # Line Number, Call, Label
            DEBUG.Assert(len(inpTuple) == 3, "Expected 3-tuple for call")
            self.jmpTarget  = str(inpTuple[2])               

        elif self.instrType.is_RETURN():
            # Line Number, Return
            DEBUG.Assert(len(inpTuple) == 2, "Expected 2-tuple for return")

        elif self.instrType.is_PRINT() or self.instrType.is_LABEL():
            # Line Number, Print, Input                                
            # Line Number, Label, LabelName
            DEBUG.Assert(len(inpTuple) == 3, "Expected 3-tuple for label") 
            self.inp1 = str(inpTuple[2])

        elif self.instrType.is_ASSIGN():                 
            # Line Number, =, OP, dest, inp1, inp2                 
            # Line Number, =, dest, inp1             
            # Line Number, =, OP, dest, inp1
            DEBUG.Assert(len(inpTuple) >= 4, "Expected 4/5/6-tuple for assign")      
            DEBUG.Assert(len(inpTuple) <= 6, "Expected 4/5/6-tuple for assign")          

            if len(inpTuple) == 4:
                self.dest   = str(inpTuple[2])
                self.inp1   = str(inpTuple[3])

            elif len(inpTuple) == 5:
                self.opType = OperationType(str(inpTuple[2]))
                self.dest   = str(inpTuple[3])
                self.inp1   = str(inpTuple[4])

            else:
                self.opType = OperationType(str(inpTuple[2]))
                self.dest   = str(inpTuple[3])
                self.inp1   = str(inpTuple[4])
                self.inp2   = str(inpTuple[5])
