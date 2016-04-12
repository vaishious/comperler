	.file	1 "typechecking.c"
	.text
	.align	2
	.globl	initArray
	.ent	initArray
initArray:
	.frame	$fp,40,$31		# vars= 8, regs= 3/0, args= 16, extra= 0
	.mask	0xc0010000,-8
	.fmask	0x00000000,0
	subu	$sp,$sp,40
	sw	$31,32($sp)
	sw	$fp,28($sp)
	sw	$16,24($sp)
	move	$fp,$sp
	li	$4,8			# 0x8
	jal	alloc
	sw	$2,16($fp)
	lw	$16,16($fp)
	li	$4,8			# 0x8
	jal	alloc
	sw	$2,4($16)
	lw	$2,16($fp)
	beq	$2,$0,$L2
	lw	$3,16($fp)
	li	$2,1			# 0x1
	sw	$2,0($3)
$L2:
	lw	$2,16($fp)
	move	$sp,$fp
	lw	$31,32($sp)
	lw	$fp,28($sp)
	lw	$16,24($sp)
	addu	$sp,$sp,40
	j	$31
	.end	initArray
	.align	2
	.globl	lengthOfArray
	.ent	lengthOfArray
lengthOfArray:
	.frame	$fp,16,$31		# vars= 8, regs= 1/0, args= 0, extra= 0
	.mask	0x40000000,-8
	.fmask	0x00000000,0
	subu	$sp,$sp,16
	sw	$fp,8($sp)
	move	$fp,$sp
	sw	$4,16($fp)
	lw	$2,16($fp)
	beq	$2,$0,$L4
	lw	$2,16($fp)
	lw	$2,0($2)
	sw	$2,0($fp)
	j	$L3
$L4:
	sw	$0,0($fp)
$L3:
	lw	$2,0($fp)
	move	$sp,$fp
	lw	$fp,8($sp)
	addu	$sp,$sp,16
	j	$31
	.end	lengthOfArray
	.align	2
	.globl	accessIndex
	.ent	accessIndex
accessIndex:
	.frame	$fp,32,$31		# vars= 8, regs= 2/0, args= 16, extra= 0
	.mask	0xc0000000,-4
	.fmask	0x00000000,0
	subu	$sp,$sp,32
	sw	$31,28($sp)
	sw	$fp,24($sp)
	move	$fp,$sp
	sw	$4,32($fp)
	sw	$5,36($fp)
	lw	$2,32($fp)
	lw	$3,36($fp)
	lw	$2,0($2)
	slt	$2,$3,$2
	bne	$2,$0,$L7
	lw	$2,36($fp)
	sll	$2,$2,4
	addu	$2,$2,16
	move	$4,$2
	jal	alloc
	sw	$2,16($fp)
	sw	$0,20($fp)
$L8:
	lw	$2,32($fp)
	lw	$3,20($fp)
	lw	$2,0($2)
	slt	$2,$3,$2
	bne	$2,$0,$L11
	j	$L9
$L11:
	lw	$2,20($fp)
	sll	$3,$2,3
	lw	$2,16($fp)
	addu	$5,$3,$2
	lw	$4,32($fp)
	lw	$2,20($fp)
	sll	$3,$2,3
	lw	$2,4($4)
	addu	$2,$3,$2
	lw	$2,0($2)
	sw	$2,0($5)
	lw	$2,20($fp)
	sll	$3,$2,3
	lw	$2,16($fp)
	addu	$2,$3,$2
	addu	$5,$2,4
	lw	$4,32($fp)
	lw	$2,20($fp)
	sll	$3,$2,3
	lw	$2,4($4)
	addu	$2,$3,$2
	addu	$2,$2,4
	lw	$2,0($2)
	sw	$2,0($5)
	lw	$2,20($fp)
	addu	$2,$2,1
	sw	$2,20($fp)
	j	$L8
$L9:
	lw	$3,32($fp)
	lw	$2,36($fp)
	sll	$2,$2,1
	addu	$2,$2,2
	sw	$2,0($3)
	lw	$3,32($fp)
	lw	$2,16($fp)
	sw	$2,4($3)
	lw	$2,32($fp)
	lw	$2,0($2)
	slt	$2,$2,2
	bne	$2,$0,$L7
	li	$4,64			# 0x40
	jal	PrintChar
	lw	$2,32($fp)
	lw	$2,4($2)
	addu	$2,$2,8
	lw	$4,0($2)
	jal	PrintInt
	li	$4,10			# 0xa
	jal	PrintChar
$L7:
	lw	$4,32($fp)
	lw	$2,36($fp)
	sll	$3,$2,3
	lw	$2,4($4)
	addu	$2,$3,$2
	move	$sp,$fp
	lw	$31,28($sp)
	lw	$fp,24($sp)
	addu	$sp,$sp,32
	j	$31
	.end	accessIndex
	.align	2
	.globl	accessIndexType
	.ent	accessIndexType
accessIndexType:
	.frame	$fp,32,$31		# vars= 8, regs= 2/0, args= 16, extra= 0
	.mask	0xc0000000,-4
	.fmask	0x00000000,0
	subu	$sp,$sp,32
	sw	$31,28($sp)
	sw	$fp,24($sp)
	move	$fp,$sp
	sw	$4,32($fp)
	sw	$5,36($fp)
	lw	$2,32($fp)
	lw	$3,36($fp)
	lw	$2,0($2)
	slt	$2,$3,$2
	bne	$2,$0,$L14
	lw	$2,36($fp)
	sll	$2,$2,4
	addu	$2,$2,16
	move	$4,$2
	jal	alloc
	sw	$2,16($fp)
	sw	$0,20($fp)
$L15:
	lw	$2,32($fp)
	lw	$3,20($fp)
	lw	$2,0($2)
	slt	$2,$3,$2
	bne	$2,$0,$L18
	j	$L16
$L18:
	lw	$2,20($fp)
	sll	$3,$2,3
	lw	$2,16($fp)
	addu	$5,$3,$2
	lw	$4,32($fp)
	lw	$2,20($fp)
	sll	$3,$2,3
	lw	$2,4($4)
	addu	$2,$3,$2
	lw	$2,0($2)
	sw	$2,0($5)
	lw	$2,20($fp)
	sll	$3,$2,3
	lw	$2,16($fp)
	addu	$2,$3,$2
	addu	$5,$2,4
	lw	$4,32($fp)
	lw	$2,20($fp)
	sll	$3,$2,3
	lw	$2,4($4)
	addu	$2,$3,$2
	addu	$2,$2,4
	lw	$2,0($2)
	sw	$2,0($5)
	lw	$2,20($fp)
	addu	$2,$2,1
	sw	$2,20($fp)
	j	$L15
