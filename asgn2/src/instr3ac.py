"""

MODULE  : instr3ac.py

Purpose : * Class used to represent an individual instruction in 3AC format 

Import Acronym : INSTRUCTION

"""

# List of Imports Begin
import re               # For checking type of variable
import debug as DEBUG
import global_objects as G
import registers as REG
import library as LIB
import mips_assembly as ASM
import basic_blocks as BB
# List of Imports End


class InstrType(object):
    """ 
        Instruction Types : 
    
        Straightforward : ASSIGN, IFGOTO, GOTO, CALL, RETURN, PRINT, NOP, LABEL

        Custom          : Declare - Will be used to fix sizes of the arrays

    """


    # Enum for holding these values
    ASSIGN, IFGOTO, GOTO, CALL, RETURN, PRINT, LABEL, DECLARE, NOP = range(9)

    typeMap = { 
                "="       : ASSIGN,        "assign" : ASSIGN,       "ASSIGN"   : ASSIGN,
                "ifgoto"  : IFGOTO,                                 "IFGOTO"   : IFGOTO,
                "goto"    : GOTO,          "jmp"    : GOTO,         "GOTO"     : GOTO, 
                "call"    : CALL,                                   "CALL"     : CALL,
                "ret"     : RETURN,        "return" : RETURN,       "RETURN"   : RETURN,       "RET" : RETURN,
                "print"   : PRINT,         "printf" : PRINT,        "PRINT"    : PRINT,
                "label"   : LABEL,         "Label"  : LABEL,        "LABEL"    : LABEL,
                "declare" : DECLARE,       "decl"   : DECLARE,      "DECLARE"  : DECLARE,
                "nop"     : NOP,           ""       : NOP,          "NOP"      : NOP
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
    def is_DECLARE(self)  : return self.instrType == InstrType.DECLARE
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


class Entity(object):
    """ Used to represent the variables/numbers/strings used in the instruction """

    # Enum for storing the types
    SCALAR_VARIABLE, HASH_VARIABLE, ARRAY_VARIABLE, STRING, NUMBER, NONE = range(6)

    # Rules for identifying each one
    singleQuoteString = r'\'([^\\]|(\\[\s\S]))*?\''
    doubleQuoteString = r'\"([^\\]|(\\[\s\S]))*?\"'
    string            = r'(' + singleQuoteString + r'|' + doubleQuoteString + r')'
    number            = r'\d+'
    identifier        = r'[a-zA-Z_][a-zA-Z0-9_]*'
    arrayAccess       = identifier + r'\[' + number + r'\]'
    hashAccessNumber  = identifier + r'\{' + number + r'\}'
    hashAccessString  = identifier + r'\{' + string + '\}'

    reString         = re.compile(r'^' + string + r'$')
    reNumber         = re.compile(r'^' + number + r'$')
    reScalar         = re.compile(r'^' + identifier + r'$')
    reArray          = re.compile(r'^' + arrayAccess + r'$')
    reHashNum        = re.compile(r'^' + hashAccessNumber + r'$')
    reHashString     = re.compile(r'^' + hashAccessString + r'$')

    def __init__(self, inpString):
        self.inpString = inpString
        self.entity = None
        self.value  = None
        self.key    = None

        if inpString == "":
            self.entity = Entity.NONE

        elif Entity.reNumber.match(inpString): # Is a number
            self.entity = Entity.NUMBER
            self.value  = int(inpString)

        elif Entity.reString.match(inpString): # Is a string
            self.entity = Entity.STRING
            self.value  = repr(inpString)[2:-2]
            G.AsmData.AllocateString(self)

        elif Entity.reScalar.match(inpString): # Is a scalar
            self.entity = Entity.SCALAR_VARIABLE
            self.value  = repr(inpString)[1:-1]

        elif Entity.reArray.match(inpString):  # Is an array
            self.entity = Entity.ARRAY_VARIABLE
            self.value  = repr(inpString[:inpString.find('[')])[1:-1]
            self.key    = Entity(repr(inpString[inpString.find('[')+1:-1])[1:-1])

        elif Entity.reHashNum.match(inpString) or Entity.reHashString.match(inpString): # Is a hashmap
            self.entity = Entity.HASH_VARIABLE
            self.value  = repr(inpString[:inpString.find('{')])[1:-1]
            self.key    = Entity(repr(inpString[inpString.find('{')+1:-1])[1:-1])

        else:
            raise DEBUG.InputError3AC(inpString, "Failed to recognize entity")

    def is_NUMBER(self)          : return self.entity == Entity.NUMBER
    def is_SCALAR_VARIABLE(self) : return self.entity == Entity.SCALAR_VARIABLE
    def is_ARRAY_VARIABLE(self)  : return self.entity == Entity.ARRAY_VARIABLE
    def is_HASH_VARIABLE(self)   : return self.entity == Entity.HASH_VARIABLE
    def is_STRING(self)          : return self.entity == Entity.STRING
    def is_NONE(self)            : return self.entity == Entity.NONE
    def is_VARIABLE(self)        : return (self.entity == Entity.SCALAR_VARIABLE or
                                           self.entity == Entity.HASH_VARIABLE or
                                           self.entity == Entity.ARRAY_VARIABLE)

    def AllocateGlobalMemory(self):
        """ Allocate itself memory in the global region """
        if self.is_SCALAR_VARIABLE():
            G.AsmData.Allocate32(self)

        elif self.is_ARRAY_VARIABLE():
            G.AsmData.AllocateArray(self)

    def IsRegisterAllocated(self):
        """ Reads the current reg-address descriptor and returns a boolean value """
        return True

    def GetCurrReg(self):
        """ Reads the current reg-address descriptor and returns the relevant register """
        return 0

    def CopyToRegister(self, reg):
        """ 
            Copies its value to the given register. If it has been allocated to a register, it uses the move instruction.
            If not, it uses the lw instruction in case it is a scalar/array variable. If it is a number, it uses "li".
            If it is a string, it will use "la". This is used specially for parameter assignments for functions
        """

        if self.is_NUMBER():
            return G.INDENT + "li %s, %s\n"%(reg, str(self.value))

        if self.is_STRING():
            return G.INDENT + "la %s, %s\n"%(reg, ASM.GetStrAddr(self))

        if self.is_SCALAR_VARIABLE():
            if self.IsRegisterAllocated():
                return G.INDENT + "move %s %s\n"%(reg, self.GetCurrReg())
            else:
                return G.INDENT + "lw %s, %s\n"%(reg, ASM.GetVarAddr(self))

    def CopyToMemory(self, mem):
        """
            Copies the value at the given memory location. Instructions used are straightforward. In case it is allocated, 
            we use sw directly. Otherwise we copy it to $v0 and then use sw. Specifically used in parameter assignments.
        """

        if self.IsRegisterAllocated():
            return G.INDENT + "sw %s, %s\n"%(self.GetCurrReg(), mem)

        codeSegment = self.CopyToRegister(REG.v0)
        codeSegment += G.INDENT + "sw %s, %s\n"%(REG.v0, mem)

        return codeSegment

    def ReturnSymbols(self):

        if self.is_SCALAR_VARIABLE():
            return [str(self.value)]

        elif self.is_ARRAY_VARIABLE() or self.is_HASH_VARIABLE():
            ret = [str(self.value)]
            currEntity = self.key
            while (currEntity.is_ARRAY_VARIABLE() or currEntity.is_HASH_VARIABLE()):
                currEntity = currEntity.key

            if currEntity.is_SCALAR_VARIABLE():
                ret += [str(currEntity.value)]

            return ret

        else:
            return []

class Instr3AC(object):
    """ 
        An object of this class represents a single instruction in 3AC format

        Member Variables :

        * Instruction Type : ASSIGN, IFGOTO, GOTO, CALL, RETURN, PRINT

        * Operation Type   : PLUS, MINUS, MULT, DIV, LT, GT, LEQ, GEQ, EQ 

        * Destination      : Where the result is to be stored (Eg: LHS in an assign)

        * Inp1             : Input 1 for the operation

        * Inp2             : Input 2 for the operation. May be omitted

        * PrintArgs        : Store the arguments to Print. Deviation from 3-addr code. Cannot be used for any other instruction

        * Jump Target      : Line ID to jump to in case the type is GOTO or IFGOTO

        * Line ID          : The line id of this instruction 

        * Jump Label       : Label to jump to in case of "call"

        * Label            : Label associated with this instruction

        * Is Target        : Is this a jump target for another instruction?

        * SymTable         : Local symbol table holding info on liveness and next-use 
                             assigned by the basic-block for register allocation

    """

    def __init__(self, inpTuple):
        self.inpTuple = inpTuple

        # Initialize everything to default values
        self.instrType = InstrType("") 
        self.opType    = OperationType("")
        self.dest      = Entity("")
        self.inp1      = Entity("")
        self.inp2      = Entity("")
        self.PrintArgs = []
        self.lineID    = 0
        self.jmpTarget = None
        self.jmpLabel  = None
        self.label     = None
        self.isTarget  = False
        self.symTable  = None
        self.isCopy    = False # Is it of the form x = y

        # Set line id
        self.lineID    = int(inpTuple[0])                    # Value error raised if input is not an integer
        # Set instruction type
        self.instrType = InstrType(str(inpTuple[1]))         # Custom exception raised in case of error

        if self.instrType.is_IFGOTO(): 
            # Line Number, IFGOTO, OP, inp1, inp2, Target
            DEBUG.Assert(len(inpTuple) == 6, "Expected 6-tuple for ifgoto") 
            self.opType     =  OperationType(str(inpTuple[2]))
            self.inp1       =  Entity(str(inpTuple[3]))
            self.inp2       =  Entity(str(inpTuple[4]))
            self.jmpTarget  =  int(inpTuple[5])

        elif self.instrType.is_GOTO():
            # Line Number, Goto, Target
            DEBUG.Assert(len(inpTuple) == 3, "Expected 3-tuple for goto")                       
            self.jmpTarget  = int(inpTuple[2])

        elif self.instrType.is_CALL():
            # Line Number, Call, Label
            DEBUG.Assert(len(inpTuple) == 3, "Expected 3-tuple for call")
            self.jmpLabel  = str(inpTuple[2])               

        elif self.instrType.is_RETURN():
            # Line Number, Return
            DEBUG.Assert(len(inpTuple) == 2, "Expected 2-tuple for return")

        elif self.instrType.is_PRINT():
            # Line Number, Print, Inputs                                
            DEBUG.Assert(len(inpTuple) >= 3, "Expected atleast a 3-tuple for print")
            self.PrintArgs = map(Entity, map(str, inpTuple[2:]))
            
        elif self.instrType.is_LABEL():
            # Line Number, Label, LabelName
            DEBUG.Assert(len(inpTuple) == 3, "Expected 3-tuple for label") 
            self.label    = str(inpTuple[2])
            self.isTarget = True

        elif self.instrType.is_DECLARE():
            # Line Number, Declare, Input                                
            DEBUG.Assert(len(inpTuple) == 3, "Expected 3-tuple for declare")
            self.inp1 = Entity(str(inpTuple[2]))
            self.inp1.AllocateGlobalMemory()

        elif self.instrType.is_ASSIGN():                 
            # Line Number, =, OP, dest, inp1, inp2                 
            # Line Number, =, dest, inp1             
            # Line Number, =, OP, dest, inp1
            DEBUG.Assert(len(inpTuple) >= 4, "Expected 4/5/6-tuple for assign")      
            DEBUG.Assert(len(inpTuple) <= 6, "Expected 4/5/6-tuple for assign")          

            if len(inpTuple) == 4:
                self.dest   = Entity(str(inpTuple[2]))
                self.inp1   = Entity(str(inpTuple[3]))
                self.isCopy = True

            elif len(inpTuple) == 5:
                self.opType = OperationType(str(inpTuple[2]))
                self.dest   = Entity(str(inpTuple[3]))
                self.inp1   = Entity(str(inpTuple[4]))

            else:
                self.opType = OperationType(str(inpTuple[2]))
                self.dest   = Entity(str(inpTuple[3]))
                self.inp1   = Entity(str(inpTuple[4]))
                self.inp2   = Entity(str(inpTuple[5]))

            DEBUG.Assert(self.dest.is_VARIABLE(), "LHS of an ASSIGN has to be a variable")
            self.dest.AllocateGlobalMemory()
            

    def IsTarget(self): 
        """ Is this branch a jump target or a label? """
        return self.isTarget

    def GetTarget(self):
        """ Return line ID of the jump target if any """
        return self.jmpTarget

    def PrettyPrint(self):
        print self.inpTuple

    def ReturnSymbols(self):
        ret = self.dest.ReturnSymbols() + self.inp1.ReturnSymbols() + self.inp2.ReturnSymbols()
        for arg in self.PrintArgs:
            ret += arg.ReturnSymbols()

        return set(ret)

    def UpdateAndAttachSymbolTable(self, oldTable):
        """ Set new liveness and next-use parameters """

        symbols = list(self.ReturnSymbols())
        if len(symbols) == 0:
            self.symTable = oldTable
            return

        newProperties = {sym:[False, -1] for sym in symbols}

        outSymbol = self.dest.value

        if self.dest.is_VARIABLE():
            newProperties[outSymbol] = [False, -1]

        # Rest of the symbols count as a "use"
        for sym in symbols:
            if sym == outSymbol:
                continue

            newProperties[sym] = [True, self.lineID]

        # Check if the outSymbol is used as an input as well
        if self.dest.is_VARIABLE():
            if (self.inp1.value == outSymbol or 
                self.inp2.value == outSymbol or 
                outSymbol in [i.value for i in self.PrintArgs]):

                newProperties[outSymbol] = [True, self.lineID] 


        self.symTable = BB.SymSetProperties(oldTable, newProperties)
