"""

MODULE  : instr3ac.py

Purpose : * Class used to represent an individual instruction in 3AC format 

Import Acronym : INSTRUCTION

"""

# List of Imports Begin
import re               # For checking type of variable
import debug as DEBUG
import global_objects as G
import library as LIB
import mips_assembly as ASM
import basic_blocks as BB
import translator as TRANS
import registers as REG
# List of Imports End


class InstrType(object):
    """ 
        Instruction Types : 
    
        Straightforward : ASSIGN, IFGOTO, GOTO, CALL, RETURN, PRINT, READ, NOP, LABEL, ALLOC, EXIT

        Custom          : Declare - Will be used to fix sizes of the arrays

    """


    # Enum for holding these values
    ASSIGN, IFGOTO, STRIFGOTO, GOTO, CALL, RETURN, PRINT, KEYS, VALUES, READ, LABEL, DECLARE, EXIT, NOP, ALLOC = range(15)

    typeMap = { 
                "="          : ASSIGN,        "assign" : ASSIGN,       "ASSIGN"    : ASSIGN,
                "ifgoto"     : IFGOTO,                                 "IFGOTO"    : IFGOTO,
                "strifgoto"  : STRIFGOTO,                              "STRIFGOTO" : STRIFGOTO,    "str_ifgoto" : STRIFGOTO,
                "goto"       : GOTO,          "jmp"    : GOTO,         "GOTO"      : GOTO, 
                "call"       : CALL,                                   "CALL"      : CALL,
                "ret"        : RETURN,        "return" : RETURN,       "RETURN"    : RETURN,       "RET" : RETURN,
                "print"      : PRINT,         "printf" : PRINT,        "PRINT"     : PRINT,
                "keys"       : KEYS,          "KEYS"   : KEYS,
                "values"     : VALUES,        "VALUES" : VALUES,
                "read"       : READ,          "scanf"  : READ,         "READ"      : READ,
                "label"      : LABEL,         "Label"  : LABEL,        "LABEL"     : LABEL,
                "declare"    : DECLARE,       "decl"   : DECLARE,      "DECLARE"   : DECLARE,
                "alloc"      : ALLOC,         "malloc" : ALLOC,        "ALLOC"     : ALLOC,
                "exit"       : EXIT,          "quit"   : EXIT,         "EXIT"      : EXIT,         "done" : EXIT,
                "nop"        : NOP,           ""       : NOP,          "NOP"       : NOP
              }

    def __init__(self, inpType):
        self.inpType = inpType      # Will be a string

        if not InstrType.typeMap.has_key(inpType):
            raise DEBUG.InputError3AC(inpType, "Instruction type not recognized")
        
        self.instrType = InstrType.typeMap[inpType]

    def is_ASSIGN(self)     : return self.instrType == InstrType.ASSIGN
    def is_IFGOTO(self)     : return self.instrType == InstrType.IFGOTO
    def is_STRIFGOTO(self)  : return self.instrType == InstrType.STRIFGOTO
    def is_GOTO(self)       : return self.instrType == InstrType.GOTO
    def is_CALL(self)       : return self.instrType == InstrType.CALL
    def is_RETURN(self)     : return self.instrType == InstrType.RETURN
    def is_PRINT(self)      : return self.instrType == InstrType.PRINT
    def is_KEYS(self)       : return self.instrType == InstrType.KEYS
    def is_VALUES(self)     : return self.instrType == InstrType.VALUES
    def is_READ(self)       : return self.instrType == InstrType.READ
    def is_ALLOC(self)      : return self.instrType == InstrType.ALLOC
    def is_LABEL(self)      : return self.instrType == InstrType.LABEL
    def is_DECLARE(self)    : return self.instrType == InstrType.DECLARE
    def is_EXIT(self)       : return self.instrType == InstrType.EXIT
    def is_NOP(self)        : return self.instrType == InstrType.NOP

    def is_JMP(self)     : return (self.instrType == InstrType.IFGOTO or
                                   self.instrType == InstrType.STRIFGOTO or
                                   self.instrType == InstrType.GOTO or
                                   self.instrType == InstrType.RETURN or
                                   self.instrType == InstrType.EXIT or
                                   self.instrType == InstrType.CALL or
                                   self.instrType == InstrType.PRINT or
                                   self.instrType == InstrType.KEYS or
                                   self.instrType == InstrType.VALUES or
                                   self.instrType == InstrType.ALLOC or
                                   self.instrType == InstrType.READ)


