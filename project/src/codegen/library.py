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
import translator as TRANS

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

def LinkLibData():
    codeData = ""
    insideData = False
    for fileName in G.LIBSRC:
        with open(os.path.dirname(__file__) + "/" + fileName, 'r') as f:
            for line in f:
                if (".text" in line):
                    insideData = False
                    continue

                if (".rdata" in line) or (".sdata" in line) or (".data" in line):
                    insideData = True
                    continue

                if insideData:
                    finalLine = line
                    if ".ascii" in finalLine:
                        finalLine = finalLine.replace(".ascii", ".asciiz")
                        finalLine = finalLine.replace("\\000", "")

                    codeData += finalLine

    return codeData

def AddEssentialLibraries():
    for fileName in G.EssentialLibraries:
        with open(os.path.dirname(__file__) + "/" + fileName, 'r') as f:
            for line in f:
                if ".ent" in line:
                    G.LibraryFunctionsUsed.add(line.split("\t")[-1][:-1])


def Translate_Printf(parameter):
    """ Custom version of Printf can be found in iolib.c in the lib/ folder """

    G.CurrRegAddrTable.DumpDirtyVars()
    G.AsmText.AddText(G.INDENT + "lw %s, %s"%(REG.a0, ASM.GetVarAddr(parameter)), "Passing parameter")
    G.AsmText.AddText(" ")
    G.AsmText.AddText(G.INDENT + "jal Printf")
    G.AsmText.AddText(G.INDENT + "lw %s, 16($fp)"%(REG.a0))

    # Add library for linking
    G.LibraryFunctionsUsed.add("Printf")
    G.LibraryFunctionsUsed.add("PrintInt")
    G.LibraryFunctionsUsed.add("PrintChar")
    G.LibraryFunctionsUsed.add("PrintString")
    G.LibraryFunctionsUsed.add("accessIndex")
    G.LibraryFunctionsUsed.add("lengthOfArray")

def Translate_Scanf(parameters):
    """ Custom version of Scanf can be found in iolib.c in the lib/ folder """

    codeSegment = ""

    G.CurrRegAddrTable.DumpDirtyVars()
    G.AsmText.AddText(" ")
    G.AsmText.AddText(G.INDENT + "jal Scanf")
    G.AsmText.AddText(G.INDENT + "lw %s, 16($fp)"%(REG.a0))

    # Add library for linking
    G.LibraryFunctionsUsed.add("Scanf")
    G.LibraryFunctionsUsed.add("ReadInt")
    G.LibraryFunctionsUsed.add("ReadChar")
    G.LibraryFunctionsUsed.add("ReadString")

def Translate_StrCmp(str1, str2):
    """ Custom version of strCmp can be found in hashlib.c in the lib/ folder """

    DEBUG.Assert(str1.is_VARIABLE(), "First argument of StrCmp has to be a variable")
    DEBUG.Assert(str2.is_VARIABLE(), "Second argument of StrCmp has to be a variable")

    codeSegment = ""

    codeSegment += str1.CopyToRegister(REG.argRegs[0])
    codeSegment += str2.CopyToRegister(REG.argRegs[1])

    codeSegment += G.INDENT + "jal strCmp\n"
    G.AsmText.AddText(codeSegment)
    G.AsmText.AddText(G.INDENT + "lw %s, 16($fp)"%(REG.a0))

    # Add library for linking
    G.LibraryFunctionsUsed.add("strCmp")

def Translate_initHash(targetVar):
    """ Hash implementation can be found in hashlib.c in the lib/ folder """

    #DEBUG.Assert(targetVar.is_HASH_VARIABLE(), "Argument of initHash should be a hash pointer")

    #G.AsmText.AddText(G.INDENT + "li %s, %s"%(REG.argRegs[0], str(G.AsmData.GetHashType(targetVar.value))), "Passing the type of hash")
    G.AsmText.AddText(G.INDENT + "jal initHash", "Allocating memory and initializing the hash")
    G.AsmText.AddText(G.INDENT + "sw $v0, %s"%(ASM.GetVarAddr(targetVar)), "Storing the returned memory address of hash")
    G.AsmText.AddText(G.INDENT + "lw %s, 16($fp)"%(REG.a0))

    # Add library for linking
    G.LibraryFunctionsUsed.add("initHash")
    G.LibraryFunctionsUsed.add("alloc")

def Translate_initArray(targetVar):
    """ Array implemented can be found in arraylib.c in the lib/ folder """

    G.AsmText.AddText(G.INDENT + "jal initArray", "Allocating memory and initializing the array")
    G.AsmText.AddText(G.INDENT + "sw $v0, %s"%(ASM.GetVarAddr(targetVar)), "Storing the returned memory address of array")
    G.AsmText.AddText(G.INDENT + "lw %s, 16($fp)"%(REG.a0))

    # Add library for linking
    G.LibraryFunctionsUsed.add("initArray")
    G.LibraryFunctionsUsed.add("alloc")

