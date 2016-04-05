	.file	1 "arraylib.c"
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
	li	$4,4			# 0x4
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
	sll	$2,$2,3
	addu	$2,$2,8
	move	$4,$2
	jal	alloc
	sw	$2,16($fp)
	lw	$2,16($fp)
	beq	$2,$0,$L7
	sw	$0,20($fp)
$L9:
	lw	$2,32($fp)
	lw	$3,20($fp)
	lw	$2,0($2)
	slt	$2,$3,$2
	bne	$2,$0,$L12
	j	$L10
$L12:
	lw	$2,20($fp)
	sll	$3,$2,2
	lw	$2,16($fp)
	addu	$5,$3,$2
	lw	$4,32($fp)
	lw	$2,20($fp)
	sll	$3,$2,2
	lw	$2,4($4)
	addu	$2,$3,$2
	lw	$2,0($2)
	sw	$2,0($5)
	lw	$2,20($fp)
	addu	$2,$2,1
	sw	$2,20($fp)
	j	$L9
$L10:
	lw	$3,32($fp)
	lw	$2,36($fp)
	sll	$2,$2,1
	addu	$2,$2,2
	sw	$2,0($3)
	lw	$3,32($fp)
	lw	$2,16($fp)
	sw	$2,4($3)
$L7:
	lw	$4,32($fp)
	lw	$2,36($fp)
	sll	$3,$2,2
	lw	$2,4($4)
	addu	$2,$3,$2
	move	$sp,$fp
	lw	$31,28($sp)
	lw	$fp,24($sp)
	addu	$sp,$sp,32
	j	$31
	.end	accessIndex
