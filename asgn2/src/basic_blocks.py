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
import translator as TRANS
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
        self.finalSymTable = symTable

        for revInstr in reversed(self.instructions):
            revInstr.UpdateAndAttachSymbolTable(symTable)
            symTable = revInstr.symTable

    def Translate(self):
        self.ComputeSymbolTables()
        bbRegAddrDescriptor = RegAddrDescriptor(self.symbols)

        # Set global pointers
        G.CurrRegAddrTable = bbRegAddrDescriptor

        for (idx, instr) in enumerate(self.instructions):

            # Set global pointers
            G.CurrSymbolTable = instr.symTable
            G.CurrInstruction = instr
            G.AllocMap = {}
            instr.PrettyPrint()

            if idx != len(self.instructions) - 1:
                G.NextSymbolTable = self.instructions[idx + 1].symTable
            else:
                G.NextSymbolTable = self.finalSymTable

            # Add the necessary labels before doing register allocation
            if instr.instrType.is_LABEL():
                G.AsmText.AddText("%s:"%(instr.label))
            elif instr.IsTarget():
                # Add a label L_<line_no> for each line in the input
                # if it is a branch target
                G.AsmText.AddText("L_%d:"%(instr.lineID))

            # Perform register allocation
            regAllocCode = self.RegisterAllocate()
            if regAllocCode:
                G.AsmText.AddText(regAllocCode)

            self.UpdateRegAddrDescriptor()

            G.CurrRegAddrTable.PrettyPrintRegisters()

            # TODO : Actual Translation

            TRANS.Translate(instr)


    def PrettyPrint(self):
        print "BASIC BLOCK #" + str(self.bbNum)
        for instr in self.instructions:
            instr.PrettyPrint()

    def RegisterAllocate(self):
        """ Perform register allocation for the current instruction """

        codeSegment = ""
        alreadyAllocatedRegs = []

        # Register Allocation for input 1
        if G.CurrInstruction.inp1.is_SCALAR_VARIABLE():
            varName = G.CurrInstruction.inp1.value
            reg, getRegCode, isLoaded = GetReg(varName, alreadyAllocatedRegs)

            # Set global details and add code for loading if necessary
            G.AllocMap[varName] = reg
            codeSegment += getRegCode

            if not isLoaded:
                codeSegment += reg.LoadVar(varName)

            alreadyAllocatedRegs += [reg.regName]

        # Register Allocation for input 2
        if G.CurrInstruction.inp2.is_SCALAR_VARIABLE():
            varName = G.CurrInstruction.inp2.value
            reg, getRegCode, isLoaded = GetReg(varName, alreadyAllocatedRegs)

            # Set global details and add code for loading if necessary
            G.AllocMap[varName] = reg
            codeSegment += getRegCode

            if not isLoaded:
                codeSegment += reg.LoadVar(varName)

            alreadyAllocatedRegs += [reg.regName]

        # Register Allocation for dest variable
        if G.CurrInstruction.dest.is_SCALAR_VARIABLE():
            varName = G.CurrInstruction.dest.value

            if G.CurrInstruction.isCopy:

                # If it is a copy operation, simply allocate the register allocated to the input
                if (G.CurrInstruction.inp1.is_SCALAR_VARIABLE()):
                    inpVarName = G.CurrInstruction.inp1.value
                    reg =  G.AllocMap[inpVarName]
                    G.AllocMap[varName] = reg

                    return codeSegment

            if G.CurrRegAddrTable.IsInRegisterSafe(varName):

                reg = G.AllocMap[varName]
                G.AllocMap[varName] = reg

                return codeSegment
        
            if G.CurrInstruction.inp1.is_SCALAR_VARIABLE():
                inpVarName = G.CurrInstruction.inp1.value

                if SafeToReuse(inpVarName):
                    # Use the same register
                    reg =  G.AllocMap[inpVarName]
                    G.AllocMap[varName] = reg

                    return codeSegment

            if G.CurrInstruction.inp2.is_SCALAR_VARIABLE():
                inpVarName = G.CurrInstruction.inp2.value

                if SafeToReuse(inpVarName):
                    # Use the same register
                    reg =  G.AllocMap[inpVarName]
                    G.AllocMap[varName] = reg

                    return codeSegment

            reg, getRegCode, isLoaded = GetReg(varName, alreadyAllocatedRegs, forceSearch=True)

            # Set global details and add code for loading if necessary
            G.AllocMap[varName] = reg
            codeSegment += getRegCode

            return codeSegment

    def UpdateRegAddrDescriptor(self):
        if G.CurrInstruction.inp1.is_SCALAR_VARIABLE():
            varName = G.CurrInstruction.inp1.value
            G.CurrRegAddrTable.SetRegister(varName, G.AllocMap[varName])

        if G.CurrInstruction.inp2.is_SCALAR_VARIABLE():
            varName = G.CurrInstruction.inp2.value
            G.CurrRegAddrTable.SetRegister(varName, G.AllocMap[varName])

        if G.CurrInstruction.dest.is_SCALAR_VARIABLE():
            varName = G.CurrInstruction.dest.value

            if G.CurrInstruction.isCopy:
                G.CurrRegAddrTable.RemoveDestVarFromRegisters(varName)
                G.CurrRegAddrTable.SetInMemory(varName, False, knockOffRegister=True)
                G.CurrRegAddrTable.SetRegister(varName, G.AllocMap[varName])

            else:
                G.CurrRegAddrTable.RemoveDestVarFromRegisters(varName)
                G.CurrRegAddrTable.ClearRegister(G.AllocMap[varName])
                G.CurrRegAddrTable.SetInMemory(varName, False, knockOffRegister=True)
                G.CurrRegAddrTable.SetRegister(varName, G.AllocMap[varName])

