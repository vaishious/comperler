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
import registers as REG
import global_objects as G
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

        for revInstr in reversed(self.instructions):
            revInstr.UpdateAndAttachSymbolTable(symTable)
            #revInstr.PrettyPrint()
            #revInstr.symTable.PrettyPrint()

    def Translate(self):
        self.ComputeSymbolTables()
        bbRegAddrDescriptor = RegAddrDescriptor(self.symbols)

        # Set global pointers
        G.CurrRegAddrTable = bbRegAddrDescriptor

        for instr in self.instructions:

            # Set global pointers
            G.CurrSymbolTable = instr.symTable

            # TODO : Actual Translation

            if instr.instrType.is_LABEL():
                G.AsmText.AddText("%s:"%(instr.label))

            elif instr.IsTarget():
                # Add a label L_<line_no> for each line in the input
                # if it is a branch target
                G.AsmText.AddText("L_%d:"%(instr.lineID))

            if instr.instrType.is_DECLARE():
                pass

            elif instr.instrType.is_GOTO():
                G.CurrRegAddrTable.DumpDirtyVars()
                G.AsmText.AddText(G.INDENT + "j L_%d"%(instr.jmpTarget))

            elif instr.instrType.is_CALL():
                G.CurrRegAddrTable.DumpDirtyVars()
                G.AsmText.AddText(G.INDENT + "jal %s"%(instr.jmpLabel))

            elif instr.instrType.is_RETURN():
                G.CurrRegAddrTable.DumpDirtyVars()
                G.AsmText.AddText(G.INDENT + "jr $ra")

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

    def PrettyPrint(self):
        """ For debugging purposes """

        for (sym, prop) in self.symTable.items():
            print sym, " : ", prop


def SymSetProperties(symTable, newProperties):
    """ Creates a copy and then modifies it. This is because we need a separate table for every instruction """

    symCopy = copy.deepcopy(symTable)

    for (varName, properties) in newProperties.items():
        symCopy.SetLive(varName, properties[0])
        symCopy.SetNextUse(varName, properties[1])

    return symCopy


class RegAddrDescriptor(object):
    """ 
        This class implements a register and address descriptor.
    """

    def __init__(self, initial_symbols):
        self.symbols = initial_symbols
        self.regs = REG.tmpRegs + REG.savedRegs # Can be changed if we want to use less/more

        # Since everything is global, all of them reside in memory
        # MAP : <var_name> -> (in_memory? , in_register?)

        self.addrMap = {sym:[True, None] for sym in initial_symbols}

        # All registers assumed to be empty initially

        self.regMap  = {reg : [] for reg in self.regs}

    def IsInRegister(self, varName):
        if type(varName) == INSTRUCTION.Entity:
            DEBUG.Assert(varName.is_VARIABLE(), "Entity is not a variable")
            varName = varName.value

        return not self.addrMap[varName][1]

    def IsElsewhere(self, varName, regName):
        return IsInMemory(varName) or (self.addrMap[varName][1].regName != regName)

    def GetVars(self, reg):
        return regMap[reg]

    def GetReg(self, varName):
        """ To be used for register allocation """

        if type(varName) == INSTRUCTION.Entity:
            DEBUG.Assert(varName.is_VARIABLE(), "Entity is not a variable")
            varName = varName.value

        if self.IsInRegister(varName):
            # Already in a register, nothing to do
            return

        for (reg, alloc) in self.regMap.items():
            if not alloc: # Empty, we can use this
                self.regMap[reg] += [varName]
                return

        # All registers are full, need to select the cheapest one.



    def GetAllocatedRegister(self, varName):
        """ To be used after register allocation has been performed """

        if type(varName) == INSTRUCTION.Entity:
            DEBUG.Assert(varName.is_VARIABLE(), "Entity is not a variable")
            varName = varName.value

        return self.addrMap[varName][1]

    def IsInMemory(self, varName):
        """ Is latest value in memory? """

        if type(varName) == INSTRUCTION.Entity:
            DEBUG.Assert(varName.is_VARIABLE(), "Entity is not a variable")
            varName = varName.value
        
        return self.addrMap[varName][0]

    def SetInMemory(self, varName, inMemory=True):
        if type(varName) == INSTRUCTION.Entity:
            DEBUG.Assert(varName.is_VARIABLE(), "Entity is not a variable")
            varName = varName.value
        
        self.addrMap[varName][0] = inMemory

    def SetRegister(self, varName, reg):
        if type(varName) == INSTRUCTION.Entity:
            DEBUG.Assert(varName.is_VARIABLE(), "Entity is not a variable")
            varName = varName.value
        
        self.addrMap[varName][1] = reg
        self.regMap[reg] += [varName]

    def DumpDirtyVars(self):
        # Will be called when exiting a basic block
        # Writes values of dirty registers to memory

        for reg in self.regs:
            regVars = self.regMap[reg]
            if (len(regVars) > 0) and (not IsInMemory(regVars[-1])):
                G.AsmText.AddText(reg.SpillVar(regVars[-1]))