$L16:
	lw	$3,32($fp)
	lw	$2,36($fp)
	sll	$2,$2,1
	addu	$2,$2,2
	sw	$2,0($3)
	lw	$3,32($fp)
	lw	$2,16($fp)
	sw	$2,4($3)
$L14:
	lw	$4,32($fp)
	lw	$2,36($fp)
	sll	$3,$2,3
	lw	$2,4($4)
	addu	$2,$3,$2
	addu	$2,$2,4
	move	$sp,$fp
	lw	$31,28($sp)
	lw	$fp,24($sp)
	addu	$sp,$sp,32
	j	$31
	.end	accessIndexType
	.align	2
	.globl	dummyFunc
	.ent	dummyFunc
dummyFunc:
	.frame	$fp,8,$31		# vars= 0, regs= 1/0, args= 0, extra= 0
	.mask	0x40000000,-8
	.fmask	0x00000000,0
	subu	$sp,$sp,8
	sw	$fp,0($sp)
	move	$fp,$sp
	sw	$4,8($fp)
	lw	$2,8($fp)
	move	$sp,$fp
	lw	$fp,0($sp)
	addu	$sp,$sp,8
	j	$31
	.end	dummyFunc
	.align	2
	.globl	convertSTRING_TO_INT
	.ent	convertSTRING_TO_INT
convertSTRING_TO_INT:
	.frame	$fp,24,$31		# vars= 16, regs= 1/0, args= 0, extra= 0
	.mask	0x40000000,-8
	.fmask	0x00000000,0
	subu	$sp,$sp,24
	sw	$fp,16($sp)
	move	$fp,$sp
	sw	$4,24($fp)
	lw	$2,24($fp)
	sw	$2,0($fp)
	sw	$0,4($fp)
	sw	$0,8($fp)
	lw	$2,0($fp)
	lb	$3,0($2)
	li	$2,45			# 0x2d
	bne	$3,$2,$L21
	li	$2,1			# 0x1
	sw	$2,4($fp)
	lw	$2,0($fp)
	addu	$2,$2,1
	sw	$2,0($fp)
	j	$L22
$L21:
	lw	$2,0($fp)
	lb	$3,0($2)
	li	$2,43			# 0x2b
	bne	$3,$2,$L22
	sw	$0,4($fp)
	lw	$2,0($fp)
	addu	$2,$2,1
	sw	$2,0($fp)
$L22:
	.set	noreorder
	nop
	.set	reorder
$L24:
	lw	$2,0($fp)
	lb	$2,0($2)
	bne	$2,$0,$L26
	j	$L25
$L26:
	lw	$2,0($fp)
	lb	$2,0($2)
	slt	$2,$2,58
	beq	$2,$0,$L28
	lw	$2,0($fp)
	lb	$2,0($2)
	slt	$2,$2,48
	bne	$2,$0,$L28
	j	$L27
$L28:
	lw	$3,4($fp)
	li	$2,1			# 0x1
	bne	$3,$2,$L29
	lw	$2,8($fp)
	subu	$2,$0,$2
	sw	$2,8($fp)
$L29:
	lw	$2,8($fp)
	sw	$2,12($fp)
	j	$L20
$L27:
	lw	$3,8($fp)
	move	$2,$3
	sll	$2,$2,2
	addu	$2,$2,$3
	sll	$3,$2,1
	lw	$2,0($fp)
	lb	$2,0($2)
	addu	$2,$3,$2
	addu	$2,$2,-48
	sw	$2,8($fp)
	lw	$2,0($fp)
	addu	$2,$2,1
	sw	$2,0($fp)
	j	$L24
$L25:
	lw	$3,4($fp)
	li	$2,1			# 0x1
	bne	$3,$2,$L30
	lw	$2,8($fp)
	subu	$2,$0,$2
	sw	$2,8($fp)
$L30:
	lw	$2,8($fp)
	sw	$2,12($fp)
$L20:
	lw	$2,12($fp)
	move	$sp,$fp
	lw	$fp,16($sp)
	addu	$sp,$sp,24
	j	$31
	.end	convertSTRING_TO_INT
	.align	2
	.globl	convertINT_TO_STRING
	.ent	convertINT_TO_STRING
convertINT_TO_STRING:
	.frame	$fp,40,$31		# vars= 16, regs= 2/0, args= 16, extra= 0
	.mask	0xc0000000,-4
	.fmask	0x00000000,0
	subu	$sp,$sp,40
	sw	$31,36($sp)
	sw	$fp,32($sp)
	move	$fp,$sp
	sw	$4,40($fp)
	li	$2,1			# 0x1
	sw	$2,16($fp)
	lw	$2,40($fp)
	sw	$2,20($fp)
	lw	$4,20($fp)
	li	$2,1717960704			# 0x66660000
	ori	$2,$2,0x6667
	mult	$4,$2
	mfhi	$2
	sra	$3,$2,2
	sra	$2,$4,31
	subu	$2,$3,$2
	sw	$2,20($fp)
$L32:
	lw	$2,20($fp)
	bgtz	$2,$L34
	j	$L33
$L34:
	lw	$2,16($fp)
	addu	$2,$2,1
	sw	$2,16($fp)
	lw	$4,20($fp)
	li	$2,1717960704			# 0x66660000
	ori	$2,$2,0x6667
	mult	$4,$2
	mfhi	$2
	sra	$3,$2,2
	sra	$2,$4,31
	subu	$2,$3,$2
	sw	$2,20($fp)
	j	$L32
$L33:
	lw	$2,16($fp)
	addu	$2,$2,1
	move	$4,$2
	jal	alloc
	sw	$2,24($fp)
	lw	$2,40($fp)
	sw	$2,20($fp)
	lw	$2,16($fp)
	addu	$2,$2,-1
	sw	$2,28($fp)
	lw	$3,24($fp)
	lw	$2,28($fp)
	addu	$5,$3,$2
	lw	$4,20($fp)
	li	$2,1717960704			# 0x66660000
	ori	$2,$2,0x6667
	mult	$4,$2
	mfhi	$2
	sra	$3,$2,2
	sra	$2,$4,31
	subu	$3,$3,$2
	move	$2,$3
	sll	$2,$2,2
	addu	$2,$2,$3
	sll	$2,$2,1
	subu	$2,$4,$2
	addu	$2,$2,48
	sb	$2,0($5)
	lw	$4,20($fp)
	li	$2,1717960704			# 0x66660000
	ori	$2,$2,0x6667
	mult	$4,$2
	mfhi	$2
	sra	$3,$2,2
	sra	$2,$4,31
	subu	$2,$3,$2
	sw	$2,20($fp)
	lw	$2,28($fp)
	addu	$2,$2,-1
	sw	$2,28($fp)
$L35:
	lw	$2,20($fp)
	bgtz	$2,$L37
	j	$L36
