"""

MODULE  : translator.py

Purpose : Contains the main translation function.

Import Acronym : TRANS

"""
# List of Imports Begin
import debug as DEBUG
import instr3ac as INSTRUCTION
import registers as REG
import global_objects as G
import translator as TRANS
# List of Imports End


def Translate(instr):
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