class OperationType(object):
    """ 
        Operation Types : PLUS, MINUS, MULT, DIV, MOD, LT, GT, LEQ, GEQ, 
                          EQ, NE, BOR, BAND, BNOT, BXOR, LSHIFT, RSHIFT, NONE 

    """ # Will add more later

    # Set up an enum
    PLUS, MINUS, MULT, DIV, MOD, LT, GT, LEQ, GEQ, EQ, NE, BOR, BAND, BNOT, BXOR, LSHIFT, RSHIFT, REFERENCE, DEREFERENCE, NONE = range(20)

    typeMap = {
                "+"     : PLUS,          "plus"     : PLUS,
                "-"     : MINUS,         "minus"    : MINUS,
                "*"     : MULT,          "mult"     : MULT,       "multiply"    : MULT,
                "/"     : DIV,           "div"      : DIV,        "divide"      : DIV,
                "%"     : MOD,           "mod"      : MOD,        "modulo"      : MOD,
                "<"     : LT,            "lt"       : LT,
                ">"     : GT,            "gt"       : GT,
                "<="    : LEQ,           "leq"      : LEQ,
                ">="    : GEQ,           "geq"      : GEQ,
                "=="    : EQ,            "eq"       : EQ,
                "!="    : NE,            "ne"       : NE,
                "|"     : BOR,           "bor"      : BOR,
                "&"     : BAND,          "band"     : BAND,
                "~"     : BNOT,          "bnot"     : BNOT,
                "^"     : BXOR,          "bxor"     : BXOR,
                "<<"    : LSHIFT,        "lshift"   : LSHIFT,
                ">>"    : RSHIFT,        "rshift"   : RSHIFT,
                "ref"   : REFERENCE,     "$"        : DEREFERENCE,  
                ""      : NONE
              }

    def __init__(self, inpType):
        self.inpType = inpType      # Will be a string

        if not OperationType.typeMap.has_key(inpType):
            raise DEBUG.InputError3AC(inpType, "Operation type not recognized")
        
        self.opType = OperationType.typeMap[inpType]

    def __str__(self):
        if self.is_PLUS()        : return "+" 
        if self.is_MINUS()       : return "-"
        if self.is_MULT()        : return "*"
        if self.is_DIV()         : return "/"
        if self.is_MOD()         : return "%"
        if self.is_LT()          : return "<"
        if self.is_GT()          : return ">"
        if self.is_LEQ()         : return "<="
        if self.is_GEQ()         : return ">="
        if self.is_EQ()          : return "=="
        if self.is_NE()          : return "!="
        if self.is_BOR()         : return "|" 
        if self.is_BAND()        : return "&"
        if self.is_BNOT()        : return "~"
        if self.is_BXOR()        : return "^" 
        if self.is_LSHIFT()      : return "<<"
        if self.is_RSHIFT()      : return ">>"
        if self.is_REFERENCE()   : return "\\"
        if self.is_DEREFERENCE() : return "$"

    def is_PLUS(self)        : return self.opType == OperationType.PLUS
    def is_MINUS(self)       : return self.opType == OperationType.MINUS
    def is_MULT(self)        : return self.opType == OperationType.MULT
    def is_DIV(self)         : return self.opType == OperationType.DIV
    def is_MOD(self)         : return self.opType == OperationType.MOD
    def is_LT(self)          : return self.opType == OperationType.LT
    def is_GT(self)          : return self.opType == OperationType.GT
    def is_LEQ(self)         : return self.opType == OperationType.LEQ
    def is_GEQ(self)         : return self.opType == OperationType.GEQ
    def is_EQ(self)          : return self.opType == OperationType.EQ
    def is_NE(self)          : return self.opType == OperationType.NE
    def is_BOR(self)         : return self.opType == OperationType.BOR
    def is_BAND(self)        : return self.opType == OperationType.BAND
    def is_BNOT(self)        : return self.opType == OperationType.BNOT
    def is_BXOR(self)        : return self.opType == OperationType.BXOR
    def is_LSHIFT(self)      : return self.opType == OperationType.LSHIFT
    def is_RSHIFT(self)      : return self.opType == OperationType.RSHIFT
    def is_REFERENCE(self)   : return self.opType == OperationType.REFERENCE
    def is_DEREFERENCE(self) : return self.opType == OperationType.DEREFERENCE
    def is_NONE(self)        : return self.opType == OperationType.NONE