$L37:
	lw	$3,24($fp)
	lw	$2,28($fp)
	addu	$5,$3,$2
	lw	$4,20($fp)
	li	$2,1717960704			# 0x66660000
	ori	$2,$2,0x6667
	mult	$4,$2
	mfhi	$2
	sra	$3,$2,2
	sra	$2,$4,31
	subu	$3,$3,$2
	move	$2,$3
	sll	$2,$2,2
	addu	$2,$2,$3
	sll	$2,$2,1
	subu	$2,$4,$2
	addu	$2,$2,48
	sb	$2,0($5)
	lw	$4,20($fp)
	li	$2,1717960704			# 0x66660000
	ori	$2,$2,0x6667
	mult	$4,$2
	mfhi	$2
	sra	$3,$2,2
	sra	$2,$4,31
	subu	$2,$3,$2
	sw	$2,20($fp)
	lw	$2,28($fp)
	addu	$2,$2,-1
	sw	$2,28($fp)
	j	$L35
$L36:
	lw	$2,24($fp)
	move	$sp,$fp
	lw	$31,36($sp)
	lw	$fp,32($sp)
	addu	$sp,$sp,40
	j	$31
	.end	convertINT_TO_STRING
	.align	2
	.globl	op_PLUS
	.ent	op_PLUS
op_PLUS:
	.frame	$fp,32,$31		# vars= 8, regs= 2/0, args= 16, extra= 0
	.mask	0xc0000000,-4
	.fmask	0x00000000,0
	subu	$sp,$sp,32
	sw	$31,28($sp)
	sw	$fp,24($sp)
	move	$fp,$sp
	sw	$4,32($fp)
	sw	$5,36($fp)
	lw	$2,OP1_TYPECAST
	lw	$4,32($fp)
	jal	$31,$2
	sw	$2,32($fp)
	lw	$2,OP2_TYPECAST
	lw	$4,36($fp)
	jal	$31,$2
	sw	$2,36($fp)
	lw	$2,32($fp)
	sw	$2,16($fp)
	lw	$2,36($fp)
	sw	$2,20($fp)
	lw	$3,16($fp)
	lw	$2,20($fp)
	addu	$2,$3,$2
	move	$sp,$fp
	lw	$31,28($sp)
	lw	$fp,24($sp)
	addu	$sp,$sp,32
	j	$31
	.end	op_PLUS
	.align	2
	.globl	op_MINUS
	.ent	op_MINUS
op_MINUS:
	.frame	$fp,32,$31		# vars= 8, regs= 2/0, args= 16, extra= 0
	.mask	0xc0000000,-4
	.fmask	0x00000000,0
	subu	$sp,$sp,32
	sw	$31,28($sp)
	sw	$fp,24($sp)
	move	$fp,$sp
	sw	$4,32($fp)
	sw	$5,36($fp)
	lw	$2,OP1_TYPECAST
	lw	$4,32($fp)
	jal	$31,$2
	sw	$2,32($fp)
	lw	$2,OP2_TYPECAST
	lw	$4,36($fp)
	jal	$31,$2
	sw	$2,36($fp)
	lw	$2,32($fp)
	sw	$2,16($fp)
	lw	$2,36($fp)
	sw	$2,20($fp)
	lw	$3,16($fp)
	lw	$2,20($fp)
	subu	$2,$3,$2
	move	$sp,$fp
	lw	$31,28($sp)
	lw	$fp,24($sp)
	addu	$sp,$sp,32
	j	$31
	.end	op_MINUS
	.align	2
	.globl	op_MULT
	.ent	op_MULT
op_MULT:
	.frame	$fp,32,$31		# vars= 8, regs= 2/0, args= 16, extra= 0
	.mask	0xc0000000,-4
	.fmask	0x00000000,0
	subu	$sp,$sp,32
	sw	$31,28($sp)
	sw	$fp,24($sp)
	move	$fp,$sp
	sw	$4,32($fp)
	sw	$5,36($fp)
	lw	$2,OP1_TYPECAST
	lw	$4,32($fp)
	jal	$31,$2
	sw	$2,32($fp)
	lw	$2,OP2_TYPECAST
	lw	$4,36($fp)
	jal	$31,$2
	sw	$2,36($fp)
	lw	$2,32($fp)
	sw	$2,16($fp)
	lw	$2,36($fp)
	sw	$2,20($fp)
	lw	$3,16($fp)
	lw	$2,20($fp)
	mult	$3,$2
	mflo	$2
	move	$sp,$fp
	lw	$31,28($sp)
	lw	$fp,24($sp)
	addu	$sp,$sp,32
	j	$31
	.end	op_MULT
	.align	2
	.globl	op_DIV
	.ent	op_DIV
op_DIV:
	.frame	$fp,32,$31		# vars= 8, regs= 2/0, args= 16, extra= 0
	.mask	0xc0000000,-4
	.fmask	0x00000000,0
	subu	$sp,$sp,32
	sw	$31,28($sp)
	sw	$fp,24($sp)
	move	$fp,$sp
	sw	$4,32($fp)
	sw	$5,36($fp)
	lw	$2,OP1_TYPECAST
	lw	$4,32($fp)
	jal	$31,$2
	sw	$2,32($fp)
	lw	$2,OP2_TYPECAST
	lw	$4,36($fp)
	jal	$31,$2
	sw	$2,36($fp)
	lw	$2,32($fp)
	sw	$2,16($fp)
	lw	$2,36($fp)
	sw	$2,20($fp)
	lw	$3,16($fp)
	lw	$2,20($fp)
	div	$0,$3,$2
	mflo	$3
	.set	noreorder
	bne	$2,$0,1f
	nop
	break	7
1:
	.set	reorder
	move	$2,$3
	move	$sp,$fp
	lw	$31,28($sp)
	lw	$fp,24($sp)
	addu	$sp,$sp,32
	j	$31
	.end	op_DIV
	.align	2
	.globl	op_MOD
	.ent	op_MOD
op_MOD:
	.frame	$fp,32,$31		# vars= 8, regs= 2/0, args= 16, extra= 0
	.mask	0xc0000000,-4
	.fmask	0x00000000,0
	subu	$sp,$sp,32
	sw	$31,28($sp)
	sw	$fp,24($sp)
	move	$fp,$sp
	sw	$4,32($fp)
	sw	$5,36($fp)
	lw	$2,OP1_TYPECAST
	lw	$4,32($fp)
	jal	$31,$2
	sw	$2,32($fp)
	lw	$2,OP2_TYPECAST
	lw	$4,36($fp)
	jal	$31,$2
	sw	$2,36($fp)
	lw	$2,32($fp)
	sw	$2,16($fp)
	lw	$2,36($fp)
	sw	$2,20($fp)
	lw	$3,16($fp)
	lw	$2,20($fp)
	div	$0,$3,$2
	mfhi	$3
	.set	noreorder
	bne	$2,$0,1f
	nop
	break	7
