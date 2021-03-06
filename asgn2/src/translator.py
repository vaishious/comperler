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
        if instr.inp1.is_HASH_VARIABLE():
            G.CurrRegAddrTable.DumpDirtyVars()
            G.CurrRegAddrTable.Reset()
            G.AllocMap = {}
            LIB.Translate_initHash(instr.inp1)

    elif instr.instrType.is_EXIT():
        G.CurrRegAddrTable.DumpDirtyVars()
        G.AsmText.AddText(G.INDENT + "li %s, 10"%(REG.v0))
        G.AsmText.AddText(G.INDENT + "syscall")

    elif instr.instrType.is_GOTO():
        G.CurrRegAddrTable.DumpDirtyVars()
        G.AsmText.AddText(G.INDENT + "j %s"%(instr.jmpTarget))

    elif instr.instrType.is_CALL():
        G.CurrRegAddrTable.DumpDirtyVars()
        G.AsmText.AddText(G.INDENT + "jal %s"%(instr.jmpLabel))
        if instr.dest.is_VARIABLE():
            GenCode_CallAssignment(instr)

    elif instr.instrType.is_PRINT():
        if instr.ContainsHashAccess():
            G.CurrRegAddrTable.DumpDirtyVars()
        LIB.Translate_Printf(instr.IOArgs)

    elif instr.instrType.is_READ():
        if instr.ContainsHashAccess():
            G.CurrRegAddrTable.DumpDirtyVars()
        LIB.Translate_Scanf(instr.IOArgs)

    elif instr.instrType.is_ALLOC():
        if instr.ContainsHashAccess():
            G.CurrRegAddrTable.DumpDirtyVars()
        GenCode_Alloc(instr)

    elif instr.instrType.is_RETURN():
        if not instr.inp1.is_NONE():
            reg = SetupRegister(instr.inp1, REG.v0)
            if reg != REG.v0:
                G.AsmText.AddText(G.INDENT + "move %s, %s\n"%(REG.v0, reg), "Storing return value in $v0")

        G.CurrRegAddrTable.DumpDirtyVars()
        stackSpaceRequired = G.StackSpaceMap[G.CurrFunction] + 24
        G.AsmText.AddText(G.INDENT + "move $sp, $fp", "Restore the stack pointer")
        #G.AsmText.AddText(G.INDENT + "lw $fp, %d($sp)"%(stackSpaceRequired-4), "Reload the fp from previous call")
        #G.AsmText.AddText(G.INDENT + "lw $ra, %d($sp)"%(stackSpaceRequired-8), "Reload the ra of current call")
        G.AsmText.AddText("%s_return:"%G.CurrFunction)
        G.AsmText.AddText(G.INDENT + "jr $ra")

    elif instr.instrType.is_IFGOTO() or instr.instrType.is_STRIFGOTO():
        # We can safely clobber registers here because this is the last
        # instruction of the basic block
        if (instr.dest.is_HASH_VARIABLE() or 
            instr.inp1.is_HASH_VARIABLE() or
            instr.inp2.is_HASH_VARIABLE()):

            G.CurrRegAddrTable.DumpDirtyVars()
            G.CurrRegAddrTable.Reset()
            G.AllocMap = {}

        G.CurrRegAddrTable.DumpDirtyVars()
        Translate_IFGOTO(instr)

    elif instr.instrType.is_ASSIGN():
        if (instr.dest.is_HASH_VARIABLE() or 
            instr.inp1.is_HASH_VARIABLE() or
            instr.inp2.is_HASH_VARIABLE()):

            G.CurrRegAddrTable.DumpDirtyVars()
            G.CurrRegAddrTable.Reset()
            G.AllocMap = {}

        Translate_ASSIGN(instr)

