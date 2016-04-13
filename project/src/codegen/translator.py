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
        if instr.declType == 'hash':
            G.CurrRegAddrTable.DumpDirtyVars()
            G.CurrRegAddrTable.Reset()
            G.AllocMap = {}
            LIB.Translate_initHash(instr.inp1)

        elif instr.declType == 'array':
            G.CurrRegAddrTable.DumpDirtyVars()
            G.CurrRegAddrTable.Reset()
            G.AllocMap = {}
            LIB.Translate_initArray(instr.inp1)

    elif instr.instrType.is_EXIT():
        G.CurrRegAddrTable.DumpDirtyVars()
        G.AsmText.AddText(G.INDENT + "li %s, 10"%(REG.v0))
        G.AsmText.AddText(G.INDENT + "syscall")

    elif instr.instrType.is_GOTO():
        G.CurrRegAddrTable.DumpDirtyVars()
        G.AsmText.AddText(G.INDENT + "j %s"%(instr.jmpTarget))

    elif instr.instrType.is_TYPECALL():
        if instr.dest.is_ARRAY_OR_HASH():
            G.CurrRegAddrTable.DumpDirtyVars()
            G.CurrRegAddrTable.Reset()
            G.AllocMap = {}

        GenCode_TypeCallAssignment(instr)

    elif instr.instrType.is_CALL():
        G.CurrRegAddrTable.DumpDirtyVars()
        if instr.inp1.is_VARIABLE():
            reg = SetupRegister(instr.inp1, REG.a0)
            if reg != REG.a0:
                G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.a0, reg))

        G.AsmText.AddText(G.INDENT + "jal %s"%(instr.jmpLabel))
        if instr.inp1.is_VARIABLE():
            G.AsmText.AddText(G.INDENT + "lw %s, 16($fp)"%(REG.a0))

        if instr.dest.is_VARIABLE():
            GenCode_CallAssignment(instr)

    elif instr.instrType.is_PRINT():
        if instr.ContainsHashAccess():
            G.CurrRegAddrTable.DumpDirtyVars()
        LIB.Translate_Printf(instr.inp1)

    elif instr.instrType.is_READ():
        if instr.ContainsHashAccess():
            G.CurrRegAddrTable.DumpDirtyVars()
        LIB.Translate_Scanf(instr.IOArgs)

    elif instr.instrType.is_ALLOC():
        if instr.ContainsHashAccess():
            G.CurrRegAddrTable.DumpDirtyVars()
        GenCode_Alloc(instr)

    elif instr.instrType.is_TYPERETURN():
        reg = SetupRegister(instr.inp1, REG.v1)
        if reg != REG.v1:
            G.AsmText.AddText(G.INDENT + "move %s, %s\n"%(REG.v1, reg), "Storing type of return value in $v1")

    elif instr.instrType.is_RETURN():
        if not instr.inp1.is_NONE():
            reg = SetupRegister(instr.inp1, REG.v0)
            if reg != REG.v0:
                G.AsmText.AddText(G.INDENT + "move %s, %s\n"%(REG.v0, reg), "Storing return value in $v0")

        G.CurrRegAddrTable.DumpDirtyVars()
        stackSpaceRequired = G.StackSpaceMap[G.CurrFunction]
        G.AsmText.AddText(G.INDENT + "move $sp, $fp", "Restore the stack pointer")
        G.AsmText.AddText(G.INDENT + "lw $fp, %d($sp)"%(stackSpaceRequired-4), "Reload the fp from previous call")
        G.AsmText.AddText(G.INDENT + "lw $ra, %d($sp)"%(stackSpaceRequired-8), "Reload the ra of current call")
        G.AsmText.AddText(G.INDENT + "jr $ra")

    elif instr.instrType.is_IFGOTO():
        # We can safely clobber registers here because this is the last
        # instruction of the basic block
        if (instr.dest.is_ARRAY_OR_HASH() or 
            instr.inp1.is_ARRAY_OR_HASH() or
            instr.inp2.is_ARRAY_OR_HASH() or
            instr.opType.is_STRING_OP()):

            G.CurrRegAddrTable.DumpDirtyVars()
            G.CurrRegAddrTable.Reset()
            G.AllocMap = {}

        G.CurrRegAddrTable.DumpDirtyVars()
        Translate_IFGOTO(instr)

    elif instr.instrType.is_ASSIGN():
        #if (instr.dest.is_ARRAY_OR_HASH() or 
            #instr.inp1.is_ARRAY_OR_HASH() or
            #instr.inp2.is_ARRAY_OR_HASH()):

        G.CurrRegAddrTable.DumpDirtyVars()
        G.CurrRegAddrTable.Reset()
        G.AllocMap = {}

        Translate_ASSIGN(instr)

    elif instr.instrType.is_TYPECHECK():
        G.CurrRegAddrTable.DumpDirtyVars()
        G.CurrRegAddrTable.Reset()
        G.AllocMap = {}

        Translate_TYPECHECK(instr)

    elif instr.instrType.is_TYPEASSIGN():
        if (instr.dest.is_ARRAY_OR_HASH() or 
            instr.inp1.is_ARRAY_OR_HASH() or
            instr.inp2.is_ARRAY_OR_HASH()):

            G.CurrRegAddrTable.DumpDirtyVars()
            G.CurrRegAddrTable.Reset()
            G.AllocMap = {}

        Translate_TYPEASSIGN(instr)

    elif instr.instrType.is_TYPECHECKASSIGN():
        G.CurrRegAddrTable.DumpDirtyVars()
        G.CurrRegAddrTable.Reset()
        G.AllocMap = {}

        Translate_TYPECHECKASSIGN(instr)

    elif instr.instrType.is_LINENUM():
        G.AsmText.AddText(G.INDENT + "li %s, %s"%(REG.tmpUsageRegs[-1], instr.inp1), "Update Prog Line Number")
        G.AsmText.AddText(G.INDENT + "sw %s, %s"%(REG.tmpUsageRegs[-1], "LINENUM"), "Update Prog Line Number")

