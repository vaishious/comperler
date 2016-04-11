	.file	1 "typechecking.c"
	.text
	.align	2
	.globl	typecheck_PLUS
	.ent	typecheck_PLUS
typecheck_PLUS:
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
	bne	$3,$2,$L3
	lw	$3,16($fp)
	li	$2,2			# 0x2
	bne	$3,$2,$L3
	j	$L2
$L3:
	la	$4,TYPE_ERROR_PLUS
	jal	PrintString
 #APP
	
                li $v0, 10
                syscall
            
 #NO_APP
$L2:
	move	$sp,$fp
	lw	$31,28($sp)
	lw	$fp,24($sp)
	addu	$sp,$sp,32
	j	$31
	.end	typecheck_PLUS
