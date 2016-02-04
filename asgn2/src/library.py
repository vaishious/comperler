"""

MODULE  : library.py

Purpose : This file contains the functionality to make calls to library functions
          Demarcation made from the translation module to keep things separate and clear

Import Acronym : LIB

"""

# List of Imports Begin
import mips_assembly as ASM
import registers as REG
import global_objects as G
import debug as DEBUG

import os
# List of Imports End

def LinkFunction(funcName):
    codeFunc = ""
    insideFunc = False
    labels = []
    for fileName in G.LIBSRC:
        with open(os.path.dirname(__file__) + "/" + fileName, 'r') as f:
            for line in f:
                if insideFunc:
                    codeFunc += line
                    if (".end" in line) and (funcName in line):

                        for l in labels:
                            codeFunc = codeFunc.replace(l, l.replace("$L", "$L" + funcName))

                        return codeFunc

                    if line[:2] == '$L':
                        labels += [line[:-2]]

                elif funcName + ":" in line:
                    insideFunc = True
                    codeFunc += line

    raise Exception("Did not find function : " + funcName)

def Translate_Printf(parameters):
    """ Custom version of Printf can be found in iolib.c in the lib/ folder """

    formatString = parameters[0]

    DEBUG.Assert(formatString.is_STRING(), "First argument of Printf has to be a format specifier")

    G.StackSpaceMap[G.CurrFunction] = max(G.StackSpaceMap[G.CurrFunction], 4*len(parameters))

    codeSegment = ""
    
    # We necessarily have to fetch the hash variable first.
    # This is because it involves function calls which will overwrite 
    # the argument registers if we setup some other argument of Printf first
    hashRegs = [REG.s3, REG.s2, REG.s1, REG.s0]
    hashArgs = []
    for (idx, param) in enumerate(parameters):
        if param.is_HASH_VARIABLE():
            tempReg = REG.tmpUsageRegs[-1]
            regComp = REG.tmpUsageRegs[2]

            if param.key.is_NUMBER():
                G.AsmText.AddText(tempReg.LoadImmediate(param.key.value), "Load key for the hash access")
            else:
                import translator as TRANS          # Top level import throws an error
                regInp = TRANS.SetupRegister(param.key, regComp)
                G.AsmText.AddText(G.INDENT + "move %s, %s"%(tempReg, regInp), "Load key for the hash access")

            Translate_getValue(param, tempReg, regComp) 

            if idx <= 3:
                # These are callee saved registers anyway
                reg = hashRegs.pop()
                hashArgs += [[reg, idx]]
                G.AsmText.AddText(G.INDENT + "move %s, %s"%(reg, regComp))

            else:
                G.AsmText.AddText(G.INDENT + "sw %s, %s"%(regComp, str(4*idx)+"($fp)"))

    # We now push the values into the arg registers (if any)
    for hashReg, idx in hashArgs:
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.argRegs[idx], hashReg))

    for (idx, param) in enumerate(parameters):
        if not param.is_HASH_VARIABLE():
            if idx <= 3:
                codeSegment += param.CopyToRegister(REG.argRegs[idx])

            else:
                codeSegment += param.CopyToMemory(str(4*idx)+"($fp)")

    codeSegment += G.INDENT + "jal Printf\n"
    G.AsmText.AddText(codeSegment)

    # Add library for linking
    G.LibraryFunctionsUsed.add("Printf")
    G.LibraryFunctionsUsed.add("PrintInt")
    G.LibraryFunctionsUsed.add("PrintChar")
    G.LibraryFunctionsUsed.add("PrintString")

def Translate_Scanf(parameters):
    """ Custom version of Scanf can be found in iolib.c in the lib/ folder """

    formatString = parameters[0]

    DEBUG.Assert(formatString.is_STRING(), "First argument of Printf has to be a format specifier")

    G.StackSpaceMap[G.CurrFunction] = max(G.StackSpaceMap[G.CurrFunction], 4*len(parameters))

    codeSegment = ""

    hashRegs = [REG.s3, REG.s2, REG.s1, REG.s0]
    hashArgs = []
    for (idx, param) in enumerate(parameters):
        if param.is_HASH_VARIABLE():
            import translator as TRANS          # Top level import throws an error
            tempReg = REG.tmpUsageRegs[-1]
            regComp = REG.tmpUsageRegs[2]

            if idx <= 3:
                # These are callee saved registers anyway
                reg = hashRegs.pop()
                hashArgs += [[reg, idx]]

                # First allocate memory and store the address returned in the callee saved register
                # We will use this address for our Scanf call
                Translate_alloc(reg)

                TRANS.SetupDestRegHash(param, regComp, tempReg) # The value of key is stored in tempReg

                # Add a new element with valRef as the pointer to the new memory allocated
                Translate_addElement(param, tempReg, reg)

            else:
                # First allocate memory and store the address returned in the temporary register reg
                # We will use this address for our Scanf call
                Translate_alloc(regComp)

                # Move the address to the appropriate location on the stack
                G.AsmText.AddText(G.INDENT + "sw %s, %s"%(regComp, str(4*idx)+"($fp)"))

                TRANS.SetupDestRegHash(param, REG.tmpUsageRegs[1], tempReg) # The value of key is stored in tempReg

                Translate_addElement(param, tempReg, regComp)

    # We now push the values into the arg registers (if any)
    for hashReg, idx in hashArgs:
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.argRegs[idx], hashReg))

    for (idx, param) in enumerate(parameters):
        if not param.is_HASH_VARIABLE():
            if idx <= 3:
                codeSegment += param.CopyAddressToRegister(REG.argRegs[idx])

            else:
                codeSegment += param.CopyAddressToMemory(str(4*idx)+"($fp)")

    codeSegment += G.INDENT + "jal Scanf\n"
    G.AsmText.AddText(codeSegment)

    # Add library for linking
    G.LibraryFunctionsUsed.add("Scanf")
    G.LibraryFunctionsUsed.add("ReadInt")
    G.LibraryFunctionsUsed.add("ReadChar")

