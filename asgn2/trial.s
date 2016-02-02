 ### GENERATED MIPS ASSEMBLY - COMPERLER ###
 ### FILENAME : test/test5.ir ###

.data
# VARIABLES
.align 2
$V_a : .word 0


# ARRAYS

# STRINGS
.align 2
$STR_0 : .asciiz "%d"
.align 2
$STR_1 : .asciiz "KEY ERROR: Match not found\n"

# HASHES
.align 2
$H_h : .word 0


.text
main:

    # BASIC BLOCK #0

    # INSTR : declare h{0}
    li $a0, 0                  # Passing the type of hash
    jal initHash               # Allocating memory and initializing the hash
    sw $v0, $H_h               # Storing the returned memory address of hash

    # INSTR : h{3} = 2
    li $t9, 3                  # Load key for the hash access
    li $t8, 2
    li $a0, 4                  # Load memory size to be allocated
    jal alloc                  #  call malloc
    move $t6, $v0              # Load returned pointer into targetReg
    sw $t8, 0($t6)             # Load key into allocated memory
    la $a0, $H_h
    move $a2, $t9              # Load key
    la $a3, 0($t6)             # Load value
    jal addElement             # Add element to the hash

    # INSTR : h{3} = 1 + h{3}
    li $t6, 1
    li $t9, 3                  # Load key for the hash access
    la $a0, $H_h
    move $a2, $t9              # Load key
    la $a3, $STR_1
    jal getValue               # Searching for value in hash
    lw $t7, 0($v0)             # Store result back into a designated register
    li $t9, 3                  # Load key for the hash access
    addu $t8, $t6, $t7
    li $a0, 4                  # Load memory size to be allocated
    jal alloc                  #  call malloc
    move $t6, $v0              # Load returned pointer into targetReg
    sw $t8, 0($t6)             # Load key into allocated memory
    la $a0, $H_h
    move $a2, $t9              # Load key
    la $a3, 0($t6)             # Load value
    jal addElement             # Add element to the hash

    # INSTR : a = h{3}
    sw $t3, $V_a

    lw $t9, $V_a
    li $t9, 3                  # Load key for the hash access
    la $a0, $H_h
    move $a2, $t9              # Load key
    la $a3, $STR_1
    jal getValue               # Searching for value in hash
    lw $t7, 0($v0)             # Store result back into a designated register
    move $t9, $t7

    sw $t3, $V_a

    # INSTR : Print ['"%d"', 'a']
    la $a0, $STR_0
    lw $a1, $V_a
    jal Printf


    # BASIC BLOCK #1

    # INSTR : exit
    li $v0, 10
    syscall

PrintInt:
	.frame	$fp,8,$31		# vars= 0, regs= 1/0, args= 0, extra= 0
	.mask	0x40000000,-8
	.fmask	0x00000000,0
	subu	$sp,$sp,8
	sw	$fp,0($sp)
	move	$fp,$sp
	sw	$4,8($fp)
	lw	$2,8($fp)
 #APP
	
            move $a0, $2
            li   $v0, 1
            syscall
        
 #NO_APP
	move	$sp,$fp
	lw	$fp,0($sp)
	addu	$sp,$sp,8
	j	$31
	.end	PrintInt

alloc:
	.frame	$fp,16,$31		# vars= 8, regs= 1/0, args= 0, extra= 0
	.mask	0x40000000,-8
	.fmask	0x00000000,0
	subu	$sp,$sp,16
	sw	$fp,8($sp)
	move	$fp,$sp
	sw	$4,16($fp)
	lw	$2,16($fp)
 #APP
		
            move $a0, $2
            li $v0,9
            syscall
            sw $v0, 0($fp)
        
 #NO_APP
	lw	$2,0($fp)
	move	$sp,$fp
	lw	$fp,8($sp)
	addu	$sp,$sp,16
	j	$31
	.end	alloc

ExitWithMessage:
	.frame	$fp,24,$31		# vars= 0, regs= 2/0, args= 16, extra= 0
	.mask	0xc0000000,-4
	.fmask	0x00000000,0
	subu	$sp,$sp,24
	sw	$31,20($sp)
	sw	$fp,16($sp)
	move	$fp,$sp
	sw	$4,24($fp)
	sw	$5,28($fp)
	lw	$2,28($fp)
	beq	$2,$0,$LExitWithMessage3
	lw	$4,24($fp)
	jal	PrintString
	lw	$4,28($fp)
	jal	PrintString
	j	$LExitWithMessage4