def SetupRegister(inp, regComp, tempReg=REG.t9, useImmediate=False, loadTypeVal=False):
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

        if loadTypeVal:
            LIB.Translate_getArrayValueType(inp, tempReg, regComp)
        else:
            LIB.Translate_getArrayValue(inp, tempReg, regComp)

        reg = regComp

    elif inp.is_HASH_VARIABLE():
        # First we need the key
        regInp = None
        if inp.key.is_NUMBER():
            G.AsmText.AddText(tempReg.LoadImmediate(inp.key.value), "Load key for the hash access")
        else:
            regInp = SetupRegister(inp.key, regComp)
            G.AsmText.AddText(G.INDENT + "move %s, %s"%(tempReg, regInp), "Load key for the hash access")

        if loadTypeVal:
            LIB.Translate_getHashValueType(inp, tempReg, regComp) 
        else:
            LIB.Translate_getHashValue(inp, tempReg, regComp) 

        reg = regComp

    DEBUG.Assert(reg, "Line %d: Unable to setup register for %s."%(G.CurrInstruction.lineID, str(inp.value)))
    return reg

def Translate_IFGOTO(instr):

    # Instead of separately handling the cases in which one or both of
    # the operands is a number, load both operands into registers and 
    # operate only on the registers.
    reg1 = SetupRegister(instr.inp1, REG.tmpUsageRegs[0])
    if instr.opType.is_STRING_OP():
        reg2 = SetupRegister(instr.inp2, REG.tmpUsageRegs[1])
    else:
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

    elif (instr.opType.is_STRLT() or
          instr.opType.is_STRLE() or
          instr.opType.is_STRGT() or
          instr.opType.is_STRGE() or
          instr.opType.is_STREQ() or
          instr.opType.is_STRNE()):

        G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.a0, reg1))
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.a1, reg2))
        G.AsmText.AddText(G.INDENT + "lw %s, OPCONTROL"%(REG.a2))
        G.AsmText.AddText(G.INDENT + "jalr %s"%(REG.a2))
        G.AsmText.AddText(G.INDENT + "lw %s, 16($sp)"%(REG.a0))

        if instr.opType.is_STRLT():
            G.AsmText.AddText(G.INDENT + "li %s, -1"%(REG.tmpUsageRegs[-1]))
            G.AsmText.AddText(G.INDENT + "beq %s, %s, %s"%(REG.v0, REG.tmpUsageRegs[-1], instr.jmpTarget))
        elif instr.opType.is_STRGT():
            G.AsmText.AddText(G.INDENT + "li %s, 1"%(REG.tmpUsageRegs[-1]))
            G.AsmText.AddText(G.INDENT + "beq %s, %s, %s"%(REG.v0, REG.tmpUsageRegs[-1], instr.jmpTarget))
        elif instr.opType.is_STRLE():
            G.AsmText.AddText(G.INDENT + "blez %s, %s"%(REG.v0, instr.jmpTarget))
        elif instr.opType.is_STRGE():
            G.AsmText.AddText(G.INDENT + "bgez %s, %s"%(REG.v0, instr.jmpTarget))
        elif instr.opType.is_STREQ():
            G.AsmText.AddText(G.INDENT + "beq %s, $0, %s"%(REG.v0, instr.jmpTarget))
        elif instr.opType.is_STRNE():
            G.AsmText.AddText(G.INDENT + "bne %s, $0, %s"%(REG.v0, instr.jmpTarget))

