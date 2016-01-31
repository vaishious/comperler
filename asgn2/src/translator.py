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
import library as LIB
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

    elif instr.instrType.is_IFGOTO():
        G.CurrRegAddrTable.DumpDirtyVars()
        if instr.inp1.is_STRING() and instr.inp2.is_STRING():
            LIB.Translate_StrCmp(instr.inp1,instr.inp2)
            if instr.opType.is_EQ():
                G.AsmText.AddText(G.INDENT + "beqz $v0, L_%d"%(instr.jmpTarget))
            elif instr.opType.is_GEQ():
                G.AsmText.AddText(G.INDENT + "bgez $v0, L_%d"%(instr.jmpTarget))
            elif instr.opType.is_LEQ():
                G.AsmText.AddText(G.INDENT + "blez $v0, L_%d"%(instr.jmpTarget))
            elif instr.opType.is_LT():
                G.AsmText.AddText(G.INDENT + "bgtz $v0, L_%d"%(instr.jmpTarget))
            elif instr.opType.is_GT():
                G.AsmText.AddText(G.INDENT + "bltz $v0, L_%d"%(instr.jmpTarget))