$LExitWithMessage3:
	lw	$4,24($fp)
	jal	PrintString
$LExitWithMessage4:
 #APP
	
            li $v0, 10
            syscall
        
 #NO_APP
	move	$sp,$fp
	lw	$31,20($sp)
	lw	$fp,16($sp)
	addu	$sp,$sp,24
	j	$31
	.end	ExitWithMessage

initHash:
	.frame	$fp,32,$31		# vars= 8, regs= 2/0, args= 16, extra= 0
	.mask	0xc0000000,-4
	.fmask	0x00000000,0
	subu	$sp,$sp,32
	sw	$31,28($sp)
	sw	$fp,24($sp)
	move	$fp,$sp
	sw	$4,32($fp)
	li	$4,16			# 0x10
	jal	alloc
	sw	$2,16($fp)
	lw	$3,16($fp)
	lw	$2,16($fp)
	sw	$0,4($2)
	sw	$0,0($3)
	lw	$2,16($fp)
	sw	$0,8($2)
	lw	$3,16($fp)
	lw	$2,32($fp)
	sw	$2,12($3)
	lw	$2,16($fp)
	move	$sp,$fp
	lw	$31,28($sp)
	lw	$fp,24($sp)
	addu	$sp,$sp,32
	j	$31
	.end	initHash

PrintChar:
	.frame	$fp,16,$31		# vars= 8, regs= 1/0, args= 0, extra= 0
	.mask	0x40000000,-8
	.fmask	0x00000000,0
	subu	$sp,$sp,16
	sw	$fp,8($sp)
	move	$fp,$sp
	move	$2,$4
	sb	$2,0($fp)
	lbu	$2,0($fp)
 #APP
	
            move $a0, $2
            li   $v0, 11
            syscall
        
 #NO_APP
	move	$sp,$fp
	lw	$fp,8($sp)
	addu	$sp,$sp,16
	j	$31
	.end	PrintChar

findMatch:
	.frame	$fp,32,$31		# vars= 8, regs= 2/0, args= 16, extra= 0
	.mask	0xc0000000,-4
	.fmask	0x00000000,0
	subu	$sp,$sp,32
	sw	$31,28($sp)
	sw	$fp,24($sp)
	move	$fp,$sp
	sw	$4,32($fp)
	sw	$5,36($fp)
	sw	$6,40($fp)
	lw	$2,32($fp)
	lw	$2,0($2)
	sw	$2,20($fp)
	sw	$0,16($fp)
$LfindMatch2:
	lw	$2,32($fp)
	lw	$3,16($fp)
	lw	$2,8($2)
	slt	$2,$3,$2
	bne	$2,$0,$LfindMatch5
	j	$LfindMatch3
$LfindMatch5:
	lw	$2,32($fp)
	lw	$2,12($2)
	bne	$2,$0,$LfindMatch6
	lw	$2,20($fp)
	lw	$3,4($2)
	lw	$2,40($fp)
	bne	$3,$2,$LfindMatch8
	j	$LfindMatch3
$LfindMatch6:
	lw	$2,20($fp)
	lw	$4,0($2)
	lw	$5,36($fp)
	jal	strCmp
	bne	$2,$0,$LfindMatch8
	j	$LfindMatch3
$LfindMatch8:
	lw	$2,20($fp)
	lw	$2,12($2)
	sw	$2,20($fp)
	lw	$2,16($fp)
	addu	$2,$2,1
	sw	$2,16($fp)
	j	$LfindMatch2
$LfindMatch3:
	lw	$2,20($fp)
	move	$sp,$fp
	lw	$31,28($sp)
	lw	$fp,24($sp)
	addu	$sp,$sp,32
	j	$31
	.end	findMatch

