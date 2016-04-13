	.file	1 "dynlib.c"
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
	li	$4,12			# 0xc
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
	lw	$3,16($fp)
	li	$2,-1			# 0xffffffffffffffff
	sw	$2,8($3)
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
	lw	$2,8($2)
	addu	$2,$2,1
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
$L7:
	lw	$2,32($fp)
	lw	$3,36($fp)
	lw	$2,8($2)
	slt	$2,$2,$3
	beq	$2,$0,$L12
	lw	$3,32($fp)
	lw	$2,36($fp)
	sw	$2,8($3)
$L12:
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
	lw	$2,32($fp)
	lw	$3,36($fp)
	lw	$2,8($2)
	slt	$2,$2,$3
	beq	$2,$0,$L19
	lw	$3,32($fp)
	lw	$2,36($fp)
	sw	$2,8($3)
$L19:
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
	bne	$3,$2,$L22
	li	$2,1			# 0x1
	sw	$2,4($fp)
	lw	$2,0($fp)
	addu	$2,$2,1
	sw	$2,0($fp)
	j	$L23
$L22:
	lw	$2,0($fp)
	lb	$3,0($2)
	li	$2,43			# 0x2b
	bne	$3,$2,$L23
	sw	$0,4($fp)
	lw	$2,0($fp)
	addu	$2,$2,1
	sw	$2,0($fp)
$L23:
	.set	noreorder
	nop
	.set	reorder
$L25:
	lw	$2,0($fp)
	lb	$2,0($2)
	bne	$2,$0,$L27
	j	$L26
$L27:
	lw	$2,0($fp)
	lb	$2,0($2)
	slt	$2,$2,58
	beq	$2,$0,$L29
	lw	$2,0($fp)
	lb	$2,0($2)
	slt	$2,$2,48
	bne	$2,$0,$L29
	j	$L28
$L29:
	lw	$3,4($fp)
	li	$2,1			# 0x1
	bne	$3,$2,$L30
	lw	$2,8($fp)
	subu	$2,$0,$2
	sw	$2,8($fp)
$L30:
	lw	$2,8($fp)
	sw	$2,12($fp)
	j	$L21
$L28:
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
	j	$L25
$L26:
	lw	$3,4($fp)
	li	$2,1			# 0x1
	bne	$3,$2,$L31
	lw	$2,8($fp)
	subu	$2,$0,$2
	sw	$2,8($fp)
$L31:
	lw	$2,8($fp)
	sw	$2,12($fp)
$L21:
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
$L33:
	lw	$2,20($fp)
	bgtz	$2,$L35
	j	$L34
$L35:
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
	j	$L33
$L34:
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
$L36:
	lw	$2,20($fp)
	bgtz	$2,$L38
	j	$L37
$L38:
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
	j	$L36
$L37:
	lw	$2,24($fp)
	move	$sp,$fp
	lw	$31,36($sp)
	lw	$fp,32($sp)
	addu	$sp,$sp,40
	j	$31
	.end	convertINT_TO_STRING
	.align	2
	.globl	op_UNARY_PLUS
	.ent	op_UNARY_PLUS
op_UNARY_PLUS:
	.frame	$fp,24,$31		# vars= 0, regs= 2/0, args= 16, extra= 0
	.mask	0xc0000000,-4
	.fmask	0x00000000,0
	subu	$sp,$sp,24
	sw	$31,20($sp)
	sw	$fp,16($sp)
	move	$fp,$sp
	sw	$4,24($fp)
	lw	$2,OP1_TYPECAST
	lw	$4,24($fp)
	jal	$31,$2
	sw	$2,24($fp)
	lw	$2,24($fp)
	move	$sp,$fp
	lw	$31,20($sp)
	lw	$fp,16($sp)
	addu	$sp,$sp,24
	j	$31
	.end	op_UNARY_PLUS
	.align	2
	.globl	op_UNARY_MINUS
	.ent	op_UNARY_MINUS
op_UNARY_MINUS:
	.frame	$fp,32,$31		# vars= 8, regs= 2/0, args= 16, extra= 0
	.mask	0xc0000000,-4
	.fmask	0x00000000,0
	subu	$sp,$sp,32
	sw	$31,28($sp)
	sw	$fp,24($sp)
	move	$fp,$sp
	sw	$4,32($fp)
	lw	$2,OP1_TYPECAST
	lw	$4,32($fp)
	jal	$31,$2
	sw	$2,32($fp)
	lw	$2,32($fp)
	sw	$2,16($fp)
	lw	$3,16($fp)
	move	$2,$0
	subu	$2,$2,$3
	move	$sp,$fp
	lw	$31,28($sp)
	lw	$fp,24($sp)
	addu	$sp,$sp,32
	j	$31
	.end	op_UNARY_MINUS
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
$L47:
	lw	$3,16($fp)
	lw	$2,24($fp)
	addu	$2,$3,$2
	lb	$2,0($2)
	bne	$2,$0,$L50
	lw	$3,20($fp)
	lw	$2,24($fp)
	addu	$2,$3,$2
	lb	$2,0($2)
	bne	$2,$0,$L50
	j	$L48
$L50:
	lw	$3,16($fp)
	lw	$2,24($fp)
	addu	$4,$3,$2
	lw	$3,20($fp)
	lw	$2,24($fp)
	addu	$2,$3,$2
	lb	$3,0($4)
	lb	$2,0($2)
	slt	$2,$2,$3
	beq	$2,$0,$L51
	li	$2,1			# 0x1
	sw	$2,28($fp)
	j	$L46