def Translate_StrCmp(str1, str2):
    """ Custom version of strCmp can be found in hashlib.c in the lib/ folder """

    DEBUG.Assert(str1.is_STRING(), "First argument of StrCmp has to be a string")
    DEBUG.Assert(str2.is_STRING(), "Second argument of StrCmp has to be a string")

    G.StackSpaceMap[G.CurrFunction] = max(G.StackSpaceMap[G.CurrFunction], 4*len(parameters))

    codeSegment = ""

    codeSegment += str1.CopyToRegister(REG.argRegs[0])
    codeSegment += str2.CopyToRegister(REG.argRegs[1])

    codeSegment += G.INDENT + "jal strCmp\n"
    G.AsmText.AddText(codeSegment)

    # Add library for linking
    G.LibraryFunctionsUsed.add("strCmp")

def Translate_initHash(targetVar):
    """ Hash implementation can be found in hashlib.c in the lib/ folder """

    DEBUG.Assert(targetVar.is_HASH_VARIABLE(), "Argument of initHash should be a hash pointer")

    G.AsmText.AddText(G.INDENT + "li %s, %s"%(REG.argRegs[0], str(G.AsmData.GetHashType(targetVar.value))), "Passing the type of hash")
    G.AsmText.AddText(G.INDENT + "jal initHash", "Allocating memory and initializing the hash")
    G.AsmText.AddText(G.INDENT + "sw $v0, %s"%(ASM.GetHashAddr(targetVar)), "Storing the returned memory address of hash")

    # Add library for linking
    G.LibraryFunctionsUsed.add("initHash")
    G.LibraryFunctionsUsed.add("alloc")

def Translate_getValue(targetVar, idxRegister, targetReg):
    """ Hash implementation can be found in hashlib.c in the lib/ folder """

    DEBUG.Assert(targetVar.is_HASH_VARIABLE(), "Argument of getValue should be a hash pointer")
    G.AsmData.AllocateString(G.HashKeyError)

    G.AsmText.AddText(targetVar.CopyToRegister(REG.argRegs[0])[:-1])

    if G.AsmData.GetHashType(targetVar.value) == 1:
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.argRegs[2], REG.zero), "Zero out the int argument")
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.argRegs[1], idxRegister), "Load key")
    else:
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.argRegs[1], REG.zero), "Zero out the char * argument")
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.argRegs[2], idxRegister), "Load key")

    G.AsmText.AddText(G.HashKeyError.CopyAddressToRegister(REG.argRegs[3])[:-1])

    G.AsmText.AddText(G.INDENT + "jal getValue", "Searching for value in hash")
    G.AsmText.AddText(G.INDENT + "lw %s, 0(%s)"%(targetReg, REG.v0), "Store result back into a designated register")

    # Add library for linking
    G.LibraryFunctionsUsed.add("getValue")
    G.LibraryFunctionsUsed.add("ExitWithMessage")

def Translate_addElement(targetVar, idxRegister, valReg):
    """ Hash implementation can be found in hashlib.c in the lib/ folder """

    DEBUG.Assert(targetVar.is_HASH_VARIABLE(), "Argument of addElement should be a hash pointer")

    G.AsmText.AddText(targetVar.CopyToRegister(REG.argRegs[0])[:-1])

    if G.AsmData.GetHashType(targetVar.value) == 1:
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.argRegs[2], REG.zero), "Zero out the int argument")
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.argRegs[1], idxRegister), "Load key")
    else:
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.argRegs[1], REG.zero), "Zero out the char * argument")
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.argRegs[2], idxRegister), "Load key")

    G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.argRegs[3], valReg), "Load value")

    G.AsmText.AddText(G.INDENT + "jal addElement", "Add element to the hash")

    # Add library for linking
    G.LibraryFunctionsUsed.add("addElement")
    G.LibraryFunctionsUsed.add("findMatch")
    G.LibraryFunctionsUsed.add("strCmp")

def Translate_alloc(targetReg, size=4):

    if type(size) == int:
        G.AsmText.AddText(G.INDENT + "li %s, %s"%(REG.argRegs[0], str(size)), "Load memory size to be allocated")
    else:
        G.AsmText.AddText(size.CopyToRegister(REG.argRegs[0])[:-1], "Load memory size to be allocated")

    G.AsmText.AddText(G.INDENT + "jal alloc", " call malloc")
    G.AsmText.AddText(G.INDENT + "move %s, %s"%(targetReg, REG.v0), "Load returned pointer into targetReg")

    # Add library for linking
    G.LibraryFunctionsUsed.add("alloc")
