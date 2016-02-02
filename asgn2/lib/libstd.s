	.file	1 "libstd.c"
	.text
	.align	2
	.globl	alloc
	.ent	alloc
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
	.sdata
	.align	2
$LC0:
	.ascii	"%s : %s\000"
	.text
	.align	2
	.globl	ExitWithMessage
	.ent	ExitWithMessage
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
	beq	$2,$0,$L3
	la	$4,$LC0
	lw	$5,24($fp)
	lw	$6,28($fp)
	jal	Printf
	j	$L4
$L3:
	lw	$4,24($fp)
	jal	PrintString
$L4:
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