1:
	.set	reorder
	move	$2,$3
	move	$sp,$fp
	lw	$31,28($sp)
	lw	$fp,24($sp)
	addu	$sp,$sp,32
	j	$31
	.end	op_MOD
	.align	2
	.globl	op_STRING_CMP
	.ent	op_STRING_CMP
op_STRING_CMP:
	.frame	$fp,40,$31		# vars= 16, regs= 2/0, args= 16, extra= 0
	.mask	0xc0000000,-4
	.fmask	0x00000000,0
	subu	$sp,$sp,40
	sw	$31,36($sp)
	sw	$fp,32($sp)
	move	$fp,$sp
	sw	$4,40($fp)
	sw	$5,44($fp)
	lw	$2,OP1_TYPECAST
	lw	$4,40($fp)
	jal	$31,$2
	sw	$2,16($fp)
	lw	$2,OP2_TYPECAST
	lw	$4,44($fp)
	jal	$31,$2
	sw	$2,20($fp)
	sw	$0,24($fp)
$L44:
	lw	$3,16($fp)
	lw	$2,24($fp)
	addu	$2,$3,$2
	lb	$2,0($2)
	bne	$2,$0,$L47
	lw	$3,20($fp)
	lw	$2,24($fp)
	addu	$2,$3,$2
	lb	$2,0($2)
	bne	$2,$0,$L47
	j	$L45
$L47:
	lw	$3,16($fp)
	lw	$2,24($fp)
	addu	$4,$3,$2
	lw	$3,20($fp)
	lw	$2,24($fp)
	addu	$2,$3,$2
	lb	$3,0($4)
	lb	$2,0($2)
	slt	$2,$2,$3
	beq	$2,$0,$L48
	li	$2,1			# 0x1
	sw	$2,28($fp)
	j	$L43
$L48:
	lw	$3,16($fp)
	lw	$2,24($fp)
	addu	$4,$3,$2
	lw	$3,20($fp)
	lw	$2,24($fp)
	addu	$2,$3,$2
	lb	$3,0($4)
	lb	$2,0($2)
	slt	$2,$3,$2
	beq	$2,$0,$L46
	li	$2,-1			# 0xffffffffffffffff
	sw	$2,28($fp)
	j	$L43
$L46:
	lw	$2,24($fp)
	addu	$2,$2,1
	sw	$2,24($fp)
	j	$L44
$L45:
	sw	$0,28($fp)
$L43:
	lw	$2,28($fp)
	move	$sp,$fp
	lw	$31,36($sp)
	lw	$fp,32($sp)
	addu	$sp,$sp,40
	j	$31
	.end	op_STRING_CMP
	.align	2
	.globl	op_STRING_DOT
	.ent	op_STRING_DOT
op_STRING_DOT:
	.frame	$fp,48,$31		# vars= 24, regs= 2/0, args= 16, extra= 0
	.mask	0xc0000000,-4
	.fmask	0x00000000,0
	subu	$sp,$sp,48
	sw	$31,44($sp)
	sw	$fp,40($sp)
	move	$fp,$sp
	sw	$4,48($fp)
	sw	$5,52($fp)
	lw	$2,OP1_TYPECAST
	lw	$4,48($fp)
	jal	$31,$2
	sw	$2,16($fp)
	lw	$2,OP2_TYPECAST
	lw	$4,52($fp)
	jal	$31,$2
	sw	$2,20($fp)
	sw	$0,24($fp)
	sw	$0,28($fp)
	sw	$0,24($fp)
$L52:
	lw	$3,16($fp)
	lw	$2,24($fp)
	addu	$2,$3,$2
	lb	$2,0($2)
	bne	$2,$0,$L54
	j	$L53
$L54:
	lw	$2,24($fp)
	addu	$2,$2,1
	sw	$2,24($fp)
	j	$L52
$L53:
	sw	$0,28($fp)
$L56:
	lw	$3,20($fp)
	lw	$2,28($fp)
	addu	$2,$3,$2
	lb	$2,0($2)
	bne	$2,$0,$L58
	j	$L57
$L58:
	lw	$2,28($fp)
	addu	$2,$2,1
	sw	$2,28($fp)
	j	$L56
$L57:
	lw	$3,24($fp)
	lw	$2,28($fp)
	addu	$2,$3,$2
	addu	$2,$2,1
	move	$4,$2
	jal	alloc
	sw	$2,32($fp)
	sw	$0,36($fp)
$L60:
	lw	$2,36($fp)
	lw	$3,24($fp)
	slt	$2,$2,$3
	bne	$2,$0,$L63
	j	$L61
$L63:
	lw	$3,32($fp)
	lw	$2,36($fp)
	addu	$4,$3,$2
	lw	$3,16($fp)
	lw	$2,36($fp)
	addu	$2,$3,$2
	lbu	$2,0($2)
	sb	$2,0($4)
	lw	$2,36($fp)
	addu	$2,$2,1
	sw	$2,36($fp)
	j	$L60
$L61:
	sw	$0,36($fp)
$L64:
	lw	$2,36($fp)
	lw	$3,28($fp)
	slt	$2,$2,$3
	bne	$2,$0,$L67
	j	$L65
$L67:
	lw	$3,24($fp)
	lw	$2,36($fp)
	addu	$3,$3,$2
	lw	$2,32($fp)
	addu	$4,$3,$2
	lw	$3,20($fp)
	lw	$2,36($fp)
	addu	$2,$3,$2
	lbu	$2,0($2)
	sb	$2,0($4)
	lw	$2,36($fp)
	addu	$2,$2,1
	sw	$2,36($fp)
	j	$L64
$L65:
	lw	$3,24($fp)
	lw	$2,28($fp)
	addu	$3,$3,$2
	lw	$2,32($fp)
	addu	$2,$3,$2
	sb	$0,0($2)
	lw	$2,32($fp)
	move	$sp,$fp
	lw	$31,44($sp)
	lw	$fp,40($sp)
	addu	$sp,$sp,48
	j	$31
	.end	op_STRING_DOT
	.align	2
	.globl	op_STRING_REPEAT
	.ent	op_STRING_REPEAT
op_STRING_REPEAT:
	.frame	$fp,56,$31		# vars= 32, regs= 2/0, args= 16, extra= 0
	.mask	0xc0000000,-4
	.fmask	0x00000000,0
	subu	$sp,$sp,56
	sw	$31,52($sp)
	sw	$fp,48($sp)
	move	$fp,$sp
	sw	$4,56($fp)
	sw	$5,60($fp)
	lw	$2,OP1_TYPECAST
	lw	$4,56($fp)
	jal	$31,$2
	sw	$2,16($fp)
	lw	$2,OP2_TYPECAST
	lw	$4,60($fp)
	jal	$31,$2
	sw	$2,20($fp)
	lw	$2,20($fp)
	bgtz	$2,$L69
	li	$4,1			# 0x1
	jal	alloc
	sw	$2,24($fp)
	lw	$2,24($fp)
	sb	$0,0($2)
	lw	$2,24($fp)
	sw	$2,40($fp)
	j	$L68
