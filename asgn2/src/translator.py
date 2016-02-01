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
import mips_assembly as ASM
# List of Imports End

def Translate(instr):
    if instr.instrType.is_DECLARE():
        pass

    elif instr.instrType.is_GOTO():
        G.CurrRegAddrTable.DumpDirtyVars()
        G.AsmText.AddText(G.INDENT + "j $LID_%d"%(instr.jmpTarget))

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

    elif instr.instrType.is_ASSIGN():
        Translate_ASSIGN(instr)

def SetupRegister(inp, regComp, tempReg=REG.t9):
    # Setup the input in a register, using regComp, if required
    # TODO : Handle Array and Hash Variables

    reg = None
    if inp.is_SCALAR_VARIABLE():
        # This variable has already been loaded into a register,
        # as register allocation has been done for this instruction
        try:
            reg = G.AllocMap[inp.value]
        except:
            # This can only happen if this variable is an index of an array
            # in which case, we directly load it from its register or from
            # memory
            if inp.IsRegisterAllocated():
                reg = inp.GetCurrReg()
            else:
                reg.CopyToRegister(regComp)

    elif inp.is_NUMBER():
        reg = regComp
        G.AsmText.AddText(reg.LoadImmediate(inp.value))

    elif inp.is_ARRAY_VARIABLE():
        # First we need the index
        regInp = None
        if inp.key.is_NUMBER():
            G.AsmText.AddText(tempReg.LoadImmediate(inp.key.value))
        else:
            regInp = SetupRegister(inp.key, regComp)
            G.AsmText.AddText(G.INDENT + "move %s, %s"%(tempReg, regInp))

        # Load the array address in regComp
        G.AsmText.AddText(G.INDENT + "la %s, %s"%(regComp, ASM.GetArrAddr(inp.value)))

        # We move the index value to tempReg to multiply it by 4
        G.AsmText.AddText(G.INDENT + "sll %s, %s, 2"%(tempReg, tempReg))
        G.AsmText.AddText(G.INDENT + "add %s, %s, %s"%(regComp, regComp, tempReg))
        G.AsmText.AddText(G.INDENT + "lw %s, 0(%s)"%(regComp, regComp))

        reg = regComp

    DEBUG.Assert(reg, "Line %d: Unable to setup register for %s."%(G.CurrInstruction.lineID, str(inp.value)))
    return reg

def Translate_IFGOTO(instr):
    optype = INSTRUCTION.OperationType
    cmp_ops = [optype.LT, optype.GT, optype.LEQ, optype.GEQ, optype.EQ, optype.NE]
    
    DEBUG.Assert(instr.opType.opType in cmp_ops,"Invalid operator for IFGOTO.")

    # If operands are strings
    if StrTranslate_IFGOTO(instr):
        return

    # Instead of separately handling the cases in which one or both of
    # the operands is a number, load both operands into registers and 
    # operate only on the registers.
    reg1 = SetupRegister(instr.inp1, REG.tmpUsageRegs[0])
    reg2 = SetupRegister(instr.inp2, REG.tmpUsageRegs[1])

    if instr.opType.is_EQ():
        G.AsmText.AddText(G.INDENT + "beq %s, %s, $LID_%d"%(reg1, reg2, instr.jmpTarget))

    elif instr.opType.is_NE():
        G.AsmText.AddText(G.INDENT + "bne %s, %s, $LID_%d"%(reg1, reg2, instr.jmpTarget))

    elif instr.opType.is_LT():
        G.AsmText.AddText(G.INDENT + "slt %s, %s, %s"%(reg1, reg1, reg2))
        G.AsmText.AddText(G.INDENT + "bgtz %s, $LID_%d"%(reg1, instr.jmpTarget))

    elif instr.opType.is_GT():
        G.AsmText.AddText(G.INDENT + "slt %s, %s, %s"%(reg1, reg2, reg1))
        G.AsmText.AddText(G.INDENT + "bgtz %s, $LID_%d"%(reg1, instr.jmpTarget))

    elif instr.opType.is_LEQ():
        G.AsmText.AddText(G.INDENT + "slt %s, %s, %s"%(reg1, reg2, reg1))
        G.AsmText.AddText(G.INDENT + "beq %s, %s, $LID_%d"%(reg1, REG.zero, instr.jmpTarget))

    elif instr.opType.is_GEQ():
        G.AsmText.AddText(G.INDENT + "slt %s, %s, %s"%(reg1, reg1, reg2))
        G.AsmText.AddText(G.INDENT + "beq %s, %s, $LID_%d"%(reg1, REG.zero, instr.jmpTarget))

def StrTranslate_IFGOTO(instr):
    if instr.inp1.is_STRING() and instr.inp2.is_STRING():
        LIB.Translate_StrCmp(instr.inp1,instr.inp2)
        if instr.opType.is_EQ():
            G.AsmText.AddText(G.INDENT + "beqz $v0, $LID_%d"%(instr.jmpTarget))
        if instr.opType.is_NE():
            G.AsmText.AddText(G.INDENT + "bne $v0, %s, $LID_%d"%(REG.zero, instr.jmpTarget))
        elif instr.opType.is_GEQ():
            G.AsmText.AddText(G.INDENT + "bgez $v0, $LID_%d"%(instr.jmpTarget))
        elif instr.opType.is_LEQ():
            G.AsmText.AddText(G.INDENT + "blez $v0, $LID_%d"%(instr.jmpTarget))
        elif instr.opType.is_LT():
            G.AsmText.AddText(G.INDENT + "bgtz $v0, $LID_%d"%(instr.jmpTarget))
        elif instr.opType.is_GT():
            G.AsmText.AddText(G.INDENT + "bltz $v0, $LID_%d"%(instr.jmpTarget))
        return True
    return False

