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
    for fileName in G.LIBSRC:
        with open(os.path.dirname(__file__) + "/" + fileName, 'r') as f:
            for line in f:
                if insideFunc:
                    codeFunc += line
                    if (".end" in line) and (funcName in line):
                        return codeFunc

                elif funcName + ":" in line:
                    insideFunc = True
                    codeFunc += line

    return ""

def Translate_Printf(parameters):
    """ Custom version of Printf can be found in iolib.c in the lib/ folder """

    formatString = parameters[0]

    DEBUG.Assert(formatString.is_STRING(), "First argument of Printf has to be a format specifier")

    G.StackSpaceRequired = max(G.StackSpaceRequired, 4*len(parameters))

    codeSegment = ""

    for (idx, param) in enumerate(parameters):
        if idx <= 3:
            codeSegment += parameters[idx].CopyToRegister(REG.argRegs[idx])

        else:
            codeSegment += parameters[idx].CopyToMemory(str(4*idx)+"($sp)")

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

    G.StackSpaceRequired = max(G.StackSpaceRequired, 4*len(parameters))

    codeSegment = ""

    for (idx, param) in enumerate(parameters):
        if idx <= 3:
            codeSegment += parameters[idx].CopyAddressToRegister(REG.argRegs[idx])

        else:
            codeSegment += parameters[idx].CopyAddressToMemory(str(4*idx)+"($sp)")

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

    G.StackSpaceRequired = max(G.StackSpaceRequired, 4*2)

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

    G.AsmText.AddText(G.INDENT + "li %s, %s"%(REG.v0, str(G.AsmData.GetHashType(targetVar.value))), "Passing the type of hash")
    G.AsmText.AddText(G.INDENT + "jal initHash", "Allocating memory and initializing the hash")
    G.AsmText.AddText(G.INDENT + "sw $v0, %s"%(ASM.GetHashAddr(targetVar)), "Storing the returned memory address of hash")

    # Add library for linking
    G.LibraryFunctionsUsed.add("initHash")
    G.LibraryFunctionsUsed.add("alloc")

def Translate_getValue(targetVar, idxRegister, targetReg):
    """ Hash implementation can be found in hashlib.c in the lib/ folder """

    DEBUG.Assert(targetVar.is_HASH_VARIABLE(), "Argument of getValue should be a hash pointer")
    G.AsmData.AllocateString(G.HashKeyError)

    G.AsmText.AddText(target.CopyToRegister(REG.argRegs[0])[:-1])

    if G.AsmData.GetHashType(targetVar.value) == 1:
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.argRegs[1], idxRegister), "Load key")
    else:
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
    G.AsmData.AllocateString(G.HashKeyError)

    G.AsmText.AddText(targetVar.CopyToRegister(REG.argRegs[0])[:-1])

    if G.AsmData.GetHashType(targetVar.value) == 1:
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.argRegs[1], idxRegister), "Load key")
    else:
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.argRegs[2], idxRegister), "Load key")

    G.AsmText.AddText(G.INDENT + "la %s, 0(%s)"%(REG.argRegs[3], valReg), "Load value")

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