$L69:
	sw	$0,24($fp)
	sw	$0,24($fp)
$L70:
	lw	$3,16($fp)
	lw	$2,24($fp)
	addu	$2,$3,$2
	lb	$2,0($2)
	bne	$2,$0,$L72
	j	$L71
$L72:
	lw	$2,24($fp)
	addu	$2,$2,1
	sw	$2,24($fp)
	j	$L70
$L71:
	lw	$3,24($fp)
	lw	$2,20($fp)
	mult	$3,$2
	mflo	$2
	addu	$2,$2,1
	move	$4,$2
	jal	alloc
	sw	$2,28($fp)
	sw	$0,32($fp)
$L74:
	lw	$2,32($fp)
	lw	$3,20($fp)
	slt	$2,$2,$3
	bne	$2,$0,$L77
	j	$L75
$L77:
	sw	$0,36($fp)
$L78:
	lw	$2,36($fp)
	lw	$3,24($fp)
	slt	$2,$2,$3
	bne	$2,$0,$L81
	j	$L76
$L81:
	lw	$3,32($fp)
	lw	$2,24($fp)
	mult	$3,$2
	mflo	$3
	lw	$2,36($fp)
	addu	$3,$3,$2
	lw	$2,28($fp)
	addu	$4,$3,$2
	lw	$3,16($fp)
	lw	$2,36($fp)
	addu	$2,$3,$2
	lbu	$2,0($2)
	sb	$2,0($4)
	lw	$2,36($fp)
	addu	$2,$2,1
	sw	$2,36($fp)
	j	$L78
$L76:
	lw	$2,32($fp)
	addu	$2,$2,1
	sw	$2,32($fp)
	j	$L74
$L75:
	lw	$3,20($fp)
	lw	$2,24($fp)
	mult	$3,$2
	mflo	$3
	lw	$2,28($fp)
	addu	$2,$3,$2
	sb	$0,0($2)
	lw	$2,28($fp)
	sw	$2,40($fp)
$L68:
	lw	$2,40($fp)
	move	$sp,$fp
	lw	$31,52($sp)
	lw	$fp,48($sp)
	addu	$sp,$sp,56
	j	$31
	.end	op_STRING_REPEAT
	.align	2
	.globl	op_ARRAY_CONCAT
	.ent	op_ARRAY_CONCAT
op_ARRAY_CONCAT:
	.frame	$fp,56,$31		# vars= 24, regs= 3/0, args= 16, extra= 0
	.mask	0xc0010000,-8
	.fmask	0x00000000,0
	subu	$sp,$sp,56
	sw	$31,48($sp)
	sw	$fp,44($sp)
	sw	$16,40($sp)
	move	$fp,$sp
	sw	$4,56($fp)
	sw	$5,60($fp)
	lw	$2,OP1_TYPECAST
	lw	$4,56($fp)
	jal	$31,$2
	sw	$2,16($fp)
	lw	$2,OP2_TYPECAST
	lw	$4,60($fp)
	jal	$31,$2
	sw	$2,20($fp)
	lw	$4,16($fp)
	jal	lengthOfArray
	sw	$2,24($fp)
	lw	$4,20($fp)
	jal	lengthOfArray
	sw	$2,28($fp)
	jal	initArray
	sw	$2,32($fp)
	sw	$0,36($fp)
$L83:
	lw	$2,36($fp)
	lw	$3,24($fp)
	slt	$2,$2,$3
	bne	$2,$0,$L86
	j	$L84
$L86:
	lw	$4,32($fp)
	lw	$5,36($fp)
	jal	accessIndex
	move	$16,$2
	lw	$4,16($fp)
	lw	$5,36($fp)
	jal	accessIndex
	lw	$2,0($2)
	sw	$2,0($16)
	lw	$2,36($fp)
	addu	$2,$2,1
	sw	$2,36($fp)
	j	$L83
$L84:
	sw	$0,36($fp)
$L87:
	lw	$2,36($fp)
	lw	$3,28($fp)
	slt	$2,$2,$3
	bne	$2,$0,$L90
	j	$L88
$L90:
	lw	$3,24($fp)
	lw	$2,36($fp)
	addu	$2,$3,$2
	lw	$4,32($fp)
	move	$5,$2
	jal	accessIndex
	move	$16,$2
	lw	$4,20($fp)
	lw	$5,36($fp)
	jal	accessIndex
	lw	$2,0($2)
	sw	$2,0($16)
	lw	$2,36($fp)
	addu	$2,$2,1
	sw	$2,36($fp)
	j	$L87
$L88:
	lw	$2,32($fp)
	move	$sp,$fp
	lw	$31,48($sp)
	lw	$fp,44($sp)
	lw	$16,40($sp)
	addu	$sp,$sp,56
	j	$31
	.end	op_ARRAY_CONCAT
	.globl	typeMaps
	.sdata
	.align	2
$LC0:
	.ascii	"UNKNOWN\000"
	.align	2
$LC1:
	.ascii	"STRING\000"
	.align	2
$LC2:
	.ascii	"INT\000"
	.align	2
$LC3:
	.ascii	"ARRAY\000"
	.align	2
$LC4:
	.ascii	"HASH\000"
	.data
	.align	2
typeMaps:
	.word	$LC0
	.word	$LC1
	.word	$LC2
	.word	$LC3
	.word	$LC4
	.text
	.align	2
	.globl	Exit
	.ent	Exit
Exit:
	.frame	$fp,8,$31		# vars= 0, regs= 1/0, args= 0, extra= 0
	.mask	0x40000000,-8
	.fmask	0x00000000,0
	subu	$sp,$sp,8
	sw	$fp,0($sp)
	move	$fp,$sp
 #APP
	
            li $v0, 10
            syscall
        
 #NO_APP
	move	$sp,$fp
	lw	$fp,0($sp)
	addu	$sp,$sp,8
	j	$31
	.end	Exit
	.rdata
	.align	2
$LC5:
	.ascii	"Atleast one argument of arithmetic operation has to be a"
	.ascii	"n INT/STRING\000"
	.align	2
$LC6:
	.ascii	"Cannot perform arithmetic operation on %s with a INT/STR"
	.ascii	"ING\000"
	.text
	.align	2
	.globl	typecheck_GENERIC_INT_STRING_3OP
	.ent	typecheck_GENERIC_INT_STRING_3OP