getValue:
	.frame	$fp,32,$31		# vars= 8, regs= 2/0, args= 16, extra= 0
	.mask	0xc0000000,-4
	.fmask	0x00000000,0
	subu	$sp,$sp,32
	sw	$31,28($sp)
	sw	$fp,24($sp)
	move	$fp,$sp
	sw	$4,32($fp)
	sw	$5,36($fp)
	sw	$6,40($fp)
	sw	$7,44($fp)
	lw	$4,32($fp)
	lw	$5,36($fp)
	lw	$6,40($fp)
	jal	findMatch
	sw	$2,16($fp)
	lw	$2,16($fp)
	beq	$2,$0,$LgetValue16
	lw	$2,16($fp)
	lw	$2,8($2)
	sw	$2,20($fp)
	j	$LgetValue15
$LgetValue16:
	lw	$4,44($fp)
	lw	$5,36($fp)
	jal	ExitWithMessage
$LgetValue15:
	lw	$2,20($fp)
	move	$sp,$fp
	lw	$31,28($sp)
	lw	$fp,24($sp)
	addu	$sp,$sp,32
	j	$31
	.end	getValue

Printf:
	.frame	$fp,40,$31		# vars= 16, regs= 2/0, args= 16, extra= 0
	.mask	0xc0000000,-4
	.fmask	0x00000000,0
	sw	$4,0($sp)
	sw	$5,4($sp)
	sw	$6,8($sp)
	sw	$7,12($sp)
	subu	$sp,$sp,40
	sw	$31,36($sp)
	sw	$fp,32($sp)
	move	$fp,$sp
	sw	$4,40($fp)
	addu	$2,$fp,44
	sw	$2,16($fp)
$LPrintf8:
	lw	$2,40($fp)
	lb	$2,0($2)
	bne	$2,$0,$LPrintf10
	j	$LPrintf7
$LPrintf10:
	lw	$2,40($fp)
	lb	$3,0($2)
	li	$2,37			# 0x25
	bne	$3,$2,$LPrintf11
	lw	$2,40($fp)
	addu	$2,$2,1
	sw	$2,40($fp)
	lw	$2,40($fp)
	lb	$3,0($2)
	li	$2,100			# 0x64
	bne	$3,$2,$LPrintf12
	lw	$2,16($fp)
	lw	$2,0($2)
	sw	$2,20($fp)
	lw	$4,20($fp)
	jal	PrintInt
	lw	$2,16($fp)
	addu	$2,$2,4
	sw	$2,16($fp)
	j	$LPrintf18
$LPrintf12:
	lw	$2,40($fp)
	lb	$3,0($2)
	li	$2,115			# 0x73
	bne	$3,$2,$LPrintf14
	lw	$2,16($fp)
	lw	$2,0($2)
	sw	$2,28($fp)
	lw	$4,28($fp)
	jal	PrintString
	lw	$2,16($fp)
	addu	$2,$2,4
	sw	$2,16($fp)
	j	$LPrintf18
$LPrintf14:
	lw	$2,40($fp)
	lb	$3,0($2)
	li	$2,99			# 0x63
	bne	$3,$2,$LPrintf7
	lw	$2,16($fp)
	lbu	$2,0($2)
	sb	$2,24($fp)
	lb	$2,24($fp)
	move	$4,$2
	jal	PrintChar
	lw	$2,16($fp)
	addu	$2,$2,1
	sw	$2,16($fp)
	j	$LPrintf18
$LPrintf11:
	lw	$2,40($fp)
	lb	$2,0($2)
	move	$4,$2
	jal	PrintChar
$LPrintf18:
	lw	$2,40($fp)
	addu	$2,$2,1
	sw	$2,40($fp)
	j	$LPrintf8
$LPrintf7:
	move	$sp,$fp
	lw	$31,36($sp)
	lw	$fp,32($sp)
	addu	$sp,$sp,40
	j	$31
	.end	Printf

addElement:
	.frame	$fp,32,$31		# vars= 8, regs= 2/0, args= 16, extra= 0
	.mask	0xc0000000,-4
	.fmask	0x00000000,0
	subu	$sp,$sp,32
	sw	$31,28($sp)
	sw	$fp,24($sp)
	move	$fp,$sp
	sw	$4,32($fp)
	sw	$5,36($fp)
	sw	$6,40($fp)
	sw	$7,44($fp)
	lw	$4,32($fp)
	lw	$5,36($fp)
	lw	$6,40($fp)
	jal	findMatch
	sw	$2,16($fp)
	lw	$2,16($fp)
	beq	$2,$0,$LaddElement12
	lw	$3,16($fp)
	lw	$2,36($fp)
	sw	$2,0($3)
	lw	$3,16($fp)
	lw	$2,40($fp)
	sw	$2,4($3)
	lw	$3,16($fp)
	lw	$2,44($fp)
	sw	$2,8($3)
	j	$LaddElement11