$L51:
	lw	$3,16($fp)
	lw	$2,24($fp)
	addu	$4,$3,$2
	lw	$3,20($fp)
	lw	$2,24($fp)
	addu	$2,$3,$2
	lb	$3,0($4)
	lb	$2,0($2)
	slt	$2,$3,$2
	beq	$2,$0,$L49
	li	$2,-1			# 0xffffffffffffffff
	sw	$2,28($fp)
	j	$L46
$L49:
	lw	$2,24($fp)
	addu	$2,$2,1
	sw	$2,24($fp)
	j	$L47
$L48:
	sw	$0,28($fp)
$L46:
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
$L55:
	lw	$3,16($fp)
	lw	$2,24($fp)
	addu	$2,$3,$2
	lb	$2,0($2)
	bne	$2,$0,$L57
	j	$L56
$L57:
	lw	$2,24($fp)
	addu	$2,$2,1
	sw	$2,24($fp)
	j	$L55
$L56:
	sw	$0,28($fp)
$L59:
	lw	$3,20($fp)
	lw	$2,28($fp)
	addu	$2,$3,$2
	lb	$2,0($2)
	bne	$2,$0,$L61
	j	$L60
$L61:
	lw	$2,28($fp)
	addu	$2,$2,1
	sw	$2,28($fp)
	j	$L59
$L60:
	lw	$3,24($fp)
	lw	$2,28($fp)
	addu	$2,$3,$2
	addu	$2,$2,1
	move	$4,$2
	jal	alloc
	sw	$2,32($fp)
	sw	$0,36($fp)
$L63:
	lw	$2,36($fp)
	lw	$3,24($fp)
	slt	$2,$2,$3
	bne	$2,$0,$L66
	j	$L64
$L66:
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
	j	$L63
$L64:
	sw	$0,36($fp)
$L67:
	lw	$2,36($fp)
	lw	$3,28($fp)
	slt	$2,$2,$3
	bne	$2,$0,$L70
	j	$L68
$L70:
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
	j	$L67
$L68:
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
	bgtz	$2,$L72
	li	$4,1			# 0x1
	jal	alloc
	sw	$2,24($fp)
	lw	$2,24($fp)
	sb	$0,0($2)
	lw	$2,24($fp)
	sw	$2,40($fp)
	j	$L71
$L72:
	sw	$0,24($fp)
	sw	$0,24($fp)
$L73:
	lw	$3,16($fp)
	lw	$2,24($fp)
	addu	$2,$3,$2
	lb	$2,0($2)
	bne	$2,$0,$L75
	j	$L74
$L75:
	lw	$2,24($fp)
	addu	$2,$2,1
	sw	$2,24($fp)
	j	$L73
$L74:
	lw	$3,24($fp)
	lw	$2,20($fp)
	mult	$3,$2
	mflo	$2
	addu	$2,$2,1
	move	$4,$2
	jal	alloc
	sw	$2,28($fp)
	sw	$0,32($fp)
$L77:
	lw	$2,32($fp)
	lw	$3,20($fp)
	slt	$2,$2,$3
	bne	$2,$0,$L80
	j	$L78
$L80:
	sw	$0,36($fp)
$L81:
	lw	$2,36($fp)
	lw	$3,24($fp)
	slt	$2,$2,$3
	bne	$2,$0,$L84
	j	$L79
$L84:
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
	j	$L81
$L79:
	lw	$2,32($fp)
	addu	$2,$2,1
	sw	$2,32($fp)
	j	$L77
$L78:
	lw	$3,20($fp)
	lw	$2,24($fp)
	mult	$3,$2
	mflo	$3
	lw	$2,28($fp)
	addu	$2,$3,$2
	sb	$0,0($2)
	lw	$2,28($fp)
	sw	$2,40($fp)
$L71:
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
$L86:
	lw	$2,36($fp)
	lw	$3,24($fp)
	slt	$2,$2,$3
	bne	$2,$0,$L89
	j	$L87
$L89:
	lw	$4,32($fp)
	lw	$5,36($fp)
	jal	accessIndex
	move	$16,$2
	lw	$4,16($fp)
	lw	$5,36($fp)
	jal	accessIndex
	lw	$2,0($2)
	sw	$2,0($16)
	lw	$4,32($fp)
	lw	$5,36($fp)
	jal	accessIndexType
	move	$16,$2
	lw	$4,16($fp)
	lw	$5,36($fp)
	jal	accessIndexType
	lw	$2,0($2)
	sw	$2,0($16)
	lw	$2,36($fp)
	addu	$2,$2,1
	sw	$2,36($fp)
	j	$L86
$L87:
	sw	$0,36($fp)
$L90:
	lw	$2,36($fp)
	lw	$3,28($fp)
	slt	$2,$2,$3
	bne	$2,$0,$L93
	j	$L91
$L93:
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
	lw	$3,24($fp)
	lw	$2,36($fp)
	addu	$2,$3,$2
	lw	$4,32($fp)
	move	$5,$2
	jal	accessIndexType
	move	$16,$2
	lw	$4,20($fp)
	lw	$5,36($fp)
	jal	accessIndexType
	lw	$2,0($2)
	sw	$2,0($16)
	lw	$2,36($fp)
	addu	$2,$2,1
	sw	$2,36($fp)
	j	$L90
$L91:
	lw	$2,32($fp)
	move	$sp,$fp
	lw	$31,48($sp)
	lw	$fp,44($sp)
	lw	$16,40($sp)
	addu	$sp,$sp,56
	j	$31
	.end	op_ARRAY_CONCAT