typecheck_GENERIC_INT_STRING_3OP:
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
	sw	$2,16($fp)
	lw	$2,36($fp)
	sw	$2,20($fp)
	la	$2,dummyFunc
	sw	$2,OP1_TYPECAST
	la	$2,dummyFunc
	sw	$2,OP2_TYPECAST
	lw	$2,40($fp)
	sw	$2,OPCONTROL
	lw	$3,16($fp)
	li	$2,2			# 0x2
	beq	$3,$2,$L93
	lw	$3,16($fp)
	li	$2,1			# 0x1
	beq	$3,$2,$L93
	lw	$3,20($fp)
	li	$2,2			# 0x2
	beq	$3,$2,$L93
	lw	$3,20($fp)
	li	$2,1			# 0x1
	beq	$3,$2,$L93
	la	$4,$LC5
	jal	PrintfNormal
	jal	Exit
$L93:
	lw	$3,16($fp)
	li	$2,2			# 0x2
	beq	$3,$2,$L94
	lw	$3,16($fp)
	li	$2,1			# 0x1
	beq	$3,$2,$L94
	lw	$2,16($fp)
	sll	$3,$2,2
	la	$2,typeMaps
	addu	$2,$3,$2
	la	$4,$LC6
	lw	$5,0($2)
	jal	PrintfNormal
	jal	Exit
$L94:
	lw	$3,20($fp)
	li	$2,2			# 0x2
	beq	$3,$2,$L95
	lw	$3,20($fp)
	li	$2,1			# 0x1
	beq	$3,$2,$L95
	lw	$2,20($fp)
	sll	$3,$2,2
	la	$2,typeMaps
	addu	$2,$3,$2
	la	$4,$LC6
	lw	$5,0($2)
	jal	PrintfNormal
	jal	Exit
$L95:
	lw	$3,16($fp)
	li	$2,1			# 0x1
	bne	$3,$2,$L96
	la	$2,convertSTRING_TO_INT
	sw	$2,OP1_TYPECAST
$L96:
	lw	$3,20($fp)
	li	$2,1			# 0x1
	bne	$3,$2,$L97
	la	$2,convertSTRING_TO_INT
	sw	$2,OP2_TYPECAST
$L97:
	li	$2,2			# 0x2
	move	$sp,$fp
	lw	$31,28($sp)
	lw	$fp,24($sp)
	addu	$sp,$sp,32
	j	$31
	.end	typecheck_GENERIC_INT_STRING_3OP
	.align	2
	.globl	typecheck_INT_PLUS
	.ent	typecheck_INT_PLUS
typecheck_INT_PLUS:
	.frame	$fp,40,$31		# vars= 16, regs= 2/0, args= 16, extra= 0
	.mask	0xc0000000,-4
	.fmask	0x00000000,0
	subu	$sp,$sp,40
	sw	$31,36($sp)
	sw	$fp,32($sp)
	move	$fp,$sp
	sw	$4,40($fp)
	sw	$5,44($fp)
	lw	$2,40($fp)
	sw	$2,16($fp)
	lw	$2,44($fp)
	sw	$2,20($fp)
	lw	$3,16($fp)
	li	$2,3			# 0x3
	bne	$3,$2,$L99
	lw	$3,20($fp)
	li	$2,3			# 0x3
	bne	$3,$2,$L99
	la	$2,dummyFunc
	sw	$2,OP1_TYPECAST
	la	$2,dummyFunc
	sw	$2,OP2_TYPECAST
	la	$2,op_ARRAY_CONCAT
	sw	$2,OPCONTROL
	li	$2,3			# 0x3
	sw	$2,24($fp)
	j	$L98
$L99:
	lw	$4,40($fp)
	lw	$5,44($fp)
	la	$6,op_PLUS
	jal	typecheck_GENERIC_INT_STRING_3OP
	sw	$2,24($fp)
$L98:
	lw	$2,24($fp)
	move	$sp,$fp
	lw	$31,36($sp)
	lw	$fp,32($sp)
	addu	$sp,$sp,40
	j	$31
	.end	typecheck_INT_PLUS
	.align	2
	.globl	typecheck_INT_MINUS
	.ent	typecheck_INT_MINUS
typecheck_INT_MINUS:
	.frame	$fp,24,$31		# vars= 0, regs= 2/0, args= 16, extra= 0
	.mask	0xc0000000,-4
	.fmask	0x00000000,0
	subu	$sp,$sp,24
	sw	$31,20($sp)
	sw	$fp,16($sp)
	move	$fp,$sp
	sw	$4,24($fp)
	sw	$5,28($fp)
	lw	$4,24($fp)
	lw	$5,28($fp)
	la	$6,op_MINUS
	jal	typecheck_GENERIC_INT_STRING_3OP
	move	$sp,$fp
	lw	$31,20($sp)
	lw	$fp,16($sp)
	addu	$sp,$sp,24
	j	$31
	.end	typecheck_INT_MINUS
	.align	2
	.globl	typecheck_INT_MULT
	.ent	typecheck_INT_MULT
typecheck_INT_MULT:
	.frame	$fp,24,$31		# vars= 0, regs= 2/0, args= 16, extra= 0
	.mask	0xc0000000,-4
	.fmask	0x00000000,0
	subu	$sp,$sp,24
	sw	$31,20($sp)
	sw	$fp,16($sp)
	move	$fp,$sp
	sw	$4,24($fp)
	sw	$5,28($fp)
	lw	$4,24($fp)
	lw	$5,28($fp)
	la	$6,op_MULT
	jal	typecheck_GENERIC_INT_STRING_3OP
	move	$sp,$fp
	lw	$31,20($sp)
	lw	$fp,16($sp)
	addu	$sp,$sp,24
	j	$31
	.end	typecheck_INT_MULT
	.align	2
	.globl	typecheck_INT_DIV
	.ent	typecheck_INT_DIV
typecheck_INT_DIV:
	.frame	$fp,24,$31		# vars= 0, regs= 2/0, args= 16, extra= 0
	.mask	0xc0000000,-4
	.fmask	0x00000000,0
	subu	$sp,$sp,24
	sw	$31,20($sp)
	sw	$fp,16($sp)
	move	$fp,$sp
	sw	$4,24($fp)
	sw	$5,28($fp)
	lw	$4,24($fp)
	lw	$5,28($fp)
	la	$6,op_DIV
	jal	typecheck_GENERIC_INT_STRING_3OP
	move	$sp,$fp
	lw	$31,20($sp)
	lw	$fp,16($sp)
	addu	$sp,$sp,24
	j	$31
	.end	typecheck_INT_DIV
	.align	2
	.globl	typecheck_INT_MOD
	.ent	typecheck_INT_MOD