def Translate_ASSIGN(instr):
    if (not instr.opType.is_NONE()) and (not instr.inp2.is_NONE()):
        # dest = inp1 OP inp2

        reg1 = SetupRegister(instr.inp1,REG.tmpUsageRegs[0])
        if (instr.opType.is_DIV() or 
            instr.opType.is_MULT() or 
            instr.opType.is_MOD() or 
            instr.opType.is_PLUS() or 
            instr.opType.is_MINUS() or
            instr.opType.is_DOT() or
            instr.opType.is_REPEAT()):
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

            G.AsmText.AddText(G.INDENT + "move %s, %s"%(reg1, regComp), "Load hash value")

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

            G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.tmpUsageRegs[0], regComp), "Load hash value")

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

            G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.tmpUsageRegs[1], regComp), "Load value into allocated memory")

            LIB.Translate_addElement(instr.dest, tempReg, REG.tmpUsageRegs[1])


def GenCode_3OPASSIGN(instr, regDest, regInp1, regInp2):
    # Currently ignoring overflows everywhere
    if instr.opType.is_PLUS():
        #G.AsmText.AddText(G.INDENT + "addu %s, %s, %s"%(regDest, regInp1, regInp2),
                                     #"%s = %s + %s"%(instr.dest, instr.inp1, instr.inp2))
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.a0, regInp1))
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.a1, regInp2))
        G.AsmText.AddText(G.INDENT + "lw %s, OPCONTROL"%(REG.a2))
        G.AsmText.AddText(G.INDENT + "jalr %s"%(REG.a2))
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(regDest, REG.v0))
        G.AsmText.AddText(G.INDENT + "lw %s, 16($fp)"%(REG.a0))

    elif instr.opType.is_MINUS():
        #G.AsmText.AddText(G.INDENT + "subu %s, %s, %s"%(regDest, regInp1, regInp2),
                                     #"%s = %s - %s"%(instr.dest, instr.inp1, instr.inp2))
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.a0, regInp1))
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.a1, regInp2))
        G.AsmText.AddText(G.INDENT + "lw %s, OPCONTROL"%(REG.a2))
        G.AsmText.AddText(G.INDENT + "jalr %s"%(REG.a2))
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(regDest, REG.v0))
        G.AsmText.AddText(G.INDENT + "lw %s, 16($fp)"%(REG.a0))

    elif instr.opType.is_MULT():
        #G.AsmText.AddText(G.INDENT + "multu %s, %s"%(regInp1, regInp2))
        #G.AsmText.AddText(G.INDENT + "mflo %s"%(regDest),
                                     #"%s = %s * %s"%(instr.dest, instr.inp1, instr.inp2))

        G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.a0, regInp1))
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.a1, regInp2))
        G.AsmText.AddText(G.INDENT + "lw %s, OPCONTROL"%(REG.a2))
        G.AsmText.AddText(G.INDENT + "jalr %s"%(REG.a2))
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(regDest, REG.v0))
        G.AsmText.AddText(G.INDENT + "lw %s, 16($fp)"%(REG.a0))

    elif instr.opType.is_DIV():
        #G.AsmText.AddText(G.INDENT + "div %s, %s"%(regInp1, regInp2))
        #G.AsmText.AddText(G.INDENT + "mflo %s"%(regDest),
                                     #"%s = %s / %s"%(instr.dest, instr.inp1, instr.inp2))


        G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.a0, regInp1))
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.a1, regInp2))
        G.AsmText.AddText(G.INDENT + "lw %s, OPCONTROL"%(REG.a2))
        G.AsmText.AddText(G.INDENT + "jalr %s"%(REG.a2))
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(regDest, REG.v0))
        G.AsmText.AddText(G.INDENT + "lw %s, 16($fp)"%(REG.a0))

    elif instr.opType.is_MOD():
        #G.AsmText.AddText(G.INDENT + "div %s, %s"%(regInp1, regInp2))
        #G.AsmText.AddText(G.INDENT + "mfhi %s"%(regDest),
                                     #"%s = %s mod %s"%(instr.dest, instr.inp1, instr.inp2))


        G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.a0, regInp1))
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.a1, regInp2))
        G.AsmText.AddText(G.INDENT + "lw %s, OPCONTROL"%(REG.a2))
        G.AsmText.AddText(G.INDENT + "jalr %s"%(REG.a2))
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(regDest, REG.v0))
        G.AsmText.AddText(G.INDENT + "lw %s, 16($fp)"%(REG.a0))

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

    elif instr.opType.is_DOT():
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.a0, regInp1))
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.a1, regInp2))
        G.AsmText.AddText(G.INDENT + "lw %s, OPCONTROL"%(REG.a2))
        G.AsmText.AddText(G.INDENT + "jalr %s"%(REG.a2))
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(regDest, REG.v0))
        G.AsmText.AddText(G.INDENT + "lw %s, 16($fp)"%(REG.a0))

    elif instr.opType.is_REPEAT():
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.a0, regInp1))
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.a1, regInp2))
        G.AsmText.AddText(G.INDENT + "lw %s, OPCONTROL"%(REG.a2))
        G.AsmText.AddText(G.INDENT + "jalr %s"%(REG.a2))
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(regDest, REG.v0))
        G.AsmText.AddText(G.INDENT + "lw %s, 16($fp)"%(REG.a0))

    else:
        raise Exception("%s : Instruction not recognized in 3OPAssign"%(instr))

