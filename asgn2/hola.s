 ### GENERATED MIPS ASSEMBLY - COMPERLER ###
 ### FILENAME : test/test4.ir ###

.data
# VARIABLES
.align 2
$V_a : .word 0

.align 2
$V_i : .word 0


# ARRAYS
.align 2
$A_g : .word 0:1


# STRINGS
.align 2
$STR_0 : .asciiz "KEY ERROR: Match not found
"
.align 2
$STR_2 : .asciiz "%d"
.align 2
$STR_1 : .asciiz "Enter a number : "
.align 2
$STR_3 : .asciiz "Factorial of %d is %d\n"

# HASHES
.align 2
$H_h : .word 0


.text
main:

    # BASIC BLOCK #0

    # INSTR : a = 1
    li $t3, 1

    # INSTR : declare g[1]

    # INSTR : declare h{0}
    sw $t3, $V_a

    li $v0, 0                  # Passing the type of hash
    jal initHash               # Allocating memory and initializing the hash
    sw $v0, $H_h               # Storing the returned memory address of hash

    # INSTR : Print ['"Enter a number : "']
    la $a0, $STR_1
    jal Printf


    # INSTR : Read ['"%d"', 'g[0]']
    la $a0, $STR_2
    li $t9, 0
    la $a1, $A_g
    sll $t9, $t9, 2
    add $a1, $a1, $t9
    jal Scanf


    # INSTR : i = 1
    li $t3, 1
    sw $t3, $V_i


    # BASIC BLOCK #1

    # INSTR : If ( i > g[0] ) GOTO $LID_8
$LID_4:
    lw $t3, $V_i

    li $t9, 0                  # Load index for the array access
    la $t7, $A_g               # Load array address
    sll $t9, $t9, 2            # Multiply index by 4
    add $t7, $t7, $t9          # Add index as an offset to array address
    lw $t7, 0($t7)             # Extract array value
    sgt $t3, $t3, $t7
    bgtz $t3, $LID_8

    # BASIC BLOCK #2

    # INSTR : a = a * i
    lw $t3, $V_a
    lw $t4, $V_i

    multu $t3, $t4
    mflo $t3

    # INSTR : i = i + 1
    addu $t4, $t4, 1

    # INSTR : GOTO $LID_4
    sw $t3, $V_a

    sw $t4, $V_i

    j $LID_4

    # BASIC BLOCK #3

    # INSTR : Print ['"Factorial of %d is %d\\n"', 'g[0]', 'a']
$LID_8:
    la $a0, $STR_3
    li $t9, 0
    la $a1, $A_g
    sll $t9, $t9, 2
    add $a1, $a1, $t9
    lw $a1, 0($a1)
    lw $a2, $V_a
    jal Printf


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

ReadInt:
	.frame	$fp,16,$31		# vars= 8, regs= 1/0, args= 0, extra= 0
	.mask	0x40000000,-8
	.fmask	0x00000000,0
	subu	$sp,$sp,16
	sw	$fp,8($sp)
	move	$fp,$sp
 #APP
	
            li  $v0, 5
            syscall
            move $2, $v0
        
 #NO_APP
	sw	$2,0($fp)
	lw	$2,0($fp)
	move	$sp,$fp
	lw	$fp,8($sp)
	addu	$sp,$sp,16
	j	$31
	.end	ReadInt

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

Scanf:
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
$L20:
	lw	$2,40($fp)
	lb	$2,0($2)
	bne	$2,$0,$L22
	j	$L19
$L22:
	lw	$2,40($fp)
	lb	$3,0($2)
	li	$2,37			# 0x25
	bne	$3,$2,$L23
	lw	$2,40($fp)
	addu	$2,$2,1
	sw	$2,40($fp)
	lw	$2,40($fp)
	lb	$3,0($2)
	li	$2,100			# 0x64
	bne	$3,$2,$L24
	lw	$2,16($fp)
	lw	$2,0($2)
	sw	$2,20($fp)
	jal	ReadInt
	move	$3,$2
	lw	$2,20($fp)
	sw	$3,0($2)
	lw	$2,16($fp)
	addu	$2,$2,4
	sw	$2,16($fp)
	j	$L23
$L24:
	lw	$2,40($fp)
	lb	$3,0($2)
	li	$2,99			# 0x63
	bne	$3,$2,$L19
	lw	$2,16($fp)
	lw	$2,0($2)
	sw	$2,24($fp)
	jal	ReadChar
	move	$3,$2
	lw	$2,24($fp)
	sb	$3,0($2)
	lw	$2,16($fp)
	addu	$2,$2,4
	sw	$2,16($fp)
$L23:
	lw	$2,40($fp)
	addu	$2,$2,1
	sw	$2,40($fp)
	j	$L20
$L19:
	move	$sp,$fp
	lw	$31,36($sp)
	lw	$fp,32($sp)
	addu	$sp,$sp,40
	j	$31
	.end	Scanf

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
$L8:
	lw	$2,40($fp)
	lb	$2,0($2)
	bne	$2,$0,$L10
	j	$L7
$L10:
	lw	$2,40($fp)
	lb	$3,0($2)
	li	$2,37			# 0x25
	bne	$3,$2,$L11
	lw	$2,40($fp)
	addu	$2,$2,1
	sw	$2,40($fp)
	lw	$2,40($fp)
	lb	$3,0($2)
	li	$2,100			# 0x64
	bne	$3,$2,$L12
	lw	$2,16($fp)
	lw	$2,0($2)
	sw	$2,20($fp)
	lw	$4,20($fp)
	jal	PrintInt
	lw	$2,16($fp)
	addu	$2,$2,4
	sw	$2,16($fp)
	j	$L18
$L12:
	lw	$2,40($fp)
	lb	$3,0($2)
	li	$2,115			# 0x73
	bne	$3,$2,$L14
	lw	$2,16($fp)
	lw	$2,0($2)
	sw	$2,28($fp)
	lw	$4,28($fp)
	jal	PrintString
	lw	$2,16($fp)
	addu	$2,$2,4
	sw	$2,16($fp)
	j	$L18
$L14:
	lw	$2,40($fp)
	lb	$3,0($2)
	li	$2,99			# 0x63
	bne	$3,$2,$L7
	lw	$2,16($fp)
	lbu	$2,0($2)
	sb	$2,24($fp)
	lb	$2,24($fp)
	move	$4,$2
	jal	PrintChar
	lw	$2,16($fp)
	addu	$2,$2,1
	sw	$2,16($fp)
	j	$L18
$L11:
	lw	$2,40($fp)
	lb	$2,0($2)
	move	$4,$2
	jal	PrintChar
$L18:
	lw	$2,40($fp)
	addu	$2,$2,1
	sw	$2,40($fp)
	j	$L8
$L7:
	move	$sp,$fp
	lw	$31,36($sp)
	lw	$fp,32($sp)
	addu	$sp,$sp,40
	j	$31
	.end	Printf

ReadChar:
	.frame	$fp,16,$31		# vars= 8, regs= 1/0, args= 0, extra= 0
	.mask	0x40000000,-8
	.fmask	0x00000000,0
	subu	$sp,$sp,16
	sw	$fp,8($sp)
	move	$fp,$sp
 #APP
	
            li  $v0, 12
            syscall
            move $2, $v0
        
 #NO_APP
	sb	$2,0($fp)
	lb	$2,0($fp)
	move	$sp,$fp
	lw	$fp,8($sp)
	addu	$sp,$sp,16
	j	$31
	.end	ReadChar

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