class Entity(object):
    """ Used to represent the variables/numbers/strings used in the instruction """

    # Enum for storing the types
    SCALAR_VARIABLE, HASH_VARIABLE, ARRAY_VARIABLE, STRING, NUMBER, NONE = range(6)

    # Rules for identifying each one
    singleQuoteString = r'\'([^\\]|(\\[\s\S]))*?\''
    doubleQuoteString = r'\"([^\\]|(\\[\s\S]))*?\"'
    string            = r'(' + singleQuoteString + r'|' + doubleQuoteString + r')'
    number            = r'[-]?\d+'
    identifier        = r'[a-zA-Z_][a-zA-Z0-9_\$\%@]*'
    arrayAccess       = identifier + r'\[' + r'(.*)' + r'\]'
    hashAccess        = identifier + r'\{'  + r'(.*)' + r'\}'

    reString         = re.compile(r'^' + string + r'$')
    reNumber         = re.compile(r'^' + number + r'$')
    reScalar         = re.compile(r'^' + identifier + r'$')
    reArray          = re.compile(r'^' + arrayAccess + r'$')
    reHash           = re.compile(r'^' + hashAccess + r'$')

    def __init__(self, inpString, stringAllocate=True):
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
            self.value  = inpString[1:-1]
            if stringAllocate:
                G.AsmData.AllocateString(self)

        elif Entity.reScalar.match(inpString): # Is a scalar
            self.entity = Entity.SCALAR_VARIABLE
            self.value  = repr(inpString)[1:-1]

        elif Entity.reArray.match(inpString):  # Is an array
            self.entity = Entity.ARRAY_VARIABLE
            self.value  = repr(inpString[:inpString.find('[')])[1:-1]
            self.key    = Entity(repr(inpString[inpString.find('[')+1:-1])[1:-1])

        elif Entity.reHash.match(inpString):
            self.entity = Entity.HASH_VARIABLE
            self.value  = repr(inpString[:inpString.find('{')])[1:-1]
            self.key    = Entity(repr(inpString[inpString.find('{')+1:-1])[1:-1])

        else:
            raise DEBUG.InputError3AC(inpString, "Failed to recognize entity")

    def __str__(self):
        return str(self.inpString)

    def is_NUMBER(self)          : return self.entity == Entity.NUMBER
    def is_SCALAR_VARIABLE(self) : return self.entity == Entity.SCALAR_VARIABLE
    def is_ARRAY_VARIABLE(self)  : return self.entity == Entity.ARRAY_VARIABLE
    def is_HASH_VARIABLE(self)   : return self.entity == Entity.HASH_VARIABLE
    def is_STRING(self)          : return self.entity == Entity.STRING
    def is_NONE(self)            : return self.entity == Entity.NONE
    def is_VARIABLE(self)        : return (self.entity == Entity.SCALAR_VARIABLE or
                                           self.entity == Entity.HASH_VARIABLE or
                                           self.entity == Entity.ARRAY_VARIABLE)

    def IsRegisterAllocated(self):
        """ Reads the current reg-address descriptor and returns a boolean value """
        if not self.is_SCALAR_VARIABLE():
            return False

        return G.CurrRegAddrTable.IsInRegister(self.value)

    def GetCurrReg(self):
        """ Reads the current reg-address descriptor and returns the relevant register """
        return G.CurrRegAddrTable.GetAllocatedRegister(self.value)

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

        if self.is_HASH_VARIABLE():
            return G.INDENT + "lw %s, %s\n"%(reg, ASM.GetHashAddr(self))

        if self.is_SCALAR_VARIABLE():
            if self.IsRegisterAllocated():
                return G.INDENT + "move %s, %s\n"%(reg, self.GetCurrReg())
            else:
                return G.INDENT + "lw %s, %s\n"%(reg, ASM.GetVarAddr(self))

        if self.is_ARRAY_VARIABLE():
            tempReg = REG.tmpUsageRegs[-1]
            regComp = reg
            codeSegment = ""

            if self.key.is_NUMBER():
                codeSegment += tempReg.LoadImmediate(self.key.value) + "\n"

            else:
                regInp = TRANS.SetupRegister(self.key, regComp)
                codeSegment += G.INDENT + "move %s, %s\n"%(tempReg, regInp)

            # Load the array address in regComp
            codeSegment += G.INDENT + "la %s, %s\n"%(regComp, ASM.GetArrAddr(self.value))

            # We move the index value to tempReg to multiply it by 4
            codeSegment += G.INDENT + "sll %s, %s, 2\n"%(tempReg, tempReg)
            codeSegment += G.INDENT + "add %s, %s, %s\n"%(regComp, regComp, tempReg)
            codeSegment += G.INDENT + "lw %s, 0(%s)\n"%(regComp, regComp)
            
            return codeSegment

        raise Exception("Can't copy value to register")

    def CopyAddressToRegister(self, reg):
        """ 
            Copies its address to the given register. 
        """
        if self.is_SCALAR_VARIABLE():
            return G.INDENT + "la %s, %s\n"%(reg, ASM.GetVarAddr(self))

        if self.is_STRING():
            return G.INDENT + "la %s, %s\n"%(reg, ASM.GetStrAddr(self))

        if self.is_HASH_VARIABLE():
            return G.INDENT + "la %s, %s\n"%(reg, ASM.GetHashAddr(self))

        if self.is_ARRAY_VARIABLE():
            tempReg = REG.tmpUsageRegs[-1]
            regComp = reg
            codeSegment = ""

            if self.key.is_NUMBER():
                codeSegment += tempReg.LoadImmediate(self.key.value) + "\n"

            else:
                regInp = TRANS.SetupRegister(self.key, regComp)
                codeSegment += G.INDENT + "move %s, %s\n"%(tempReg, regInp)

            # Load the array address in regComp
            codeSegment += G.INDENT + "la %s, %s\n"%(regComp, ASM.GetArrAddr(self.value))

            # We move the index value to tempReg to multiply it by 4
            codeSegment += G.INDENT + "sll %s, %s, 2\n"%(tempReg, tempReg)
            codeSegment += G.INDENT + "add %s, %s, %s\n"%(regComp, regComp, tempReg)

            return codeSegment

        print self.value
        raise Exception("Can't copy value to register")

    def CopyToMemory(self, mem):
        """
            Copies the value at the given memory location. Instructions used are straightforward. In case it is allocated, 
            we use sw directly. Otherwise we copy it to $v0 and then use sw. Specifically used in parameter assignments.
        """
        if self.is_STRING():
            codeSegment = G.INDENT + "la %s, %s\n"%(REG.tmpUsageRegs[-1], ASM.GetStrAddr(self))
            codeSegment += G.INDENT + "sw %s, %s\n"%(REG.tmpUsageRegs[-1], mem)
            return codeSegment

        if self.is_NUMBER():
            codeSegment = G.INDENT + "li %s, %s\n"%(REG.tmpUsageRegs[-1], str(self.value))
            codeSegment += G.INDENT + "sw %s, %s\n"%(REG.tmpUsageRegs[-1], mem)
            return codeSegment

        if self.is_HASH_VARIABLE():
            codeSegment = G.INDENT + "lw %s, %s\n"%(REG.tmpUsageRegs[-1], ASM.GetHashAddr(self))
            codeSegment = G.INDENT + "sw %s, %s\n"%(REG.tmpUsageRegs[-1], mem)
            return codeSegment

        if self.is_SCALAR_VARIABLE():
            if self.IsRegisterAllocated():
                return G.INDENT + "sw %s, %s\n"%(self.GetCurrReg(), mem)

            codeSegment = self.CopyToRegister(REG.tmpUsageRegs[-1])
            codeSegment += G.INDENT + "sw %s, %s\n"%(REG.tmpUsageRegs[-1], mem)
            return codeSegment

        if self.is_ARRAY_VARIABLE():
            codeSegment = self.CopyToRegister(REG.tmpUsageRegs[-1])
            codeSegment += G.INDENT + "sw %s, %s\n"%(REG.tmpUsageRegs[-1], mem)
            return codeSegment


        raise Exception("Can't copy value to memory")

    def CopyAddressToMemory(self, mem):
        """
            Copies the address of this variable to the given memory location
        """

        if self.is_STRING():
            codeSegment = G.INDENT + "la %s, %s\n"%(REG.tmpUsageRegs[-1], ASM.GetStrAddr(self))
            codeSegment = G.INDENT + "sw %s, %s\n"%(REG.tmpUsageRegs[-1], mem)
            return codeSegment

        if self.is_HASH_VARIABLE():
            codeSegment = G.INDENT + "la %s, %s\n"%(REG.tmpUsageRegs[-1], ASM.GetHashAddr(self))
            codeSegment = G.INDENT + "sw %s, %s\n"%(REG.tmpUsageRegs[-1], mem)
            return codeSegment

        if self.is_SCALAR_VARIABLE() or self.is_ARRAY_VARIABLE():
            codeSegment = self.CopyAddressToRegister(REG.tmpUsageRegs[-1])
            codeSegment += G.INDENT + "sw %s, %s\n"%(REG.tmpUsageRegs[-1], mem)
            return codeSegment

        raise Exception("Can't copy value to memory")

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

    def ContainsHashAccess(self):
        if self.is_HASH_VARIABLE():
            return True

        if self.is_ARRAY_VARIABLE():
            return self.key.ContainsHashAccess()

        return False

