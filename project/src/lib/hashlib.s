	.file	1 "hashlib.c"
	.text
	.align	2
	.globl	findMatch
	.ent	findMatch
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
	lw	$2,32($fp)
	lw	$2,0($2)
	sw	$2,20($fp)
	sw	$0,16($fp)
$L2:
	lw	$2,32($fp)
	lw	$3,16($fp)
	lw	$2,8($2)
	slt	$2,$3,$2
	bne	$2,$0,$L5
	j	$L3
$L5:
	lw	$2,20($fp)
	lw	$4,0($2)
	lw	$5,36($fp)
	jal	strCmp
	bne	$2,$0,$L6
	j	$L3
$L6:
	lw	$2,20($fp)
	lw	$2,12($2)
	sw	$2,20($fp)
	lw	$2,16($fp)
	addu	$2,$2,1
	sw	$2,16($fp)
	j	$L2
$L3:
	lw	$2,20($fp)
	move	$sp,$fp
	lw	$31,28($sp)
	lw	$fp,24($sp)
	addu	$sp,$sp,32
	j	$31
	.end	findMatch
	.align	2
	.globl	initHash
	.ent	initHash
initHash:
	.frame	$fp,32,$31		# vars= 8, regs= 2/0, args= 16, extra= 0
	.mask	0xc0000000,-4
	.fmask	0x00000000,0
	subu	$sp,$sp,32
	sw	$31,28($sp)
	sw	$fp,24($sp)
	move	$fp,$sp
	li	$4,12			# 0xc
	jal	alloc
	sw	$2,16($fp)
	lw	$3,16($fp)
	lw	$2,16($fp)
	sw	$0,4($2)
	sw	$0,0($3)
	lw	$2,16($fp)
	sw	$0,8($2)
	lw	$2,16($fp)
	move	$sp,$fp
	lw	$31,28($sp)
	lw	$fp,24($sp)
	addu	$sp,$sp,32
	j	$31
	.end	initHash
	.align	2
	.globl	addElementType
	.ent	addElementType
addElementType:
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
	lw	$2,OP1_TYPECAST
	lw	$4,36($fp)
	jal	$31,$2
	sw	$2,16($fp)
	lw	$4,32($fp)
	lw	$5,16($fp)
	jal	findMatch
	sw	$2,20($fp)
	lw	$2,20($fp)
	beq	$2,$0,$L9
	lw	$3,20($fp)
	lw	$2,16($fp)
	sw	$2,0($3)
	lw	$3,20($fp)
	lw	$2,40($fp)
	sw	$2,8($3)
	j	$L8
$L9:
	li	$4,16			# 0x10
	jal	alloc
	sw	$2,20($fp)
	lw	$3,20($fp)
	lw	$2,16($fp)
	sw	$2,0($3)
	lw	$3,20($fp)
	lw	$2,40($fp)
	sw	$2,8($3)
	lw	$2,20($fp)
	sw	$0,12($2)
	lw	$2,32($fp)
	lw	$2,8($2)
	bne	$2,$0,$L10
	lw	$4,32($fp)
	lw	$3,32($fp)
	lw	$2,20($fp)
	sw	$2,4($3)
	sw	$2,0($4)
	j	$L11
$L10:
	lw	$2,32($fp)
	lw	$3,4($2)
	lw	$2,20($fp)
	sw	$2,12($3)
	lw	$3,32($fp)
	lw	$2,20($fp)
	sw	$2,4($3)
$L11:
	lw	$3,32($fp)
	lw	$2,32($fp)
	lw	$2,8($2)
	addu	$2,$2,1
	sw	$2,8($3)
$L8:
	move	$2,$0
	move	$sp,$fp
	lw	$31,28($sp)
	lw	$fp,24($sp)
	addu	$sp,$sp,32
	j	$31
	.end	addElementType
	.align	2
	.globl	addElement
	.ent	addElement
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
	lw	$2,OP1_TYPECAST
	lw	$4,36($fp)
	jal	$31,$2
	sw	$2,16($fp)
	lw	$4,32($fp)
	lw	$5,16($fp)
	jal	findMatch
	sw	$2,20($fp)
	lw	$2,20($fp)
	beq	$2,$0,$L13
	lw	$3,20($fp)
	lw	$2,16($fp)
	sw	$2,0($3)
	lw	$3,20($fp)
	lw	$2,40($fp)
	sw	$2,4($3)
	j	$L12
$L13:
	li	$4,16			# 0x10
	jal	alloc
	sw	$2,20($fp)
	lw	$3,20($fp)
	lw	$2,16($fp)
	sw	$2,0($3)
	lw	$3,20($fp)
	lw	$2,40($fp)
	sw	$2,4($3)
	lw	$2,20($fp)
	sw	$0,12($2)
	lw	$2,32($fp)
	lw	$2,8($2)
	bne	$2,$0,$L14
	lw	$4,32($fp)
	lw	$3,32($fp)
	lw	$2,20($fp)
	sw	$2,4($3)
	sw	$2,0($4)
	j	$L15
