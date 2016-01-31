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
# List of Imports End

def Translate__Printf(parameters):
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


def Translate_StrCmp(str1, str2):
    """ Custom version of strCmp can be found in hashlib.c in the lib/ folder """

    DEBUG.Assert(str1.is_STRING(), "First argument of StrCmp has to be a string")
    DEBUG.Assert(str2.is_STRING(), "Second argument of StrCmp has to be a string")

    G.StackSpaceRequired = max(G.StackSpaceRequired, 4*2)

    codeSegment = ""

    codeSegment+= str1.CopyToRegister(REG.argRegs[0])
    codeSegment+= str2.CopyToRegister(REG.argRegs[1])

    codeSegment += G.INDENT + "jal strCmp\n"
    G.AsmText.AddText(codeSegment)