class Instr3AC(object):
    """ 
        An object of this class represents a single instruction in 3AC format

        Member Variables :

        * Instruction Type : ASSIGN, IFGOTO, GOTO, CALL, RETURN, PRINT

        * Operation Type   : PLUS, MINUS, MULT, DIV, MOD, LT, GT, LEQ, GEQ, EQ, NE

        * Destination      : Where the result is to be stored (Eg: LHS in an assign)

        * Inp1             : Input 1 for the operation

        * Inp2             : Input 2 for the operation. May be omitted

        * IOArgs           : Store the arguments to Print/Read. Deviation from 3-addr code. Cannot be used for any other instruction

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
        self.IOArgs    = []
        self.lineID    = 0
        self.jmpTarget = None
        self.jmpLabel  = None
        self.label     = None
        self.isTarget  = False
        self.symTable  = None
        self.isCopy    = False # Is it of the form x = y
        self.declType  = ''

        # Set line id
        self.lineID    = int(inpTuple[0])                    # Value error raised if input is not an integer
        # Set instruction type
        self.instrType = InstrType(str(inpTuple[1]))         # Custom exception raised in case of error

        if self.instrType.is_IFGOTO() or self.instrType.is_STRIFGOTO(): 
            # Line Number, IFGOTO, OP, inp1, inp2, Target
            DEBUG.Assert(len(inpTuple) == 6, "Expected 6-tuple for ifgoto") 
            self.opType     =  OperationType(str(inpTuple[2]))
            self.inp1       =  Entity(str(inpTuple[3]))
            self.inp2       =  Entity(str(inpTuple[4]))
            self.jmpTarget  =  ConvertTarget(str(inpTuple[5]))

        elif self.instrType.is_GOTO():
            # Line Number, Goto, Target
            DEBUG.Assert(len(inpTuple) == 3, "Expected 3-tuple for goto")                       
            self.jmpTarget  =  ConvertTarget(str(inpTuple[2]))

        elif self.instrType.is_CALL():
            # Line Number, Call, retValTarget, Label, paramArray
            DEBUG.Assert(len(inpTuple) >= 4, "Expected 4-5 tuple for call")
            DEBUG.Assert(len(inpTuple) <= 5, "Expected 4-5 tuple for call")

            self.jmpLabel  = str(inpTuple[3])               
            self.dest = Entity(str(inpTuple[2]))
            DEBUG.Assert(self.dest.is_VARIABLE(), "LHS of a CALL has to be a variable")

            if len(inpTuple) == 5:
                self.inp1 = Entity(str(inpTuple[4]))

        elif self.instrType.is_RETURN():
            # Line Number, Return, retVal
            DEBUG.Assert(len(inpTuple) >= 2, "Expected 2/3-tuple for return")
            DEBUG.Assert(len(inpTuple) <= 3, "Expected 2/3-tuple for return")
            if len(inpTuple) == 3:
                self.inp1 = Entity(str(inpTuple[2]))

        elif self.instrType.is_EXIT():
            # Line Number, Exit
            DEBUG.Assert(len(inpTuple) == 2, "Expected 2-tuple for exit")

        elif self.instrType.is_PRINT():
            # Line Number, Print, InputArray                                
            DEBUG.Assert(len(inpTuple) == 3, "Expected a 3-tuple for print")
            self.inp1 = Entity(inpTuple[2])
 
        elif self.instrType.is_KEYS():
            # Line Number, keys, TargetVar, InputArray                                
            DEBUG.Assert(len(inpTuple) == 4, "Expected a 4-tuple for keys")
            self.dest = Entity(str(inpTuple[2]))
            self.inp1 = Entity(inpTuple[3])           

        elif self.instrType.is_VALUES():
            # Line Number, keys, TargetVar, InputArray                                
            DEBUG.Assert(len(inpTuple) == 4, "Expected a 4-tuple for values")
            self.dest = Entity(str(inpTuple[2]))
            self.inp1 = Entity(inpTuple[3])

        elif self.instrType.is_READ():
            # Line Number, Read, Inputs                                
            DEBUG.Assert(len(inpTuple) >= 3, "Expected atleast a 3-tuple for read")
            self.IOArgs = map(Entity, map(str, inpTuple[2:]))
            
        elif self.instrType.is_ALLOC():
            # Line Number, alloc/malloc, targetVar, size
            DEBUG.Assert(len(inpTuple) == 4, "Expected 4-tuple for alloc")
            self.dest = Entity(str(inpTuple[2]))
            self.inp1 = Entity(str(inpTuple[3]))

        elif self.instrType.is_LABEL():
            # Line Number, Label, LabelName
            DEBUG.Assert(len(inpTuple) == 3, "Expected 3-tuple for label") 
            self.label    = str(inpTuple[2])
            self.isTarget = True

        elif self.instrType.is_DECLARE():
            # Line Number, Declare, Type, Input                                
            DEBUG.Assert(len(inpTuple) == 4, "Expected 4-tuple for declare")
            self.inp1 = Entity(str(inpTuple[3]))
            self.declType = str(inpTuple[2])

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
            
    def __str__(self):
        return self.PrettyPrint()

    def IsTarget(self): 
        """ Is this branch a jump target or a label? """
        return self.isTarget

    def GetTarget(self):
        """ Return ID of the jump target if any """
        return self.jmpTarget

    def ReturnSymbols(self):
        ret = self.dest.ReturnSymbols() + self.inp1.ReturnSymbols() + self.inp2.ReturnSymbols()
        for arg in self.IOArgs:
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

        if self.dest.is_SCALAR_VARIABLE():
            newProperties[outSymbol] = [False, -1]

        # Rest of the symbols count as a "use"
        for sym in symbols:
            if sym == outSymbol:
                continue

            newProperties[sym] = [True, self.lineID]

        # Check if the outSymbol is used as an input as well
        if self.dest.is_SCALAR_VARIABLE():
            if (self.inp1.value == outSymbol or 
                self.inp2.value == outSymbol or 
                outSymbol in [i.value for i in self.IOArgs]):

                newProperties[outSymbol] = [True, self.lineID] 


        self.symTable = BB.SymSetProperties(oldTable, newProperties)

    def ContainsHashAccess(self):
        if self.dest.ContainsHashAccess():
            return True

        if self.inp1.ContainsHashAccess():
            return True

        if self.inp2.ContainsHashAccess():
            return True

        for arg in self.IOArgs:
            if arg.ContainsHashAccess():
                return True

        return False

    def PrettyPrint(self):
        if self.instrType.is_IFGOTO() or self.instrType.is_STRIFGOTO():
            return "If ( %s %s %s ) GOTO %s"%(self.inp1, self.opType, self.inp2, self.jmpTarget)

        if self.instrType.is_GOTO():
            return "GOTO %s"%(self.jmpTarget)

        if self.instrType.is_CALL():
            return "%s = call %s(%s)"%(self.dest, str(self.jmpLabel), str(self.inp1))

        if self.instrType.is_RETURN():
            return "return %s"%(self.inp1)

        if self.instrType.is_EXIT():
            return "exit"

        if self.instrType.is_PRINT():
            return "Print %s"%(str(self.inp1))

        if self.instrType.is_KEYS():
            return "%s = keys(%s)"%(str(self.dest), str(self.inp1))

        if self.instrType.is_VALUES():
            return "%s = values(%s)"%(str(self.dest), str(self.inp1))

        if self.instrType.is_ALLOC():
            return "%s = malloc(%s)"%(self.dest, self.inp1)

        if self.instrType.is_READ():
            return "Read %s"%(str(self.inpTuple[2:]))

        if self.instrType.is_DECLARE():
            return "declare %s of type %s"%(self.inp1, self.declType)

        if self.instrType.is_LABEL():
            return "%s : "%(str(self.label))

        if self.instrType.is_NOP():
            return "NOOP"

        if self.instrType.is_ASSIGN():
            if self.inp2.is_NONE():
                if self.opType.is_NONE():
                    return "%s = %s"%(self.dest, self.inp1)
                else:
                    return "%s = %s%s"%(self.dest, self.opType, self.inp1)
            else:
                return "%s = %s %s %s"%(self.dest, self.inp1, self.opType, self.inp2)
        
def ConvertTarget(inpString):
    if inpString.isdigit():
        return "$LID_" + inpString
    else:
        return inpString
