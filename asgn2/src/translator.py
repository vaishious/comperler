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
        # We can safely clobber registers here because this is the last
        # instruction of the basic block

        G.CurrRegAddrTable.DumpDirtyVars()
        Translate_IFGOTO(instr)

def SetupRegisters(inp1, inp2, regClob1, regClob2):
    # Setup the registers, clobbering register regClob1 or regClob2, if required

    reg1 = None
    reg2 = None

    if inp1.is_VARIABLE() and inp2.is_VARIABLE():
        # These variables have already been loaded into registers,
        # as register allocation has been done for this instruction
        reg1 = G.AllocMap[inp1.value]
        reg2 = G.AllocMap[inp2.value]

    elif inp1.is_VARIABLE() and inp2.is_NUMBER():
        reg1 = G.AllocMap[inp1.value]

        # Don't clobber the register corresponding to the variable
        if regClob1 == reg1:
            reg2 = regClob2
        else:
            reg2 = regClob1
        G.AsmText.AddText(reg2.LoadImmediate(inp2.value))

    elif inp1.is_NUMBER() and inp2.is_VARIABLE():
        reg2 = G.AllocMap[inp2.value]

        # Don't clobber the register corresponding to the variable
        if regClob1 == reg2:
            reg1 = regClob2
        else:
            reg1 = regClob1
        G.AsmText.AddText(reg1.LoadImmediate(inp1.value))

    elif inp1.is_NUMBER() and inp2.is_NUMBER():
        reg1 = regClob1
        reg2 = regClob2
        G.AsmText.AddText(reg1.LoadImmediate(inp1.value))
        G.AsmText.AddText(reg2.LoadImmediate(inp2.value))

    else:
        pass

    return reg1,reg2

def Translate_IFGOTO(instr):
    optype = INSTRUCTION.OperationType
    cmp_ops = [optype.LT, optype.GT, optype.LEQ, optype.GEQ, optype.EQ]
    
    DEBUG.Assert(instr.opType.opType in cmp_ops,"Invalid operator for IFGOTO.")

    # If operands are strings
    if StrTranslate_IFGOTO(instr):
        return

    # Instead of separately handling the cases in which one or both of
    # the operands is a number, load both operands into registers and 
    # operate only on the registers.
    reg1, reg2 = SetupRegisters(instr.inp1, instr.inp2, REG.t1, REG.t2)

    if instr.opType.is_EQ():
        G.AsmText.AddText(G.INDENT + "beq %s, %s, L_%d"%(reg1, reg2, instr.jmpTarget))

    elif instr.opType.is_LT():
        G.AsmText.AddText(G.INDENT + "slt %s, %s, %s"%(reg1, reg1, reg2))
        G.AsmText.AddText(G.INDENT + "bgtz %s, L_%d"%(reg1, instr.jmpTarget))

    elif instr.opType.is_GT():
        G.AsmText.AddText(G.INDENT + "slt %s, %s, %s"%(reg1, reg2, reg1))
        G.AsmText.AddText(G.INDENT + "bgtz %s, L_%d"%(reg1, instr.jmpTarget))

    elif instr.opType.is_LEQ():
        G.AsmText.AddText(G.INDENT + "slt %s, %s, %s"%(reg1, reg2, reg1))
        G.AsmText.AddText(G.INDENT + "beq %s, %s, L_%d"%(reg1, REG.zero, instr.jmpTarget))

    elif instr.opType.is_GEQ():
        G.AsmText.AddText(G.INDENT + "slt %s, %s, %s"%(reg1, reg1, reg2))
        G.AsmText.AddText(G.INDENT + "beq %s, %s, L_%d"%(reg1, REG.zero, instr.jmpTarget))

def StrTranslate_IFGOTO(instr):
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
            return True
        return False
