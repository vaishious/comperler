	.file	1 "../asgn2/lib/hashlib.c"
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
$L3:
	lw	$3,16($fp)
	lw	$2,0($fp)
	addu	$2,$3,$2
	lb	$2,0($2)
	bne	$2,$0,$L6
	lw	$3,20($fp)
	lw	$2,0($fp)
	addu	$2,$3,$2
	lb	$2,0($2)
	bne	$2,$0,$L6
	j	$L4
$L6:
	lw	$3,16($fp)
	lw	$2,0($fp)
	addu	$4,$3,$2
	lw	$3,20($fp)
	lw	$2,0($fp)
	addu	$2,$3,$2
	lb	$3,0($4)
	lb	$2,0($2)
	slt	$2,$2,$3
	beq	$2,$0,$L7
	li	$2,1			# 0x1
	sw	$2,4($fp)
	j	$L2
$L7:
	lw	$3,16($fp)
	lw	$2,0($fp)
	addu	$4,$3,$2
	lw	$3,20($fp)
	lw	$2,0($fp)
	addu	$2,$3,$2
	lb	$3,0($4)
	lb	$2,0($2)
	slt	$2,$3,$2
	beq	$2,$0,$L5
	li	$2,-1			# 0xffffffffffffffff
	sw	$2,4($fp)
	j	$L2
$L5:
	lw	$2,0($fp)
	addu	$2,$2,1
	sw	$2,0($fp)
	j	$L3
$L4:
	sw	$0,4($fp)
$L2:
	lw	$2,4($fp)
	move	$sp,$fp
	lw	$fp,8($sp)
	addu	$sp,$sp,16
	j	$31
	.end	strCmp
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
$L11:
	lw	$2,20($fp)
	bne	$2,$0,$L13
	j	$L12
$L13:
	lw	$2,20($fp)
	lw	$4,0($2)
	lw	$5,36($fp)
	jal	strCmp
	bne	$2,$0,$L14
	j	$L12
$L14:
	lw	$2,20($fp)
	lw	$2,8($2)
	sw	$2,20($fp)
	j	$L11
$L12:
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
	lw	$4,32($fp)
	lw	$5,36($fp)
	jal	findMatch
	sw	$2,16($fp)
	lw	$2,16($fp)
	beq	$2,$0,$L17
	lw	$3,16($fp)
	lw	$2,36($fp)
	sw	$2,0($3)
	lw	$3,16($fp)
	lw	$2,40($fp)
	sw	$2,4($3)
	j	$L16
$L17:
	li	$4,12			# 0xc
	jal	alloc
	sw	$2,16($fp)
	lw	$3,16($fp)
	lw	$2,36($fp)
	sw	$2,0($3)
	lw	$3,16($fp)
	lw	$2,40($fp)
	sw	$2,4($3)
	lw	$2,32($fp)
	lw	$2,8($2)
	bne	$2,$0,$L18
	lw	$4,32($fp)
	lw	$3,32($fp)
	lw	$2,16($fp)
	sw	$2,4($3)
	sw	$2,0($4)
	j	$L19
$L18:
	lw	$2,32($fp)
	lw	$3,4($2)
	lw	$2,16($fp)
	sw	$2,8($3)
	lw	$3,32($fp)
	lw	$2,16($fp)
	sw	$2,4($3)
$L19:
	lw	$3,32($fp)
	lw	$2,32($fp)
	lw	$2,8($2)
	addu	$2,$2,1
	sw	$2,8($3)
$L16:
	move	$2,$0
	move	$sp,$fp
	lw	$31,28($sp)
	lw	$fp,24($sp)
	addu	$sp,$sp,32
	j	$31
	.end	addElement
	.align	2
	.globl	getValue
	.ent	getValue
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
	lw	$4,32($fp)
	lw	$5,36($fp)
	jal	findMatch
	sw	$2,16($fp)
	lw	$2,16($fp)
	beq	$2,$0,$L21
	lw	$2,16($fp)
	lw	$2,4($2)
	sw	$2,20($fp)
	j	$L20
$L21:
	sw	$0,20($fp)
$L20:
	lw	$2,20($fp)
	move	$sp,$fp
	lw	$31,28($sp)
	lw	$fp,24($sp)
	addu	$sp,$sp,32
	j	$31
	.end	getValue