def GenCode_2OPASSIGN(instr, regDest, regInp):
    # Ignoring Overflow in negation operation
    if instr.opType.is_BNOT():
        G.AsmText.AddText(G.INDENT + "not %s, %s"%(regDest, regInp),
                                     "%s = ~%s"%(instr.dest, instr.inp1))

    elif instr.opType.is_MINUS():
        #G.AsmText.AddText(G.INDENT + "negu %s, %s"%(regDest, regInp),
                                     #"%s = -%s"%(instr.dest, instr.inp1))
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.a0, regInp))
        G.AsmText.AddText(G.INDENT + "lw %s, OPCONTROL"%(REG.a2))
        G.AsmText.AddText(G.INDENT + "jalr %s"%(REG.a2))
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(regDest, REG.v0))
        G.AsmText.AddText(G.INDENT + "lw %s, 16($fp)"%(REG.a0))

    elif instr.opType.is_PLUS():
        #G.AsmText.AddText(G.INDENT + "move %s, %s"%(regDest, regInp),
                                     #"%s = +%s"%(instr.dest, instr.inp1))
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.a0, regInp))
        G.AsmText.AddText(G.INDENT + "lw %s, OPCONTROL"%(REG.a2))
        G.AsmText.AddText(G.INDENT + "jalr %s"%(REG.a2))
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(regDest, REG.v0))
        G.AsmText.AddText(G.INDENT + "lw %s, 16($fp)"%(REG.a0))

    elif instr.opType.is_REFERENCE():
        G.AsmText.AddText(G.INDENT + "la %s, %s"%(regDest, ASM.GetVarAddr(instr.inp1)),
                                     "%s = \\%s"%(instr.dest, instr.inp1))
 
    elif instr.opType.is_DEREFERENCE():
        G.AsmText.AddText(G.INDENT + "lw %s, 0(%s)"%(regDest, regInp),
                                     "%s = $%s"%(instr.dest, instr.inp1))   
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

        G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.tmpUsageRegs[0], REG.tmpUsageRegs[1]), "Load value into allocated memory")

        LIB.Translate_addElement(instr.dest, tempReg, REG.tmpUsageRegs[0]) 