def Translate_getArrayValue(targetVar, idxRegister, targetReg):
    """ Array implementation can be found in arraylib.c in the lib/ folder """

    DEBUG.Assert(targetVar.is_ARRAY_VARIABLE(), "Argument of getValue should be an array pointer")

    G.AsmText.AddText(targetVar.CopyToRegister(REG.argRegs[0])[:-1])
    G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.argRegs[1], idxRegister))

    G.AsmText.AddText(G.INDENT + "jal accessIndex", "Searching for value in array")
    G.AsmText.AddText(G.INDENT + "lw %s, 0(%s)"%(targetReg, REG.v0), "Store result back into a designated register")
    G.AsmText.AddText(G.INDENT + "lw %s, 16($fp)"%(REG.a0))

    # Add library for linking
    G.LibraryFunctionsUsed.add("accessIndex")
    G.LibraryFunctionsUsed.add("lengthOfArray")
    G.LibraryFunctionsUsed.add("ExitWithMessage")

def Translate_getArrayValueType(targetVar, idxRegister, targetReg):
    """ Array implementation can be found in arraylib.c in the lib/ folder """

    DEBUG.Assert(targetVar.is_ARRAY_VARIABLE(), "Argument of getValue should be an array pointer")

    G.AsmText.AddText(targetVar.CopyToRegister(REG.argRegs[0])[:-1])
    G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.argRegs[1], idxRegister))

    G.AsmText.AddText(G.INDENT + "jal accessIndexType", "Searching for value in array")
    G.AsmText.AddText(G.INDENT + "lw %s, 0(%s)"%(targetReg, REG.v0), "Store result back into a designated register")
    G.AsmText.AddText(G.INDENT + "lw %s, 16($fp)"%(REG.a0))

    # Add library for linking
    G.LibraryFunctionsUsed.add("accessIndexType")
    G.LibraryFunctionsUsed.add("lengthOfArray")
    G.LibraryFunctionsUsed.add("ExitWithMessage")

def Translate_getArrayIndexAddress(targetVar, idxRegister, targetReg):
    """ Array implementation can be found in arraylib.c in the lib/ folder """

    DEBUG.Assert(targetVar.is_ARRAY_VARIABLE(), "Argument of getValue should be an array pointer")

    G.AsmText.AddText(targetVar.CopyToRegister(REG.argRegs[0])[:-1])
    G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.argRegs[1], idxRegister))

    G.AsmText.AddText(G.INDENT + "jal accessIndex", "Searching for address in array")
    G.AsmText.AddText(G.INDENT + "move %s, %s"%(targetReg, REG.v0), "Store result back into a designated register")
    G.AsmText.AddText(G.INDENT + "lw %s, 16($fp)"%(REG.a0))

    # Add library for linking
    G.LibraryFunctionsUsed.add("accessIndex")
    G.LibraryFunctionsUsed.add("lengthOfArray")
    G.LibraryFunctionsUsed.add("ExitWithMessage")

def Translate_getArrayIndexAddressType(targetVar, idxRegister, targetReg):
    """ Array implementation can be found in arraylib.c in the lib/ folder """

    DEBUG.Assert(targetVar.is_ARRAY_VARIABLE(), "Argument of getValue should be an array pointer")

    G.AsmText.AddText(targetVar.CopyToRegister(REG.argRegs[0])[:-1])
    G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.argRegs[1], idxRegister))

    G.AsmText.AddText(G.INDENT + "jal accessIndexType", "Searching for address in array")
    G.AsmText.AddText(G.INDENT + "move %s, %s"%(targetReg, REG.v0), "Store result back into a designated register")
    G.AsmText.AddText(G.INDENT + "lw %s, 16($fp)"%(REG.a0))

    # Add library for linking
    G.LibraryFunctionsUsed.add("accessIndexType")
    G.LibraryFunctionsUsed.add("lengthOfArray")
    G.LibraryFunctionsUsed.add("ExitWithMessage")

def Translate_getHashValue(targetVar, idxRegister, targetReg):
    """ Hash implementation can be found in hashlib.c in the lib/ folder """

    DEBUG.Assert(targetVar.is_HASH_VARIABLE(), "Argument of getValue should be a hash pointer")

    G.AsmText.AddText(targetVar.CopyToRegister(REG.argRegs[0])[:-1])

    G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.argRegs[1], idxRegister), "Load key")

    G.AsmText.AddText(G.INDENT + "jal getHashValue", "Searching for value in hash")
    G.AsmText.AddText(G.INDENT + "move %s, %s"%(targetReg, REG.v0), "Store result back into a designated register")
    G.AsmText.AddText(G.INDENT + "lw %s, 16($fp)"%(REG.a0))

    # Add library for linking
    G.LibraryFunctionsUsed.add("getHashValue")
    G.LibraryFunctionsUsed.add("ExitWithMessage")

