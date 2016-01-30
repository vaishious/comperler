"""

MODULE  : registers.py

Purpose : This file simply stores the instances of the MIPS register set.
          MIPS conventions are specified in the comments here.

Import Acronym : REG

"""

# List of Imports Begin
import mips_assembly as ASM
# List of Imports End

# Constant Value Zero
zero = ASM.Register("zero")

# These registers contain the Returned Value of a subroutine
# If the value is 1 word only $v0 is significant.
# Compilers also use these as temporary registers for transferring/loading immediate values

v0   = ASM.Register("v0")
v1   = ASM.Register("v1")

# Assembler Temporary used by the assembler in expanding pseudo-ops
# Don't use though.

at   = ASM.Register("at")

# Argument registers - Contain the first 4 argument values for a subroutine call

a0   = ASM.Register("a0")
a1   = ASM.Register("a1")
a2   = ASM.Register("a2")
a3   = ASM.Register("a3")

# Caller saved temporaries. Caller can assume their values to be destroyed upon return from a call
# It is the responsibility of the caller to save their values if it wants to reuse them

t0   = ASM.Register("t0")
t1   = ASM.Register("t1")
t2   = ASM.Register("t2")
t3   = ASM.Register("t3")
t4   = ASM.Register("t4")
t5   = ASM.Register("t5")
t6   = ASM.Register("t6")
t7   = ASM.Register("t7")
t8   = ASM.Register("t8")
t9   = ASM.Register("t9")

# Callee saved registers. Caller can assume their values to be intact upon return from a call
# It is the responsibility of the callee to save their values

s0   = ASM.Register("s0")
s1   = ASM.Register("s1")
s2   = ASM.Register("s2")
s3   = ASM.Register("s3")
s4   = ASM.Register("s4")
s5   = ASM.Register("s5")
s6   = ASM.Register("s6")
s7   = ASM.Register("s7")

# Kernel Reserved ASM.Registers. Not supposed to use them though

k0   = ASM.Register("k0")
k1   = ASM.Register("k1")

# Global Pointer

gp   = ASM.Register("gp")

# Stack Pointer

sp   = ASM.Register("sp")

# Frame Pointer. Not using this explicitly can allow us to use this as another saved register.
# Not recommended though

fp   = ASM.Register("fp")

# Return address in a subroutine call

ra   = ASM.Register("ra")

# Group argument registers together for easy access

argRegs = [a0, a1, a2, a3]

# Group caller saved registers together

tmpRegs = [t0, t1, t2, t3, t4, t5, t6, t7, t8, t9]

# Group callee saved registers together

savedRegs = [s0, s1, s2, s3, s4, s5, s6, s7]