def GenCode_TypeCallAssignment(instr):

    if instr.dest.is_SCALAR_VARIABLE():
        reg1 = SetupDestRegScalar(instr.dest)
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(reg1, REG.v1), "Store function return type")

    elif instr.dest.is_ARRAY_VARIABLE():
        tempReg = REG.tmpUsageRegs[-1]
        regComp = REG.tmpUsageRegs[2]

        SetupDestRegArray(instr.dest, regComp, tempReg, loadTypeVal=True)

        # Store back the value
        G.AsmText.AddText(G.INDENT + "sw %s, 0(%s)"%(REG.v1, regComp), "Store function return type directly into the memory address")

    elif instr.dest.is_HASH_VARIABLE():
        tempReg = REG.tmpUsageRegs[-1]
        regComp = REG.tmpUsageRegs[2]

        SetupDestRegHash(instr.dest, regComp, tempReg) # The value of key is stored in tempReg

        G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.tmpUsageRegs[0], REG.v1), "Load return type into hash value")

        LIB.Translate_addElementType(instr.dest, tempReg, REG.tmpUsageRegs[0]) 

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


def SetupDestRegArray(dest, regComp, tempReg=REG.tmpUsageRegs[-1], loadTypeVal=False):
    if dest.key.is_NUMBER():
        G.AsmText.AddText(tempReg.LoadImmediate(dest.key.value), "Load index for array access")
    else:
        regInp = SetupRegister(dest.key, regComp)
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(tempReg, regInp), "Load index for array access")

    if loadTypeVal:
        LIB.Translate_getArrayIndexAddressType(dest, tempReg, regComp)
    else:
        LIB.Translate_getArrayIndexAddress(dest, tempReg, regComp)

def SetupDestRegHash(dest, regComp, tempReg=REG.tmpUsageRegs[-1]):
    if dest.key.is_NUMBER():
        G.AsmText.AddText(tempReg.LoadImmediate(dest.key.value), "Load key for the hash access")
    else:
        regInp = SetupRegister(dest.key, regComp)
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(tempReg, regInp), "Load key for the hash access")