def SetupRegister(inp, regComp, tempReg=REG.t9, useImmediate=False):
    # Setup the input in a register, using regComp, if required

    reg = None
    if inp.is_SCALAR_VARIABLE():
        # This variable has already been loaded into a register,
        # as register allocation has been done for this instruction
        try:
            reg = G.AllocMap[inp.value]
        except:
            # This can only happen if this variable is an index of an array
            # in which case, we directly load it from its register or from
            # memory. It can also happen when we're dealing with hashes as it
            # requires a function call and everything will be wiped out.
            if inp.IsRegisterAllocated():
                reg = inp.GetCurrReg()
            else:
                G.AsmText.AddText(inp.CopyToRegister(regComp)[:-1])
                reg = regComp

    elif inp.is_NUMBER():
        if useImmediate:
            reg = str(inp.value)
        else:
            reg = regComp
            G.AsmText.AddText(reg.LoadImmediate(inp.value))

    elif inp.is_STRING():
        reg = regComp
        G.AsmText.AddText(inp.CopyToRegister(reg)[:-1])

    elif inp.is_ARRAY_VARIABLE():
        # First we need the index
        regInp = None
        if inp.key.is_NUMBER():
            G.AsmText.AddText(tempReg.LoadImmediate(inp.key.value), "Load index for the array access")
        else:
            regInp = SetupRegister(inp.key, regComp)
            G.AsmText.AddText(G.INDENT + "move %s, %s"%(tempReg, regInp), "Load index for the array access")

        # Load the array address in regComp
        G.AsmText.AddText(G.INDENT + "la %s, %s"%(regComp, ASM.GetArrAddr(inp.value)), "Load array address")

        # We move the index value to tempReg to multiply it by 4
        G.AsmText.AddText(G.INDENT + "sll %s, %s, 2"%(tempReg, tempReg), "Multiply index by 4")
        G.AsmText.AddText(G.INDENT + "add %s, %s, %s"%(regComp, regComp, tempReg), "Add index as an offset to array address")
        G.AsmText.AddText(G.INDENT + "lw %s, 0(%s)"%(regComp, regComp), "Extract array value")

        reg = regComp

    elif inp.is_HASH_VARIABLE():
        # First we need the key
        regInp = None
        if inp.key.is_NUMBER():
            G.AsmText.AddText(tempReg.LoadImmediate(inp.key.value), "Load key for the hash access")
        else:
            regInp = SetupRegister(inp.key, regComp)
            G.AsmText.AddText(G.INDENT + "move %s, %s"%(tempReg, regInp), "Load key for the hash access")

        LIB.Translate_getValue(inp, tempReg, regComp) 
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
    reg2 = SetupRegister(instr.inp2, REG.tmpUsageRegs[1], useImmediate=True)

    if instr.opType.is_EQ():
        G.AsmText.AddText(G.INDENT + "beq %s, %s, %s"%(reg1, reg2, instr.jmpTarget))

    elif instr.opType.is_NE():
        G.AsmText.AddText(G.INDENT + "bne %s, %s, %s"%(reg1, reg2, instr.jmpTarget))

    elif instr.opType.is_LT():
        if reg2 == "0":
            G.AsmText.AddText(G.INDENT + "bltz %s, %s"%(reg1, instr.jmpTarget))
        else:
            G.AsmText.AddText(G.INDENT + "slt %s, %s, %s"%(reg1, reg1, reg2))
            G.AsmText.AddText(G.INDENT + "bgtz %s, %s"%(reg1, instr.jmpTarget))

    elif instr.opType.is_GT():
        if reg2 == "0":
            G.AsmText.AddText(G.INDENT + "bgtz %s, %s"%(reg1, instr.jmpTarget))
        else:
            G.AsmText.AddText(G.INDENT + "sgt %s, %s, %s"%(reg1, reg1, reg2))
            G.AsmText.AddText(G.INDENT + "bgtz %s, %s"%(reg1, instr.jmpTarget))

    elif instr.opType.is_LEQ():
        if reg2 == "0":
            G.AsmText.AddText(G.INDENT + "blez %s, %s"%(reg1, instr.jmpTarget))
        else:
            G.AsmText.AddText(G.INDENT + "sle %s, %s, %s"%(reg1, reg1, reg2))
            G.AsmText.AddText(G.INDENT + "bgtz %s, %s"%(reg1, instr.jmpTarget))

    elif instr.opType.is_GEQ():
        if reg2 == "0":
            G.AsmText.AddText(G.INDENT + "bgez %s, %s"%(reg1, instr.jmpTarget))
        else:
            G.AsmText.AddText(G.INDENT + "sge %s, %s, %s"%(reg1, reg1, reg2))
            G.AsmText.AddText(G.INDENT + "bgtz %s, %s"%(reg1, instr.jmpTarget))