$LaddElement12:
	li	$4,16			# 0x10
	jal	alloc
	sw	$2,16($fp)
	lw	$3,16($fp)
	lw	$2,36($fp)
	sw	$2,0($3)
	lw	$3,16($fp)
	lw	$2,40($fp)
	sw	$2,4($3)
	lw	$3,16($fp)
	lw	$2,44($fp)
	sw	$2,8($3)
	lw	$2,16($fp)
	sw	$0,12($2)
	lw	$2,32($fp)
	lw	$2,8($2)
	bne	$2,$0,$LaddElement13
	lw	$4,32($fp)
	lw	$3,32($fp)
	lw	$2,16($fp)
	sw	$2,4($3)
	sw	$2,0($4)
	j	$LaddElement14
$LaddElement13:
	lw	$2,32($fp)
	lw	$3,4($2)
	lw	$2,16($fp)
	sw	$2,12($3)
	lw	$3,32($fp)
	lw	$2,16($fp)
	sw	$2,4($3)
$LaddElement14:
	lw	$3,32($fp)
	lw	$2,32($fp)
	lw	$2,8($2)
	addu	$2,$2,1
	sw	$2,8($3)
$LaddElement11:
	move	$2,$0
	move	$sp,$fp
	lw	$31,28($sp)
	lw	$fp,24($sp)
	addu	$sp,$sp,32
	j	$31
	.end	addElement

strCmp:
	.frame	$fp,16,$31		# vars= 8, regs= 1/0, args= 0, extra= 0
	.mask	0x40000000,-8
	.fmask	0x00000000,0
	subu	$sp,$sp,16
	sw	$fp,8($sp)
	move	$fp,$sp
	sw	$4,16($fp)
	sw	$5,20($fp)
$LstrCmp2:
	lw	$2,16($fp)
	lw	$3,20($fp)
	lb	$4,0($2)
	lb	$2,0($3)
	bne	$4,$2,$LstrCmp3
	lw	$2,16($fp)
	lb	$2,0($2)
	bne	$2,$0,$LstrCmp4
	j	$LstrCmp3
$LstrCmp4:
	lw	$2,16($fp)
	addu	$2,$2,1
	sw	$2,16($fp)
	lw	$2,20($fp)
	addu	$2,$2,1
	sw	$2,20($fp)
	j	$LstrCmp2
$LstrCmp3:
	lw	$2,16($fp)
	lw	$3,20($fp)
	lb	$4,0($2)
	lb	$2,0($3)
	slt	$2,$2,$4
	beq	$2,$0,$LstrCmp6
	li	$2,1			# 0x1
	sw	$2,0($fp)
	j	$LstrCmp1
$LstrCmp6:
	lw	$2,16($fp)
	lw	$3,20($fp)
	lb	$4,0($2)
	lb	$2,0($3)
	slt	$2,$4,$2
	beq	$2,$0,$LstrCmp7
	li	$2,-1			# 0xffffffffffffffff
	sw	$2,0($fp)
	j	$LstrCmp1
$LstrCmp7:
	sw	$0,0($fp)
$LstrCmp1:
	lw	$2,0($fp)
	move	$sp,$fp
	lw	$fp,8($sp)
	addu	$sp,$sp,16
	j	$31
	.end	strCmp

PrintString:
	.frame	$fp,8,$31		# vars= 0, regs= 1/0, args= 0, extra= 0
	.mask	0x40000000,-8
	.fmask	0x00000000,0
	subu	$sp,$sp,8
	sw	$fp,0($sp)
	move	$fp,$sp
	sw	$4,8($fp)
	lw	$2,8($fp)
 #APP
	
            move $a0, $2
            li   $v0, 4
            syscall
        
 #NO_APP
	move	$sp,$fp
	lw	$fp,0($sp)
	addu	$sp,$sp,8
	j	$31
	.end	PrintString