def Translate_ASSIGN(instr):
    if (not instr.opType.is_NONE()) and (not instr.inp2.is_NONE()):
        # dest = inp1 OP inp2

        reg1 = SetupRegister(instr.inp1,REG.tmpUsageRegs[0])
        reg2 = SetupRegister(instr.inp2,REG.tmpUsageRegs[1])

        # TODO : Handle array and hash variables in the destination
        if instr.dest.is_SCALAR_VARIABLE():
            reg3 = G.AllocMap[instr.dest.value]
            GenCode_3OPASSIGN(instr, reg3, reg1, reg2)

        elif instr.dest.is_ARRAY_VARIABLE():
            tempReg = REG.tmpUsageRegs[-1]
            regComp = REG.tmpUsageRegs[2]

            if instr.dest.key.is_NUMBER():
                G.AsmText.AddText(tempReg.LoadImmediate(instr.dest.key.value))
            else:
                regInp = SetupRegister(instr.dest.key, regComp)
                G.AsmText.AddText(G.INDENT + "move %s, %s"%(tempReg, regInp))

            # Load the array address in regComp
            G.AsmText.AddText(G.INDENT + "la %s, %s"%(regComp, ASM.GetArrAddr(instr.dest.value)))

            # We move the index value to tempReg to multiply it by 4
            G.AsmText.AddText(G.INDENT + "sll %s, %s, 2"%(tempReg, tempReg))
            G.AsmText.AddText(G.INDENT + "add %s, %s, %s"%(regComp, regComp, tempReg))

            # We will reuse tempReg as the dest register. We will then write it back to the
            # address location in the array
            GenCode_3OPASSIGN(instr, tempReg, reg1, reg2)

            # Store back the value
            G.AsmText.AddText(G.INDENT + "sw %s, 0(%s)"%(tempReg, regComp))

def GenCode_3OPASSIGN(instr, regDest, regInp1, regInp2):
    # Currently ignoring overflows everywhere
    if instr.opType.is_PLUS():
        G.AsmText.AddText(G.INDENT + "addu %s, %s, %s"%(regDest, regInp1, regInp2))

    elif instr.opType.is_MINUS():
        G.AsmText.AddText(G.INDENT + "subu %s, %s, %s"%(regDest, regInp1, regInp2))

    elif instr.opType.is_MULT():
        G.AsmText.AddText(G.INDENT + "multu %s, %s"%(regInp1, regInp2))
        G.AsmText.AddText(G.INDENT + "mflo %s"%(regDest))

    elif instr.opType.is_DIV():
        G.AsmText.AddText(G.INDENT + "divu %s, %s"%(regInp1, regInp2))
        G.AsmText.AddText(G.INDENT + "mflo %s"%(regDest))

    elif instr.opType.is_MOD():
        G.AsmText.AddText(G.INDENT + "divu %s, %s"%(regInp1, regInp2))
        G.AsmText.AddText(G.INDENT + "mfhi %s"%(regDest))

    elif instr.opType.is_LT():
        G.AsmText.AddText(G.INDENT + "slt %s, %s, %s"%(regDest, regInp1, regInp2))

    elif instr.opType.is_GT():
        G.AsmText.AddText(G.INDENT + "slt %s, %s, %s"%(regDest, regInp2, regInp1))

    elif instr.opType.is_GEQ():
        G.AsmText.AddText(G.INDENT + "slt %s, %s, %s"%(regDest, regInp1, regInp2))
        G.AsmText.AddText(G.INDENT + "nor %s, %s, %s"%(regDest, regDest, regDest))

    elif instr.opType.is_LEQ():
        G.AsmText.AddText(G.INDENT + "slt %s, %s, %s"%(regDest, regInp2, regInp1))
        G.AsmText.AddText(G.INDENT + "nor %s, %s, %s"%(regDest, regDest, regDest))

    elif instr.opType.is_EQ():
        regTmp = REG.tmpUsageRegs[0]
        G.AsmText.AddText(G.INDENT + "slt %s, %s, %s"%(regDest, regInp1, regInp2))
        G.AsmText.AddText(G.INDENT + "slt %s, %s, %s"%(regTmp, regInp2, regInp1))
        G.AsmText.AddText(G.INDENT + "nor %s, %s, %s"%(regDest, regDest, regTmp))

    elif instr.opType.is_NE():
        regTmp = REG.tmpUsageRegs[0]
        G.AsmText.AddText(G.INDENT + "slt %s, %s, %s"%(regDest, regInp1, regInp2))
        G.AsmText.AddText(G.INDENT + "slt %s, %s, %s"%(regTmp, regInp2, regInp1))
        G.AsmText.AddText(G.INDENT + "or %s, %s, %s"%(regDest, regDest, regTmp))