def GetReg(varName, alreadyAllocatedRegs, forceSearch=False):

    codeSegment = ""

    if G.CurrRegAddrTable.IsInRegister(varName) and (not forceSearch):
        # If it's already in a register, there is nothing to do
        # True stands for the fact the variable is already loaded
        return G.CurrRegAddrTable.GetAllocatedRegister(varName), codeSegment, True 

    for (reg, alloc) in G.CurrRegAddrTable.regMap.items():
        if reg.regName in alreadyAllocatedRegs:
            continue

        if not alloc: # Empty, we can use this
            # False stands for the fact the variable is not loaded
            return reg, codeSegment, False
    else:

        currReg, currCodeSegment = FindBestRegister(varName, alreadyAllocatedRegs)
        codeSegment += currCodeSegment 
        G.CurrRegAddrTable.ClearRegister(currReg)
        # False stands for the fact the variable is not loaded
        return currReg, codeSegment, False

def FindBestRegister(varName, alreadyAllocatedRegs, alreadyLoadedReg=None):
    # All registers are full, need to select the cheapest one.
    currMinScore = 10
    currReg = None
    currCodeSegment = ""
    currRemoveSet = []

    for reg in G.CurrRegAddrTable.regs:
        if reg.regName in alreadyAllocatedRegs:
            # Shouldn't disturb previous allocations. Wouldn't make any sense
            continue

        score, regCodeSeg, regRemoveSet = reg.Score(varName)

        if score < currMinScore:
            currMinScore = score
            currReg = reg
            currCodeSegment = regCodeSeg
            currRemoveSet = regRemoveSet[:]

    for removeVar in currRemoveSet:
        # Update Register-Address-Table 
        #print "REMOVING : ", removeVar
        G.CurrRegAddrTable.SetInMemory(removeVar, knockOffRegister=True)

    return currReg, currCodeSegment

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
            DEBUG.Assert(varName.is_SCALAR_VARIABLE(), "Entity is not a scalar variable")
            varName = varName.value

        self.symTable[varName][0] = isLive

    def SetNextUse(self, varName, nextUse):
        if type(varName) == INSTRUCTION.Entity:
            DEBUG.Assert(varName.is_SCALAR_VARIABLE(), "Entity is not a scalar variable")
            varName = varName.value

        self.symTable[varName][1] = nextUse

    def GetNextUse(self, varName):
        if type(varName) == INSTRUCTION.Entity:
            DEBUG.Assert(varName.is_SCALAR_VARIABLE(), "Entity is not a scalar variable")
            varName = varName.value

        return self.symTable[varName][1]


    def IsLive(self, varName):
        if type(varName) == INSTRUCTION.Entity:
            DEBUG.Assert(varName.is_SCALAR_VARIABLE(), "Entity is not a scalar variable")
            varName = varName.value

        return self.symTable[varName][0] and (self.symTable[varName][1] != -1)

    def PrettyPrint(self):
        """ For debugging purposes """

        for (sym, prop) in self.symTable.items():
            print sym, " : ", prop


