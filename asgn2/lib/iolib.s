	.file	1 "iolib.c"
	.text
	.align	2
	.globl	PrintInt
	.ent	PrintInt
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
	.align	2
	.globl	PrintString
	.ent	PrintString
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
	.align	2
	.globl	PrintChar
	.ent	PrintChar
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
	.align	2
	.globl	ReadInt
	.ent	ReadInt
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
	.align	2
	.globl	ReadChar
	.ent	ReadChar
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
	.align	2
	.globl	ReadString
	.ent	ReadString
ReadString:
	.frame	$fp,8,$31		# vars= 0, regs= 1/0, args= 0, extra= 0
	.mask	0x40000000,-8
	.fmask	0x00000000,0
	subu	$sp,$sp,8
	sw	$fp,0($sp)
	move	$fp,$sp
	sw	$4,8($fp)
	sw	$5,12($fp)
	lw	$3,8($fp)
	lw	$2,12($fp)
 #APP
	
            move $a0, $3
            move $a1, $2
            li   $v0, 8
            syscall
        
 #NO_APP
	move	$sp,$fp
	lw	$fp,0($sp)
	addu	$sp,$sp,8
	j	$31
	.end	ReadString
	.align	2
	.globl	Printf
	.ent	Printf
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
	.align	2
	.globl	Scanf
	.ent	Scanf
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
	bne	$3,$2,$L26
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
	j	$L23
$L26:
	lw	$2,40($fp)
	lb	$3,0($2)
	li	$2,115			# 0x73
	bne	$3,$2,$L19
	lw	$2,16($fp)
	lw	$2,0($2)
	lw	$2,0($2)
	sw	$2,28($fp)
	lw	$4,28($fp)
	li	$5,1000			# 0x3e8
	jal	ReadString
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
