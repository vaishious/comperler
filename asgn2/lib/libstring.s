	.file	1 "libstring.c"
	.text
	.align	2
	.globl	strCmp
	.ent	strCmp
strCmp:
	.frame	$fp,16,$31		# vars= 8, regs= 1/0, args= 0, extra= 0
	.mask	0x40000000,-8
	.fmask	0x00000000,0
	subu	$sp,$sp,16
	sw	$fp,8($sp)
	move	$fp,$sp
	sw	$4,16($fp)
	sw	$5,20($fp)
$L2:
	lw	$2,16($fp)
	lw	$3,20($fp)
	lb	$4,0($2)
	lb	$2,0($3)
	bne	$4,$2,$L3
	lw	$2,16($fp)
	lb	$2,0($2)
	bne	$2,$0,$L4
	j	$L3
$L4:
	lw	$2,16($fp)
	addu	$2,$2,1
	sw	$2,16($fp)
	lw	$2,20($fp)
	addu	$2,$2,1
	sw	$2,20($fp)
	j	$L2
$L3:
	lw	$2,16($fp)
	lw	$3,20($fp)
	lb	$4,0($2)
	lb	$2,0($3)
	slt	$2,$2,$4
	beq	$2,$0,$L6
	li	$2,1			# 0x1
	sw	$2,0($fp)
	j	$L1
$L6:
	lw	$2,16($fp)
	lw	$3,20($fp)
	lb	$4,0($2)
	lb	$2,0($3)
	slt	$2,$4,$2
	beq	$2,$0,$L7
	li	$2,-1			# 0xffffffffffffffff
	sw	$2,0($fp)
	j	$L1
$L7:
	sw	$0,0($fp)
$L1:
	lw	$2,0($fp)
	move	$sp,$fp
	lw	$fp,8($sp)
	addu	$sp,$sp,16
	j	$31
	.end	strCmp
