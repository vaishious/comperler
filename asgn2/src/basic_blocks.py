"""

MODULE  : basic_blocks

Purpose : * Class used to represent a basic block. Will be an array of instructions.
          * All required algorithms such as register allocation etc. will be a part of this 
            class

Import Acronym : BB

"""

# List of Imports Begin
import debug as DEBUG
import instr3ac as INSTRUCTION
import copy
# List of Imports End


class BasicBlock(object):
    """ 
        This class holds an array of instructions corresponding to a single basic block.

        Member Variables :

                * bbNum             : Basic Block Number
                
                * instructions      : The actual sequence of instructions corresponding to the basic block.

                * regAddrDescriptor : The register and address descriptor for this block

                TODO: Add more stuff as and how we need it.

        Member Functions : 

                * RegisterAllocate : Perform register allocation for this block

                TODO: Add more stuff as and how we need it.
    """

    def __init__(self, bbNum=0, instructions=[]):

        self.bbNum        = bbNum
        self.instructions = instructions[:]
        self.symbols      = set([])

    def AddInstruction(self, instr):
        """ Add instructions incrementally. Will help in the basic block algorithm """

        DEBUG.Assert(type(instr) == INSTRUCTION.Instr3AC, "Input is not of instr3AC type")

        self.instructions += [instr]
        self.symbols |= instr.ReturnSymbols()

    def IsEmpty(self):
        return len(self.instructions) == 0

    def ComputeSymbolTables(self):
        """ Compute live ranges and next-use using a backward scan """
        symTable = SymbolTable(self.symbols)

    def PrettyPrint(self):
        print "BASIC BLOCK #" + str(self.bbNum)
        for instr in self.instructions:
            instr.PrettyPrint()


class SymbolTable(object):
    """ 
        Used to implement a symbol table. Contains info about liveness and next-use.
        Will be required in register allocation

        symTable : Map : <var> -> (live?, next-use)

        Note: -1 means no-next-use
    """


    def __init__(self, initial_symbols):
        self.symTable = {sym:[True, -1] for sym in initial_symbols}

    def SetLive(self, varName, isLive=True):
        if type(varName) == INSTRUCTION.Entity:
            DEBUG.Assert(varName.is_VARIABLE(), "Entity is not a variable")
            varName = varName.value

        self.symTable[varName][0] = isLive

    def SetNextUse(self, varName, nextUse):
        if type(varName) == INSTRUCTION.Entity:
            DEBUG.Assert(varName.is_VARIABLE(), "Entity is not a variable")
            varName = varName.value

        self.symTable[varName][1] = nextUse


def SymSetLive(symTable, varName, isLive=True):
    """ Creates a copy and then modifies it. This is because we need a separate table for every instruction """

    symCopy = copy.deepcopy(symTable)
    symCopy.SetLive(varName, isLive)

def SymSetNextUse(symTable, varName, nextUse):
    """ Creates a copy and then modifies it. This is because we need a separate table for every instruction """

    symCopy = copy.deepcopy(symTable)
    symCopy.SetNextUse(varName, nextUse)


class RegAddrDescriptor(object):
    """ 
        This class implements a register and address descriptor.
    """

    def __init__(self, initial_symbols):
        self.symbols = initial_symbols
        self.regs = REG.tmpRegs + REG.savedRegs # Can be changed if we want to use less/more

        # Since everything is global, all of them reside in memory
        # MAP : <var_name> -> (in_memory? , in_register?)

        self.addrMap = {sym:[True, False] for sym in initial_symbols}

        # All registers assumed to be empty initially
        # @ means no variable

        self.regMap  = {reg : "@" for reg in self.regs}