$L14:
	lw	$2,32($fp)
	lw	$3,4($2)
	lw	$2,20($fp)
	sw	$2,12($3)
	lw	$3,32($fp)
	lw	$2,20($fp)
	sw	$2,4($3)
$L15:
	lw	$3,32($fp)
	lw	$2,32($fp)
	lw	$2,8($2)
	addu	$2,$2,1
	sw	$2,8($3)
$L12:
	move	$2,$0
	move	$sp,$fp
	lw	$31,28($sp)
	lw	$fp,24($sp)
	addu	$sp,$sp,32
	j	$31
	.end	addElement
	.align	2
	.globl	getHashValue
	.ent	getHashValue
getHashValue:
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
	lw	$4,44($fp)
	jal	$31,$2
	sw	$2,16($fp)
	lw	$4,40($fp)
	lw	$5,16($fp)
	jal	findMatch
	sw	$2,20($fp)
	lw	$2,20($fp)
	beq	$2,$0,$L17
	lw	$2,20($fp)
	lw	$2,4($2)
	sw	$2,24($fp)
	j	$L16
$L17:
	lw	$4,40($fp)
	lw	$5,16($fp)
	move	$6,$0
	jal	addElement
	lw	$4,40($fp)
	lw	$5,16($fp)
	li	$6,2			# 0x2
	jal	addElementType
	lw	$4,40($fp)
	lw	$5,16($fp)
	jal	findMatch
	sw	$2,20($fp)
	lw	$2,20($fp)
	beq	$2,$0,$L18
	lw	$2,20($fp)
	lw	$2,4($2)
	sw	$2,24($fp)
	j	$L16
$L18:
$L16:
	lw	$2,24($fp)
	move	$sp,$fp
	lw	$31,36($sp)
	lw	$fp,32($sp)
	addu	$sp,$sp,40
	j	$31
	.end	getHashValue
	.align	2
	.globl	getHashValueType
	.ent	getHashValueType
getHashValueType:
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
	lw	$4,44($fp)
	jal	$31,$2
	sw	$2,16($fp)
	lw	$4,40($fp)
	lw	$5,16($fp)
	jal	findMatch
	sw	$2,20($fp)
	lw	$2,20($fp)
	beq	$2,$0,$L20
	lw	$2,20($fp)
	lw	$2,8($2)
	sw	$2,24($fp)
	j	$L19
$L20:
	lw	$4,40($fp)
	lw	$5,16($fp)
	move	$6,$0
	jal	addElement
	lw	$4,40($fp)
	lw	$5,16($fp)
	li	$6,2			# 0x2
	jal	addElementType
	lw	$4,40($fp)
	lw	$5,16($fp)
	jal	findMatch
	sw	$2,20($fp)
	lw	$2,20($fp)
	beq	$2,$0,$L21
	lw	$2,20($fp)
	lw	$2,8($2)
	sw	$2,24($fp)
	j	$L19
$L21:
$L19:
	lw	$2,24($fp)
	move	$sp,$fp
	lw	$31,36($sp)
	lw	$fp,32($sp)
	addu	$sp,$sp,40
	j	$31
	.end	getHashValueType
	.align	2
	.globl	getFirstKey
	.ent	getFirstKey
getFirstKey:
	.frame	$fp,16,$31		# vars= 8, regs= 1/0, args= 0, extra= 0
	.mask	0x40000000,-8
	.fmask	0x00000000,0
	subu	$sp,$sp,16
	sw	$fp,8($sp)
	move	$fp,$sp
	sw	$4,16($fp)
	lw	$2,16($fp)
	lw	$2,0($2)
	sw	$2,0($fp)
	lw	$2,0($fp)
	bne	$2,$0,$L23
	sw	$0,4($fp)
	j	$L22
$L23:
	lw	$2,0($fp)
	lw	$2,0($2)
	sw	$2,4($fp)
$L22:
	lw	$2,4($fp)
	move	$sp,$fp
	lw	$fp,8($sp)
	addu	$sp,$sp,16
	j	$31
	.end	getFirstKey
	.align	2
	.globl	getNextKey
	.ent	getNextKey
getNextKey:
	.frame	$fp,32,$31		# vars= 8, regs= 2/0, args= 16, extra= 0
	.mask	0xc0000000,-4
	.fmask	0x00000000,0
	subu	$sp,$sp,32
	sw	$31,28($sp)
	sw	$fp,24($sp)
	move	$fp,$sp
	sw	$4,32($fp)
	sw	$5,36($fp)
	lw	$4,32($fp)
	lw	$5,36($fp)
	jal	findMatch
	sw	$2,16($fp)
	lw	$2,32($fp)
	lw	$3,16($fp)
	lw	$2,4($2)
	bne	$3,$2,$L26
	sw	$0,20($fp)
	j	$L25
$L26:
	lw	$2,16($fp)
	lw	$2,12($2)
	lw	$2,0($2)
	sw	$2,20($fp)
$L25:
	lw	$2,20($fp)
	move	$sp,$fp
	lw	$31,28($sp)
	lw	$fp,24($sp)
	addu	$sp,$sp,32
	j	$31
	.end	getNextKey