typecheck_INT_MOD:
	.frame	$fp,24,$31		# vars= 0, regs= 2/0, args= 16, extra= 0
	.mask	0xc0000000,-4
	.fmask	0x00000000,0
	subu	$sp,$sp,24
	sw	$31,20($sp)
	sw	$fp,16($sp)
	move	$fp,$sp
	sw	$4,24($fp)
	sw	$5,28($fp)
	lw	$4,24($fp)
	lw	$5,28($fp)
	la	$6,op_MOD
	jal	typecheck_GENERIC_INT_STRING_3OP
	move	$sp,$fp
	lw	$31,20($sp)
	lw	$fp,16($sp)
	addu	$sp,$sp,24
	j	$31
	.end	typecheck_INT_MOD
	.rdata
	.align	2
$LC7:
	.ascii	"Atleast one argument of string operation has to be an IN"
	.ascii	"T/STRING\000"
	.align	2
$LC8:
	.ascii	"Cannot perform string operation on %s with a INT/STRING\000"
	.text
	.align	2
	.globl	typecheck_GENERIC_STRING_3OP
	.ent	typecheck_GENERIC_STRING_3OP
typecheck_GENERIC_STRING_3OP:
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
	sw	$2,16($fp)
	lw	$2,36($fp)
	sw	$2,20($fp)
	la	$2,dummyFunc
	sw	$2,OP1_TYPECAST
	la	$2,dummyFunc
	sw	$2,OP2_TYPECAST
	lw	$2,40($fp)
	sw	$2,OPCONTROL
	lw	$3,16($fp)
	li	$2,2			# 0x2
	beq	$3,$2,$L105
	lw	$3,16($fp)
	li	$2,1			# 0x1
	beq	$3,$2,$L105
	lw	$3,20($fp)
	li	$2,2			# 0x2
	beq	$3,$2,$L105
	lw	$3,20($fp)
	li	$2,1			# 0x1
	beq	$3,$2,$L105
	la	$4,$LC7
	jal	PrintfNormal
	jal	Exit
$L105:
	lw	$3,16($fp)
	li	$2,2			# 0x2
	beq	$3,$2,$L106
	lw	$3,16($fp)
	li	$2,1			# 0x1
	beq	$3,$2,$L106
	lw	$2,16($fp)
	sll	$3,$2,2
	la	$2,typeMaps
	addu	$2,$3,$2
	la	$4,$LC8
	lw	$5,0($2)
	jal	PrintfNormal
	jal	Exit
$L106:
	lw	$3,20($fp)
	li	$2,2			# 0x2
	beq	$3,$2,$L107
	lw	$3,20($fp)
	li	$2,1			# 0x1
	beq	$3,$2,$L107
	lw	$2,20($fp)
	sll	$3,$2,2
	la	$2,typeMaps
	addu	$2,$3,$2
	la	$4,$LC8
	lw	$5,0($2)
	jal	PrintfNormal
	jal	Exit
$L107:
	lw	$3,16($fp)
	li	$2,2			# 0x2
	bne	$3,$2,$L108
	la	$2,convertINT_TO_STRING
	sw	$2,OP1_TYPECAST
$L108:
	lw	$3,20($fp)
	li	$2,2			# 0x2
	bne	$3,$2,$L109
	la	$2,convertINT_TO_STRING
	sw	$2,OP2_TYPECAST
$L109:
	li	$2,1			# 0x1
	move	$sp,$fp
	lw	$31,28($sp)
	lw	$fp,24($sp)
	addu	$sp,$sp,32
	j	$31
	.end	typecheck_GENERIC_STRING_3OP
	.align	2
	.globl	typecheck_STRING_RELOP
	.ent	typecheck_STRING_RELOP
typecheck_STRING_RELOP:
	.frame	$fp,24,$31		# vars= 0, regs= 2/0, args= 16, extra= 0
	.mask	0xc0000000,-4
	.fmask	0x00000000,0
	subu	$sp,$sp,24
	sw	$31,20($sp)
	sw	$fp,16($sp)
	move	$fp,$sp
	sw	$4,24($fp)
	sw	$5,28($fp)
	lw	$4,24($fp)
	lw	$5,28($fp)
	la	$6,op_STRING_CMP
	jal	typecheck_GENERIC_STRING_3OP
	move	$sp,$fp
	lw	$31,20($sp)
	lw	$fp,16($sp)
	addu	$sp,$sp,24
	j	$31
	.end	typecheck_STRING_RELOP
	.align	2
	.globl	typecheck_STRING_DOT
	.ent	typecheck_STRING_DOT
typecheck_STRING_DOT:
	.frame	$fp,24,$31		# vars= 0, regs= 2/0, args= 16, extra= 0
	.mask	0xc0000000,-4
	.fmask	0x00000000,0
	subu	$sp,$sp,24
	sw	$31,20($sp)
	sw	$fp,16($sp)
	move	$fp,$sp
	sw	$4,24($fp)
	sw	$5,28($fp)
	lw	$4,24($fp)
	lw	$5,28($fp)
	la	$6,op_STRING_DOT
	jal	typecheck_GENERIC_STRING_3OP
	move	$sp,$fp
	lw	$31,20($sp)
	lw	$fp,16($sp)
	addu	$sp,$sp,24
	j	$31
	.end	typecheck_STRING_DOT
	.align	2
	.globl	typecheck_STRING_REPEAT
	.ent	typecheck_STRING_REPEAT
typecheck_STRING_REPEAT:
	.frame	$fp,32,$31		# vars= 8, regs= 2/0, args= 16, extra= 0
	.mask	0xc0000000,-4
	.fmask	0x00000000,0
	subu	$sp,$sp,32
	sw	$31,28($sp)
	sw	$fp,24($sp)
	move	$fp,$sp
	sw	$4,32($fp)
	sw	$5,36($fp)
	lw	$2,32($fp)
	sw	$2,16($fp)
	lw	$2,36($fp)
	sw	$2,20($fp)
	la	$2,dummyFunc
	sw	$2,OP1_TYPECAST
	la	$2,dummyFunc
	sw	$2,OP2_TYPECAST
	la	$2,op_STRING_REPEAT
	sw	$2,OPCONTROL
	lw	$3,16($fp)
	li	$2,2			# 0x2
	beq	$3,$2,$L113
	lw	$3,16($fp)
	li	$2,1			# 0x1
	beq	$3,$2,$L113
	lw	$3,20($fp)
	li	$2,2			# 0x2
	beq	$3,$2,$L113
	lw	$3,20($fp)
	li	$2,1			# 0x1
	beq	$3,$2,$L113
	la	$4,$LC7
	jal	PrintfNormal
	jal	Exit
$L113:
	lw	$3,16($fp)
	li	$2,2			# 0x2
	beq	$3,$2,$L114
	lw	$3,16($fp)
	li	$2,1			# 0x1
	beq	$3,$2,$L114
	lw	$2,16($fp)
	sll	$3,$2,2
	la	$2,typeMaps
	addu	$2,$3,$2
	la	$4,$LC8
	lw	$5,0($2)
	jal	PrintfNormal
	jal	Exit