def StrTranslate_IFGOTO(instr):
    if instr.instrType.is_STRIFGOTO():
        LIB.Translate_StrCmp(instr.inp1,instr.inp2)
        if instr.opType.is_EQ():
            G.AsmText.AddText(G.INDENT + "beqz $v0, %s"%(instr.jmpTarget))
        if instr.opType.is_NE():
            G.AsmText.AddText(G.INDENT + "bne $v0, %s, %s"%(REG.zero, instr.jmpTarget))
        elif instr.opType.is_GEQ():
            G.AsmText.AddText(G.INDENT + "bgez $v0, %s"%(instr.jmpTarget))
        elif instr.opType.is_LEQ():
            G.AsmText.AddText(G.INDENT + "blez $v0, %s"%(instr.jmpTarget))
        elif instr.opType.is_LT():
            G.AsmText.AddText(G.INDENT + "bgtz $v0, %s"%(instr.jmpTarget))
        elif instr.opType.is_GT():
            G.AsmText.AddText(G.INDENT + "bltz $v0, %s"%(instr.jmpTarget))
        return True
    return False

def Translate_ASSIGN(instr):
    if (not instr.opType.is_NONE()) and (not instr.inp2.is_NONE()):
        # dest = inp1 OP inp2

        reg1 = SetupRegister(instr.inp1,REG.tmpUsageRegs[0])
        if (instr.opType.is_DIV() or instr.opType.is_MULT() or instr.opType.is_MOD()):
            reg2 = SetupRegister(instr.inp2,REG.tmpUsageRegs[1])
        else:
            reg2 = SetupRegister(instr.inp2,REG.tmpUsageRegs[1], useImmediate=True)

        if instr.dest.is_SCALAR_VARIABLE():
            reg3 = SetupDestRegScalar(instr.dest, REG.tmpUsageRegs[-1])
            GenCode_3OPASSIGN(instr, reg3, reg1, reg2)
            if reg3 == REG.tmpUsageRegs[-1]:
                G.AsmText.AddText(G.INDENT + "sw %s, %s"%(reg3, ASM.GetVarAddr(instr.dest)), "Store it back")

        elif instr.dest.is_ARRAY_VARIABLE():
            tempReg = REG.tmpUsageRegs[-1]
            regComp = REG.tmpUsageRegs[2]

            SetupDestRegArray(instr.dest, regComp, tempReg)

            # We will reuse tempReg as the dest register. We will then write it back to the
            # address location in the array
            GenCode_3OPASSIGN(instr, tempReg, reg1, reg2)

            # Store back the value
            G.AsmText.AddText(G.INDENT + "sw %s, 0(%s)"%(tempReg, regComp), "Array is a dest. Storing back the value")

        elif instr.dest.is_HASH_VARIABLE():
            tempReg = REG.tmpUsageRegs[-1]
            regComp = REG.tmpUsageRegs[2]

            SetupDestRegHash(instr.dest, regComp, tempReg) # The value of key is stored in tempReg
            GenCode_3OPASSIGN(instr, regComp, reg1, reg2)

            LIB.Translate_alloc(reg1) # Hack for now. Everything has been dumped anyway
            G.AsmText.AddText(G.INDENT + "sw %s, 0(%s)"%(regComp, reg1), "Load value into allocated memory")

            LIB.Translate_addElement(instr.dest, tempReg, reg1) 

    elif instr.opType.is_NONE():
        # dest = inp1

        if instr.dest.is_SCALAR_VARIABLE():
            reg3 = SetupDestRegScalar(instr.dest, REG.tmpUsageRegs[-1])
            if instr.inp1.is_NUMBER():
                G.AsmText.AddText(G.INDENT + "li %s, %s"%(reg3, str(instr.inp1.value)))
            else:
                reg1 = SetupRegister(instr.inp1, REG.tmpUsageRegs[1])
                if reg1 != reg3:
                    G.AsmText.AddText(G.INDENT + "move %s, %s"%(reg3, reg1))

            if reg3 == REG.tmpUsageRegs[-1]:
                G.AsmText.AddText(G.INDENT + "sw %s, %s"%(reg3, ASM.GetVarAddr(instr.dest)), "Store it back")

        elif instr.dest.is_ARRAY_VARIABLE():
            tempReg = REG.tmpUsageRegs[-1]
            regComp = REG.tmpUsageRegs[2]

            SetupDestRegArray(instr.dest, regComp, tempReg)

            # We will reuse tempReg as the dest register. We will then write it back to the
            # address location in the array
            if instr.inp1.is_NUMBER():
                G.AsmText.AddText(G.INDENT + "li %s, %s"%(tempReg, str(instr.inp1.value)))
            else:
                reg1 = SetupRegister(instr.inp1, REG.tmpUsageRegs[0])
                G.AsmText.AddText(G.INDENT + "move %s, %s"%(tempReg, reg1))

            # Store back the value
            G.AsmText.AddText(G.INDENT + "sw %s, 0(%s)"%(tempReg, regComp))

        elif instr.dest.is_HASH_VARIABLE():
            tempReg = REG.tmpUsageRegs[-1]
            regComp = REG.tmpUsageRegs[2]

            SetupDestRegHash(instr.dest, regComp, tempReg) # The value of key is stored in tempReg

            # Store the value in regComp
            if instr.inp1.is_NUMBER():
                G.AsmText.AddText(G.INDENT + "li %s, %s"%(regComp, str(instr.inp1.value)))
            else:
                reg1 = SetupRegister(instr.inp1, REG.tmpUsageRegs[0])
                G.AsmText.AddText(G.INDENT + "move %s, %s"%(regComp, reg1))

            LIB.Translate_alloc(REG.tmpUsageRegs[0])
            G.AsmText.AddText(G.INDENT + "sw %s, 0(%s)"%(regComp, REG.tmpUsageRegs[0]), "Load value into allocated memory")

            LIB.Translate_addElement(instr.dest, tempReg, REG.tmpUsageRegs[0]) 

    elif instr.inp2.is_NONE():
        # dest = OP inp1
        reg1 = SetupRegister(instr.inp1,REG.tmpUsageRegs[0])

        if instr.dest.is_SCALAR_VARIABLE():
            reg3 = SetupDestRegScalar(instr.dest, REG.tmpUsageRegs[-1])
            GenCode_2OPASSIGN(instr, reg3, reg1)

            if reg3 == REG.tmpUsageRegs[-1]:
                G.AsmText.AddText(G.INDENT + "sw %s, %s"%(reg3, ASM.GetVarAddr(instr.dest)), "Store it back")

        elif instr.dest.is_ARRAY_VARIABLE():
            tempReg = REG.tmpUsageRegs[-1]
            regComp = REG.tmpUsageRegs[2]

            SetupDestRegArray(instr.dest, regComp, tempReg)

            # We will reuse tempReg as the dest register. We will then write it back to the
            # address location in the array
            GenCode_2OPASSIGN(instr, tempReg, reg1)

            # Store back the value
            G.AsmText.AddText(G.INDENT + "sw %s, 0(%s)"%(tempReg, regComp))

        elif instr.dest.is_HASH_VARIABLE():
            tempReg = REG.tmpUsageRegs[-1]
            regComp = REG.tmpUsageRegs[2]

            SetupDestRegHash(instr.dest, regComp, tempReg) # The value of key is stored in tempReg
            GenCode_2OPASSIGN(instr, regComp, reg1)

            LIB.Translate_alloc(REG.tmpUsageRegs[1])
            G.AsmText.AddText(G.INDENT + "sw %s, 0(%s)"%(regComp, REG.tmpUsageRegs[1]), "Load value into allocated memory")

            LIB.Translate_addElement(instr.dest, tempReg, REG.tmpUsageRegs[1])