def Translate_getHashValueType(targetVar, idxRegister, targetReg):
    """ Hash implementation can be found in hashlib.c in the lib/ folder """

    DEBUG.Assert(targetVar.is_HASH_VARIABLE(), "Argument of getValue should be a hash pointer")

    G.AsmText.AddText(targetVar.CopyToRegister(REG.argRegs[0])[:-1])

    G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.argRegs[1], idxRegister), "Load key")

    G.AsmText.AddText(G.INDENT + "jal getHashValueType", "Searching for value in hash")
    G.AsmText.AddText(G.INDENT + "move %s, %s"%(targetReg, REG.v0), "Store result back into a designated register")
    G.AsmText.AddText(G.INDENT + "lw %s, 16($fp)"%(REG.a0))

    # Add library for linking
    G.LibraryFunctionsUsed.add("getHashValueType")
    G.LibraryFunctionsUsed.add("ExitWithMessage")


def Translate_addElement(targetVar, idxRegister, valReg):
    """ Hash implementation can be found in hashlib.c in the lib/ folder """

    DEBUG.Assert(targetVar.is_HASH_VARIABLE(), "Argument of addElement should be a hash pointer")

    G.AsmText.AddText(targetVar.CopyToRegister(REG.argRegs[0])[:-1])

    G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.argRegs[1], idxRegister), "Load key")

    G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.argRegs[2], valReg), "Load value")

    G.AsmText.AddText(" ")
    G.AsmText.AddText(G.INDENT + "jal addElement", "Add element to the hash")
    G.AsmText.AddText(G.INDENT + "lw %s, 16($fp)"%(REG.a0))

    # Add library for linking
    G.LibraryFunctionsUsed.add("addElement")
    G.LibraryFunctionsUsed.add("findMatch")
    G.LibraryFunctionsUsed.add("strCmp")

def Translate_addElementType(targetVar, idxRegister, valReg):
    """ Hash implementation can be found in hashlib.c in the lib/ folder """

    DEBUG.Assert(targetVar.is_HASH_VARIABLE(), "Argument of addElement should be a hash pointer")

    G.AsmText.AddText(targetVar.CopyToRegister(REG.argRegs[0])[:-1])

    G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.argRegs[1], idxRegister), "Load key")

    G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.argRegs[2], valReg), "Load value")

    G.AsmText.AddText(" ")
    G.AsmText.AddText(G.INDENT + "jal addElementType", "Add element to the hash")
    G.AsmText.AddText(G.INDENT + "lw %s, 16($fp)"%(REG.a0))

    # Add library for linking
    G.LibraryFunctionsUsed.add("addElementType")
    G.LibraryFunctionsUsed.add("findMatch")
    G.LibraryFunctionsUsed.add("strCmp")

def Translate_alloc(targetReg, sizeEntity=4):

    if type(sizeEntity) == int:
        G.AsmText.AddText(G.INDENT + "li %s, %s"%(REG.argRegs[0], str(sizeEntity)), "Load memory size to be allocated")
    else:
        if sizeEntity.is_HASH_VARIABLE():
            G.AsmText.AddComment("Readying hash argument for size: %s"%(sizeEntity))
            tempReg = REG.tmpUsageRegs[-1]
            regComp = REG.tmpUsageRegs[2]

            if sizeEntity.key.is_NUMBER():
                G.AsmText.AddText(tempReg.LoadImmediate(sizeEntity.key.value), "Load key for the hash access")
            else:
                regInp = TRANS.SetupRegister(sizeEntity.key, regComp)
                G.AsmText.AddText(G.INDENT + "move %s, %s"%(tempReg, regInp), "Load key for the hash access")

            Translate_getValue(sizeEntity, tempReg, regComp) 

            G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.argRegs[0], regComp), "Load size as second argument")
        else:
            G.AsmText.AddComment("Readying argument : %s"%(sizeEntity))
            G.AsmText.AddText(sizeEntity.CopyToRegister(REG.argRegs[0])[:-1])

    G.CurrRegAddrTable.DumpDirtyVars()

    G.AsmText.AddText(G.INDENT + "jal alloc", "Call malloc")
    if targetReg != REG.v0:
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(targetReg, REG.v0), "Load returned pointer into targetReg")
    G.AsmText.AddText(G.INDENT + "lw %s, 16($fp)"%(REG.a0))

    # Add library for linking
    G.LibraryFunctionsUsed.add("alloc")