$L114:
	lw	$3,20($fp)
	li	$2,2			# 0x2
	beq	$3,$2,$L115
	lw	$3,20($fp)
	li	$2,1			# 0x1
	beq	$3,$2,$L115
	lw	$2,20($fp)
	sll	$3,$2,2
	la	$2,typeMaps
	addu	$2,$3,$2
	la	$4,$LC8
	lw	$5,0($2)
	jal	PrintfNormal
	jal	Exit
$L115:
	lw	$3,16($fp)
	li	$2,2			# 0x2
	bne	$3,$2,$L116
	la	$2,convertINT_TO_STRING
	sw	$2,OP1_TYPECAST
$L116:
	lw	$3,20($fp)
	li	$2,1			# 0x1
	bne	$3,$2,$L117
	la	$2,convertSTRING_TO_INT
	sw	$2,OP2_TYPECAST
$L117:
	li	$2,1			# 0x1
	move	$sp,$fp
	lw	$31,28($sp)
	lw	$fp,24($sp)
	addu	$sp,$sp,32
	j	$31
	.end	typecheck_STRING_REPEAT
	.rdata
	.align	2
$LC9:
	.ascii	"Hash index needs to be a STRING, not %s\n\000"
	.text
	.align	2
	.globl	typecheck_HASH_INDEX_CHECK
	.ent	typecheck_HASH_INDEX_CHECK
typecheck_HASH_INDEX_CHECK:
	.frame	$fp,32,$31		# vars= 8, regs= 2/0, args= 16, extra= 0
	.mask	0xc0000000,-4
	.fmask	0x00000000,0
	subu	$sp,$sp,32
	sw	$31,28($sp)
	sw	$fp,24($sp)
	move	$fp,$sp
	sw	$4,32($fp)
	lw	$2,32($fp)
	sw	$2,16($fp)
	lw	$3,16($fp)
	li	$2,1			# 0x1
	beq	$3,$2,$L119
	lw	$2,16($fp)
	sll	$3,$2,2
	la	$2,typeMaps
	addu	$2,$3,$2
	la	$4,$LC9
	lw	$5,0($2)
	jal	PrintfNormal
	jal	Exit
$L119:
	move	$sp,$fp
	lw	$31,28($sp)
	lw	$fp,24($sp)
	addu	$sp,$sp,32
	j	$31
	.end	typecheck_HASH_INDEX_CHECK
	.rdata
	.align	2
$LC10:
	.ascii	"Array index needs to be an INT, not %s\n\000"
	.text
	.align	2
	.globl	typecheck_ARRAY_INDEX_CHECK
	.ent	typecheck_ARRAY_INDEX_CHECK
typecheck_ARRAY_INDEX_CHECK:
	.frame	$fp,32,$31		# vars= 8, regs= 2/0, args= 16, extra= 0
	.mask	0xc0000000,-4
	.fmask	0x00000000,0
	subu	$sp,$sp,32
	sw	$31,28($sp)
	sw	$fp,24($sp)
	move	$fp,$sp
	sw	$4,32($fp)
	lw	$2,32($fp)
	sw	$2,16($fp)
	lw	$3,16($fp)
	li	$2,2			# 0x2
	beq	$3,$2,$L121
	lw	$2,16($fp)
	sll	$3,$2,2
	la	$2,typeMaps
	addu	$2,$3,$2
	la	$4,$LC10
	lw	$5,0($2)
	jal	PrintfNormal
	jal	Exit
$L121:
	move	$sp,$fp
	lw	$31,28($sp)
	lw	$fp,24($sp)
	addu	$sp,$sp,32
	j	$31
	.end	typecheck_ARRAY_INDEX_CHECK
	.rdata
	.align	2
$LC11:
	.ascii	"Need types %s and %s to be equal\n\000"
	.text
	.align	2
	.globl	typecheck_TYPE_EQUAL
	.ent	typecheck_TYPE_EQUAL
typecheck_TYPE_EQUAL:
	.frame	$fp,32,$31		# vars= 8, regs= 2/0, args= 16, extra= 0
	.mask	0xc0000000,-4
	.fmask	0x00000000,0
	subu	$sp,$sp,32
	sw	$31,28($sp)
	sw	$fp,24($sp)
	move	$fp,$sp
	sw	$4,32($fp)
	sw	$5,36($fp)
	lw	$2,32($fp)
	sw	$2,16($fp)
	lw	$2,36($fp)
	sw	$2,20($fp)
	lw	$3,16($fp)
	lw	$2,20($fp)
	beq	$3,$2,$L123
	lw	$2,16($fp)
	sll	$3,$2,2
	la	$2,typeMaps
	addu	$5,$3,$2
	lw	$2,20($fp)
	sll	$3,$2,2
	la	$2,typeMaps
	addu	$2,$3,$2
	la	$4,$LC11
	lw	$5,0($5)
	lw	$6,0($2)
	jal	PrintfNormal
	jal	Exit
$L123:
	move	$sp,$fp
	lw	$31,28($sp)
	lw	$fp,24($sp)
	addu	$sp,$sp,32
	j	$31
	.end	typecheck_TYPE_EQUAL
	.rdata
	.align	2
$LC12:
	.ascii	"Cannot perform the required arithmetic operation between"
	.ascii	" types %s and %s\n\000"
	.text
	.align	2
	.globl	typecheck_GENERIC_INT_3OP
	.ent	typecheck_GENERIC_INT_3OP
typecheck_GENERIC_INT_3OP:
	.frame	$fp,32,$31		# vars= 8, regs= 2/0, args= 16, extra= 0
	.mask	0xc0000000,-4
	.fmask	0x00000000,0
	subu	$sp,$sp,32
	sw	$31,28($sp)
	sw	$fp,24($sp)
	move	$fp,$sp
	sw	$4,32($fp)
	sw	$5,36($fp)
	lw	$2,32($fp)
	sw	$2,16($fp)
	lw	$2,36($fp)
	sw	$2,20($fp)
	lw	$3,16($fp)
	li	$2,2			# 0x2
	bne	$3,$2,$L126
	lw	$3,20($fp)
	li	$2,2			# 0x2
	bne	$3,$2,$L126
	j	$L125
$L126:
	lw	$2,16($fp)
	sll	$3,$2,2
	la	$2,typeMaps
	addu	$5,$3,$2
	lw	$2,20($fp)
	sll	$3,$2,2
	la	$2,typeMaps
	addu	$2,$3,$2
	la	$4,$LC12
	lw	$5,0($5)
	lw	$6,0($2)
	jal	PrintfNormal
	jal	Exit
$L125:
	move	$sp,$fp
	lw	$31,28($sp)
	lw	$fp,24($sp)
	addu	$sp,$sp,32
	j	$31
	.end	typecheck_GENERIC_INT_3OP