def GenCode_3OPASSIGN(instr, regDest, regInp1, regInp2):
    # Currently ignoring overflows everywhere
    if instr.opType.is_PLUS():
        G.AsmText.AddText(G.INDENT + "addu %s, %s, %s"%(regDest, regInp1, regInp2),
                                     "%s = %s + %s"%(instr.dest, instr.inp1, instr.inp2))

    elif instr.opType.is_MINUS():
        G.AsmText.AddText(G.INDENT + "subu %s, %s, %s"%(regDest, regInp1, regInp2),
                                     "%s = %s - %s"%(instr.dest, instr.inp1, instr.inp2))

    elif instr.opType.is_MULT():
        G.AsmText.AddText(G.INDENT + "multu %s, %s"%(regInp1, regInp2))
        G.AsmText.AddText(G.INDENT + "mflo %s"%(regDest),
                                     "%s = %s * %s"%(instr.dest, instr.inp1, instr.inp2))

    elif instr.opType.is_DIV():
        G.AsmText.AddText(G.INDENT + "div %s, %s"%(regInp1, regInp2))
        G.AsmText.AddText(G.INDENT + "mflo %s"%(regDest),
                                     "%s = %s / %s"%(instr.dest, instr.inp1, instr.inp2))

    elif instr.opType.is_MOD():
        G.AsmText.AddText(G.INDENT + "div %s, %s"%(regInp1, regInp2))
        G.AsmText.AddText(G.INDENT + "mfhi %s"%(regDest),
                                     "%s = %s mod %s"%(instr.dest, instr.inp1, instr.inp2))

    elif instr.opType.is_LT():
        G.AsmText.AddText(G.INDENT + "slt %s, %s, %s"%(regDest, regInp1, regInp2),
                                     "%s = %s < %s"%(instr.dest, instr.inp1, instr.inp2))

    elif instr.opType.is_GT():
        G.AsmText.AddText(G.INDENT + "sgt %s, %s, %s"%(regDest, regInp1, regInp2),
                                     "%s = %s > %s"%(instr.dest, instr.inp1, instr.inp2))

    elif instr.opType.is_GEQ():
        G.AsmText.AddText(G.INDENT + "sge %s, %s, %s"%(regDest, regInp1, regInp2),
                                     "%s = %s >= %s"%(instr.dest, instr.inp1, instr.inp2))

    elif instr.opType.is_LEQ():
        G.AsmText.AddText(G.INDENT + "sle %s, %s, %s"%(regDest, regInp1, regInp2),
                                     "%s = %s <= %s"%(instr.dest, instr.inp1, instr.inp2))

    elif instr.opType.is_EQ():
        G.AsmText.AddText(G.INDENT + "seq %s, %s, %s"%(regDest, regInp1, regInp2),
                                     "%s = %s == %s"%(instr.dest, instr.inp1, instr.inp2))

    elif instr.opType.is_NE():
        G.AsmText.AddText(G.INDENT + "sne %s, %s, %s"%(regDest, regInp1, regInp2),
                                     "%s = %s != %s"%(instr.dest, instr.inp1, instr.inp2))

    elif instr.opType.is_BOR():
        G.AsmText.AddText(G.INDENT + "or %s, %s, %s"%(regDest, regInp1, regInp2),
                                     "%s = %s | %s"%(instr.dest, instr.inp1, instr.inp2))

    elif instr.opType.is_BAND():
        G.AsmText.AddText(G.INDENT + "and %s, %s, %s"%(regDest, regInp1, regInp2),
                                     "%s = %s & %s"%(instr.dest, instr.inp1, instr.inp2))

    elif instr.opType.is_BXOR():
        G.AsmText.AddText(G.INDENT + "xor %s, %s, %s"%(regDest, regInp1, regInp2),
                                     "%s = %s ^ %s"%(instr.dest, instr.inp1, instr.inp2))

    elif instr.opType.is_LSHIFT():
        G.AsmText.AddText(G.INDENT + "sllv %s, %s, %s"%(regDest, regInp1, regInp2),
                                     "%s = %s << %s"%(instr.dest, instr.inp1, instr.inp2))

    elif instr.opType.is_RSHIFT():
        G.AsmText.AddText(G.INDENT + "srlv %s, %s, %s"%(regDest, regInp1, regInp2),
                                     "%s = %s >> %s"%(instr.dest, instr.inp1, instr.inp2))

    else:
        raise Exception("%s : Instruction not recognized in 3OPAssign"%(instr))