def SymSetProperties(symTable, newProperties):
    """ Creates a copy and then modifies it. This is because we need a separate table for every instruction """

    symCopy = SymbolTable([])
    symCopy.symTable = {sym:value[:] for (sym, value) in symTable.symTable.items()}

    for (varName, properties) in newProperties.items():
        symCopy.SetLive(varName, properties[0])
        symCopy.SetNextUse(varName, properties[1])

    return symCopy

def SafeToReuse(varName):
    # Assumes a register has been allocated to varName
    return (not G.NextSymbolTable.IsLive(varName)) and (G.CurrRegAddrTable.IsInMemory(varName))

class RegAddrDescriptor(object):
    """ 
        This class implements a register and address descriptor.
    """

    def __init__(self, initial_symbols):
        self.symbols = initial_symbols
        self.regs = REG.addrDescRegs + REG.savedRegs # Can be changed if we want to use less/more
        #self.regs = [REG.t0, REG.t1, REG.t2]

        # Since everything is global, all of them reside in memory
        # MAP : <var_name> -> (in_memory? , in_register?)

        self.addrMap = {sym:[True, None] for sym in initial_symbols}

        # All registers assumed to be empty initially

        self.regMap  = {reg : [] for reg in self.regs}

    def IsInRegister(self, varName):
        if type(varName) == INSTRUCTION.Entity:
            DEBUG.Assert(varName.is_SCALAR_VARIABLE(), "Entity is not a scalar variable")
            varName = varName.value

        return (self.addrMap[varName][1] != None)

    def IsInRegisterSafe(self, varName):
        if type(varName) == INSTRUCTION.Entity:
            DEBUG.Assert(varName.is_SCALAR_VARIABLE(), "Entity is not a scalar variable")
            varName = varName.value

        reg = self.addrMap[varName][1]
        if reg == None:
            return False
        
        return len(self.regMap[reg]) == 1

    def IsElsewhere(self, varName, regName):
        return self.IsInMemory(varName) or (self.addrMap[varName][1].regName != regName)

    def GetVars(self, reg):
        return self.regMap[reg]

    def GetAllocatedRegister(self, varName):
        """ To be used after register allocation has been performed """

        if type(varName) == INSTRUCTION.Entity:
            DEBUG.Assert(varName.is_SCALAR_VARIABLE(), "Entity is not a scalar variable")
            varName = varName.value

        return self.addrMap[varName][1]

    def IsInMemory(self, varName):
        """ Is latest value in memory? """

        if type(varName) == INSTRUCTION.Entity:
            DEBUG.Assert(varName.is_SCALAR_VARIABLE(), "Entity is not a scalar variable")
            varName = varName.value
        
        return self.addrMap[varName][0]

    def SetInMemory(self, varName, inMemory=True, knockOffRegister=False):
        if type(varName) == INSTRUCTION.Entity:
            DEBUG.Assert(varName.is_SCALAR_VARIABLE(), "Entity is not a scalar variable")
            varName = varName.value
        
        self.addrMap[varName][0] = inMemory
        if knockOffRegister:
            self.addrMap[varName][1] = None

    def SetRegister(self, varName, reg):
        if type(varName) == INSTRUCTION.Entity:
            DEBUG.Assert(varName.is_SCALAR_VARIABLE(), "Entity is not a scalar variable")
            varName = varName.value
        
        self.addrMap[varName][1] = reg
        self.regMap[reg] = list(set(self.regMap[reg] + [varName]))

    def ClearRegister(self, reg):
        self.regMap[reg] = []

    def RemoveDestVarFromRegisters(self, varName):
        if type(varName) == INSTRUCTION.Entity:
            DEBUG.Assert(varName.is_SCALAR_VARIABLE(), "Entity is not a scalar variable")
            varName = varName.value

        for reg in self.regMap:
            if len(self.regMap[reg]) > 1:
                try:
                    self.regMap[reg].remove(varName)
                    self.addrMap[varName][1] = None
                except:
                    pass


    def PrettyPrintRegisters(self):
        for (reg, var) in self.regMap.items():
            if var:
                print str(reg), " : ", var, "  ",

        print ""

    def DumpDirtyVars(self):
        # Will be called when exiting a basic block
        # Writes values of dirty registers to memory

        for (var,value) in self.addrMap.iteritems():
            if not value[0]:
                G.AsmText.AddText(value[1].SpillVar(var))
