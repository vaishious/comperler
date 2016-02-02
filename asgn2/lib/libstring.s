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
	sw	$0,0($fp)
$L2:
	lw	$3,16($fp)
	lw	$2,0($fp)
	addu	$2,$3,$2
	lb	$2,0($2)
	bne	$2,$0,$L5
	lw	$3,20($fp)
	lw	$2,0($fp)
	addu	$2,$3,$2
	lb	$2,0($2)
	bne	$2,$0,$L5
	j	$L3
$L5:
	lw	$3,16($fp)
	lw	$2,0($fp)
	addu	$4,$3,$2
	lw	$3,20($fp)
	lw	$2,0($fp)
	addu	$2,$3,$2
	lb	$3,0($4)
	lb	$2,0($2)
	slt	$2,$2,$3
	beq	$2,$0,$L6
	li	$2,1			# 0x1
	sw	$2,4($fp)
	j	$L1
$L6:
	lw	$3,16($fp)
	lw	$2,0($fp)
	addu	$4,$3,$2
	lw	$3,20($fp)
	lw	$2,0($fp)
	addu	$2,$3,$2
	lb	$3,0($4)
	lb	$2,0($2)
	slt	$2,$3,$2
	beq	$2,$0,$L4
	li	$2,-1			# 0xffffffffffffffff
	sw	$2,4($fp)
	j	$L1
$L4:
	lw	$2,0($fp)
	addu	$2,$2,1
	sw	$2,0($fp)
	j	$L2
$L3:
	sw	$0,4($fp)
$L1:
	lw	$2,4($fp)
	move	$sp,$fp
	lw	$fp,8($sp)
	addu	$sp,$sp,16
	j	$31
	.end	strCmp