def GenCode_2OPASSIGN(instr, regDest, regInp):
    # Ignoring Overflow in negation operation
    if instr.opType.is_BNOT():
        G.AsmText.AddText(G.INDENT + "not %s, %s"%(regDest, regInp),
                                     "%s = ~%s"%(instr.dest, instr.inp1))

    elif instr.opType.is_MINUS():
        G.AsmText.AddText(G.INDENT + "negu %s, %s"%(regDest, regInp),
                                     "%s = -%s"%(instr.dest, instr.inp1))
    elif instr.opType.is_PLUS():
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(regDest, regInp),
                                     "%s = +%s"%(instr.dest, instr.inp1))
    
    else:
        raise Exception("%s : Instruction not recognized in 2OPAssign"%(instr))

def GenCode_CallAssignment(instr):

    if instr.dest.is_SCALAR_VARIABLE():
        G.AsmText.AddText(G.INDENT + "sw %s, %s"%(REG.v0, ASM.GetVarAddr(instr.dest)), "Store function return directly into the memory address")

    elif instr.dest.is_ARRAY_VARIABLE():
        tempReg = REG.tmpUsageRegs[-1]
        regComp = REG.tmpUsageRegs[2]

        SetupDestRegArray(instr.dest, regComp, tempReg)

        # Store back the value
        G.AsmText.AddText(G.INDENT + "sw %s, 0(%s)"%(REG.v0, regComp), "Store function return directly into the memory address")

    elif instr.dest.is_HASH_VARIABLE():
        tempReg = REG.tmpUsageRegs[-1]
        regComp = REG.tmpUsageRegs[2]

        SetupDestRegHash(instr.dest, regComp, tempReg) # The value of key is stored in tempReg
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.tmpUsageRegs[1], REG.v0), "Store return value of function call so it is not overwritten by alloc")

        LIB.Translate_alloc(REG.tmpUsageRegs[0])
        G.AsmText.AddText(G.INDENT + "sw %s, 0(%s)"%(REG.tmpUsageRegs[1], REG.tmpUsageRegs[0]), "Load value into allocated memory")

        LIB.Translate_addElement(instr.dest, tempReg, REG.tmpUsageRegs[0]) 