def Translate_TYPECHECKASSIGN(instr):
    tempReg = REG.tmpUsageRegs[-1]
    regComp = REG.tmpUsageRegs[2]

    reg1 = SetupRegister(instr.inp1, REG.tmpUsageRegs[0], loadTypeVal=True)
    reg2 = SetupRegister(instr.inp2, REG.tmpUsageRegs[1], loadTypeVal=True)

    if instr.dest.is_SCALAR_VARIABLE():
        reg = SetupDestRegScalar(instr.dest, tempReg)
        Translate_TYPECHECK(instr)
        if reg == tempReg:
            G.AsmText.AddText(G.INDENT + "sw %s, %s"%(REG.v0, ASM.GetVarAddr(instr.dest)))
        else:
            G.AsmText.AddText(G.INDENT + "move %s, %s"%(reg, REG.v0))

    elif instr.dest.is_ARRAY_VARIABLE():
        SetupDestRegArray(instr.dest, regComp, tempReg, loadTypeVal=True)
        Translate_TYPECHECK(instr)
        G.AsmText.AddText(G.INDENT + "sw %s, 0(%s)"%(REG.v0, regComp))

    elif instr.dest.is_HASH_VARIABLE():
        SetupDestRegHash(instr.dest, regComp, tempReg) # Key is stored in tempReg
        Translate_TYPECHECK(instr)
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(regComp, REG.v0))
        LIB.Translate_addElementType(instr.dest, tempReg, regComp)

def Translate_TYPEASSIGN(instr):
    tempReg = REG.tmpUsageRegs[-1]
    regComp = REG.tmpUsageRegs[2]
    if instr.opType.is_NONE():
        reg1 = SetupRegister(instr.inp1, REG.tmpUsageRegs[0], loadTypeVal=True)

    elif instr.opType.is_REFERENCE():
        reg1 = REG.tmpUsageRegs[0]
        if instr.inp1.is_SCALAR_VARIABLE():
            G.AsmText.AddText(G.INDENT + "la %s, %s"%(reg1, ASM.GetVarAddr(instr.inp1)))
        elif instr.inp1.is_ARRAY_VARIABLE():
            SetupDestRegArray(instr.inp1, reg1, tempReg, loadTypeVal=True)

    elif instr.opType.is_DEREFERENCE():
        reg1 = SetupRegister(instr.inp1, REG.tmpUsageRegs[0], loadTypeVal=True)
        G.AsmText.AddText(G.INDENT + "lw %s, 0(%s)"%(reg1, reg1))

    if instr.dest.is_SCALAR_VARIABLE():
        reg = SetupDestRegScalar(instr.dest, tempReg)
        if reg == tempReg:
            G.AsmText.AddText(G.INDENT + "sw %s, %s"%(reg1, ASM.GetVarAddr(instr.dest)), "Store it back")
        else:
            G.AsmText.AddText(G.INDENT + "move %s, %s"%(reg, reg1))

    elif instr.dest.is_ARRAY_VARIABLE():
        SetupDestRegArray(instr.dest, regComp, tempReg, loadTypeVal=True)
        G.AsmText.AddText(G.INDENT + "sw %s, 0(%s)"%(reg1, regComp))

    elif instr.dest.is_HASH_VARIABLE():
        SetupDestRegHash(instr.dest, regComp, tempReg) # Key is stored in tempReg
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(regComp, reg1))
        LIB.Translate_addElementType(instr.dest, tempReg, regComp)