def GenCode_Alloc(instr):

    if instr.dest.is_SCALAR_VARIABLE():
        LIB.Translate_alloc(REG.v0, instr.inp1)
        G.AsmText.AddText(G.INDENT + "sw %s, %s"%(REG.v0, ASM.GetVarAddr(instr.dest)), "Store function return directly into the memory address")

    elif instr.dest.is_ARRAY_VARIABLE():
        tempReg = REG.tmpUsageRegs[-1]
        regComp = REG.tmpUsageRegs[2]

        SetupDestRegArray(instr.dest, regComp, tempReg)

        LIB.Translate_alloc(REG.v0, instr.inp1)
        # Store back the value
        G.AsmText.AddText(G.INDENT + "sw %s, 0(%s)"%(REG.v0, regComp), "Store function return directly into the memory address")

    elif instr.dest.is_HASH_VARIABLE():
        tempReg = REG.tmpUsageRegs[-1]
        regComp = REG.tmpUsageRegs[2]

        SetupDestRegHash(instr.dest, regComp, tempReg) # The value of key is stored in tempReg

        LIB.Translate_alloc(REG.tmpUsageRegs[0])
        LIB.Translate_alloc(REG.v0, instr.inp1)
        G.AsmText.AddText(G.INDENT + "sw %s, 0(%s)"%(REG.v0, REG.tmpUsageRegs[0]), "Load value into allocated memory")

        LIB.Translate_addElement(instr.dest, tempReg, REG.tmpUsageRegs[0]) 

def SetupDestRegScalar(dest, tmpReg=REG.tmpUsageRegs[-1]):
    return SetupRegister(dest, tmpReg)


def SetupDestRegArray(dest, regComp, tempReg=REG.tmpUsageRegs[-1]):
    if dest.key.is_NUMBER():
        G.AsmText.AddText(tempReg.LoadImmediate(dest.key.value), "Load index for array access")
    else:
        regInp = SetupRegister(dest.key, regComp)
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(tempReg, regInp), "Load index for array access")

    # Load the array address in regComp
    G.AsmText.AddText(G.INDENT + "la %s, %s"%(regComp, ASM.GetArrAddr(dest.value)), "Load array address")

    # We move the index value to tempReg to multiply it by 4
    G.AsmText.AddText(G.INDENT + "sll %s, %s, 2"%(tempReg, tempReg), "Multiply index by 4")
    G.AsmText.AddText(G.INDENT + "add %s, %s, %s"%(regComp, regComp, tempReg), "Add index as an offset to array address")

def SetupDestRegHash(dest, regComp, tempReg=REG.tmpUsageRegs[-1]):
    if dest.key.is_NUMBER():
        G.AsmText.AddText(tempReg.LoadImmediate(dest.key.value), "Load key for the hash access")
    else:
        regInp = SetupRegister(dest.key, regComp)
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(tempReg, regInp), "Load key for the hash access")