def Translate_TYPECHECK(instr):
    tempReg = REG.tmpUsageRegs[-1]
    regComp = REG.tmpUsageRegs[2]

    reg1 = SetupRegister(instr.inp1, REG.tmpUsageRegs[0], loadTypeVal=True)
    if instr.inp2.is_NONE():
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.a0, reg1))
        if instr.opType.is_HASH_INDEX_CHECK() : 
            G.AsmText.AddText(G.INDENT + "jal typecheck_HASH_INDEX_CHECK")
        elif instr.opType.is_ARRAY_INDEX_CHECK(): 
            G.AsmText.AddText(G.INDENT + "jal typecheck_ARRAY_INDEX_CHECK")
        elif instr.opType.is_PLUS():
            G.AsmText.AddText(G.INDENT + "jal typecheck_UNARY_INT_PLUS")
        elif instr.opType.is_MINUS():
            G.AsmText.AddText(G.INDENT + "jal typecheck_UNARY_INT_MINUS")
        else:
            raise Exception("%s : Instruction not recognized in Translate_TYPECHECK"%(instr))
            
        G.AsmText.AddText(G.INDENT + "lw %s, 16($fp)"%(REG.a0))

    else:
        reg2 = SetupRegister(instr.inp2, REG.tmpUsageRegs[1], loadTypeVal=True)
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.a0, reg1))
        G.AsmText.AddText(G.INDENT + "move %s, %s"%(REG.a1, reg2))
        if instr.opType.is_PLUS():
            G.AsmText.AddText(G.INDENT + "jal typecheck_INT_PLUS")

        elif instr.opType.is_TYPE_EQUAL():
            G.AsmText.AddText(G.INDENT + "jal typecheck_TYPE_EQUAL")

        elif instr.opType.is_MINUS():
            G.AsmText.AddText(G.INDENT + "jal typecheck_INT_MINUS")

        elif instr.opType.is_MULT():
            G.AsmText.AddText(G.INDENT + "jal typecheck_INT_MULT")

        elif instr.opType.is_DIV():
            G.AsmText.AddText(G.INDENT + "jal typecheck_INT_DIV")

        elif instr.opType.is_MOD():
            G.AsmText.AddText(G.INDENT + "jal typecheck_INT_MOD")

        elif instr.opType.is_LT():
            G.AsmText.AddText(G.INDENT + "jal typecheck_GENERIC_INT_3OP")

        elif instr.opType.is_GT():
            G.AsmText.AddText(G.INDENT + "jal typecheck_GENERIC_INT_3OP")

        elif instr.opType.is_GEQ():
            G.AsmText.AddText(G.INDENT + "jal typecheck_GENERIC_INT_3OP")

        elif instr.opType.is_LEQ():
            G.AsmText.AddText(G.INDENT + "jal typecheck_GENERIC_INT_3OP")

        elif instr.opType.is_EQ():
            G.AsmText.AddText(G.INDENT + "jal typecheck_GENERIC_INT_3OP")

        elif instr.opType.is_NE():
            G.AsmText.AddText(G.INDENT + "jal typecheck_GENERIC_INT_3OP")

        elif instr.opType.is_BOR():
            G.AsmText.AddText(G.INDENT + "jal typecheck_GENERIC_INT_3OP")

        elif instr.opType.is_BAND():
            G.AsmText.AddText(G.INDENT + "jal typecheck_GENERIC_INT_3OP")

        elif instr.opType.is_BXOR():
            G.AsmText.AddText(G.INDENT + "jal typecheck_GENERIC_INT_3OP")

        elif instr.opType.is_LSHIFT():
            G.AsmText.AddText(G.INDENT + "jal typecheck_GENERIC_INT_3OP")

        elif instr.opType.is_RSHIFT():
            G.AsmText.AddText(G.INDENT + "jal typecheck_GENERIC_INT_3OP")

        elif instr.opType.is_STRLT():
            G.AsmText.AddText(G.INDENT + "jal typecheck_STRING_RELOP")

        elif instr.opType.is_STRGT():
            G.AsmText.AddText(G.INDENT + "jal typecheck_STRING_RELOP")

        elif instr.opType.is_STRLE():
            G.AsmText.AddText(G.INDENT + "jal typecheck_STRING_RELOP")

        elif instr.opType.is_STRGE():
            G.AsmText.AddText(G.INDENT + "jal typecheck_STRING_RELOP")

        elif instr.opType.is_STREQ():
            G.AsmText.AddText(G.INDENT + "jal typecheck_STRING_RELOP")

        elif instr.opType.is_STRNE():
            G.AsmText.AddText(G.INDENT + "jal typecheck_STRING_RELOP")

        elif instr.opType.is_DOT():
            G.AsmText.AddText(G.INDENT + "jal typecheck_STRING_DOT")

        elif instr.opType.is_REPEAT():
            G.AsmText.AddText(G.INDENT + "jal typecheck_STRING_REPEAT")

        else:
            raise Exception("%s : Instruction not recognized in Translate_TYPECHECK"%(instr))

        G.AsmText.AddText(G.INDENT + "lw %s, 16($fp)"%(REG.a0))

