	.file	1 "typechecking.c"
	.text
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
	bne	$3,$2,$L3
	li	$2,1			# 0x1
	sw	$2,4($fp)
	lw	$2,0($fp)
	addu	$2,$2,1
	sw	$2,0($fp)
	j	$L4
$L3:
	lw	$2,0($fp)
	lb	$3,0($2)
	li	$2,43			# 0x2b
	bne	$3,$2,$L4
	sw	$0,4($fp)
	lw	$2,0($fp)
	addu	$2,$2,1
	sw	$2,0($fp)
$L4:
	.set	noreorder
	nop
	.set	reorder
$L6:
	lw	$2,0($fp)
	lb	$2,0($2)
	bne	$2,$0,$L8
	j	$L7
$L8:
	lw	$2,0($fp)
	lb	$2,0($2)
	slt	$2,$2,58
	beq	$2,$0,$L10
	lw	$2,0($fp)
	lb	$2,0($2)
	slt	$2,$2,48
	bne	$2,$0,$L10
	j	$L9
$L10:
	lw	$3,4($fp)
	li	$2,1			# 0x1
	bne	$3,$2,$L11
	lw	$2,8($fp)
	subu	$2,$0,$2
	sw	$2,8($fp)
$L11:
	lw	$2,8($fp)
	sw	$2,12($fp)
	j	$L2
$L9:
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
	j	$L6
$L7:
	lw	$3,4($fp)
	li	$2,1			# 0x1
	bne	$3,$2,$L12
	lw	$2,8($fp)
	subu	$2,$0,$2
	sw	$2,8($fp)
$L12:
	lw	$2,8($fp)
	sw	$2,12($fp)
$L2:
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
$L14:
	lw	$2,20($fp)
	bgtz	$2,$L16
	j	$L15
$L16:
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
	j	$L14
$L15:
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
$L17:
	lw	$2,20($fp)
	bgtz	$2,$L19
	j	$L18
$L19:
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
	j	$L17
$L18:
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
$L26:
	lw	$3,16($fp)
	lw	$2,24($fp)
	addu	$2,$3,$2
	lb	$2,0($2)
	bne	$2,$0,$L29
	lw	$3,20($fp)
	lw	$2,24($fp)
	addu	$2,$3,$2
	lb	$2,0($2)
	bne	$2,$0,$L29
	j	$L27
$L29:
	lw	$3,16($fp)
	lw	$2,24($fp)
	addu	$4,$3,$2
	lw	$3,20($fp)
	lw	$2,24($fp)
	addu	$2,$3,$2
	lb	$3,0($4)
	lb	$2,0($2)
	slt	$2,$2,$3
	beq	$2,$0,$L30
	li	$2,1			# 0x1
	sw	$2,28($fp)
	j	$L25
$L30:
	lw	$3,16($fp)
	lw	$2,24($fp)
	addu	$4,$3,$2
	lw	$3,20($fp)
	lw	$2,24($fp)
	addu	$2,$3,$2
	lb	$3,0($4)
	lb	$2,0($2)
	slt	$2,$3,$2
	beq	$2,$0,$L28
	li	$2,-1			# 0xffffffffffffffff
	sw	$2,28($fp)
	j	$L25
$L28:
	lw	$2,24($fp)
	addu	$2,$2,1
	sw	$2,24($fp)
	j	$L26
$L27:
	sw	$0,28($fp)
$L25:
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
$L34:
	lw	$3,16($fp)
	lw	$2,24($fp)
	addu	$2,$3,$2
	lb	$2,0($2)
	bne	$2,$0,$L36
	j	$L35
$L36:
	lw	$2,24($fp)
	addu	$2,$2,1
	sw	$2,24($fp)
	j	$L34
$L35:
	sw	$0,28($fp)
$L38:
	lw	$3,20($fp)
	lw	$2,28($fp)
	addu	$2,$3,$2
	lb	$2,0($2)
	bne	$2,$0,$L40
	j	$L39
$L40:
	lw	$2,28($fp)
	addu	$2,$2,1
	sw	$2,28($fp)
	j	$L38
$L39:
	lw	$3,24($fp)
	lw	$2,28($fp)
	addu	$2,$3,$2
	addu	$2,$2,1
	move	$4,$2
	jal	alloc
	sw	$2,32($fp)
	sw	$0,36($fp)
$L42:
	lw	$2,36($fp)
	lw	$3,24($fp)
	slt	$2,$2,$3
	bne	$2,$0,$L45
	j	$L43
$L45:
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
	j	$L42
$L43:
	sw	$0,36($fp)
$L46:
	lw	$2,36($fp)
	lw	$3,28($fp)
	slt	$2,$2,$3
	bne	$2,$0,$L49
	j	$L47
$L49:
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
	j	$L46
$L47:
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
	bgtz	$2,$L51
	li	$4,1			# 0x1
	jal	alloc
	sw	$2,24($fp)
	lw	$2,24($fp)
	sb	$0,0($2)
	lw	$2,24($fp)
	sw	$2,40($fp)
	j	$L50
$L51:
	sw	$0,24($fp)
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
	lw	$3,24($fp)
	lw	$2,20($fp)
	mult	$3,$2
	mflo	$2
	addu	$2,$2,1
	move	$4,$2
	jal	alloc
	sw	$2,28($fp)
	sw	$0,32($fp)
$L56:
	lw	$2,32($fp)
	lw	$3,20($fp)
	slt	$2,$2,$3
	bne	$2,$0,$L59
	j	$L57
$L59:
	sw	$0,36($fp)
$L60:
	lw	$2,36($fp)
	lw	$3,24($fp)
	slt	$2,$2,$3
	bne	$2,$0,$L63
	j	$L58
$L63:
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
	j	$L60
$L58:
	lw	$2,32($fp)
	addu	$2,$2,1
	sw	$2,32($fp)
	j	$L56
$L57:
	lw	$3,20($fp)
	lw	$2,24($fp)
	mult	$3,$2
	mflo	$3
	lw	$2,28($fp)
	addu	$2,$3,$2
	sb	$0,0($2)
	lw	$2,28($fp)
	sw	$2,40($fp)
$L50:
	lw	$2,40($fp)
	move	$sp,$fp
	lw	$31,52($sp)
	lw	$fp,48($sp)
	addu	$sp,$sp,56
	j	$31
	.end	op_STRING_REPEAT
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
	beq	$3,$2,$L66
	lw	$3,16($fp)
	li	$2,1			# 0x1
	beq	$3,$2,$L66
	lw	$3,20($fp)
	li	$2,2			# 0x2
	beq	$3,$2,$L66
	lw	$3,20($fp)
	li	$2,1			# 0x1
	beq	$3,$2,$L66
	la	$4,$LC5
	jal	PrintfNormal
	jal	Exit
$L66:
	lw	$3,16($fp)
	li	$2,2			# 0x2
	beq	$3,$2,$L67
	lw	$3,16($fp)
	li	$2,1			# 0x1
	beq	$3,$2,$L67
	lw	$2,16($fp)
	sll	$3,$2,2
	la	$2,typeMaps
	addu	$2,$3,$2
	la	$4,$LC6
	lw	$5,0($2)
	jal	PrintfNormal
	jal	Exit
$L67:
	lw	$3,20($fp)
	li	$2,2			# 0x2
	beq	$3,$2,$L68
	lw	$3,20($fp)
	li	$2,1			# 0x1
	beq	$3,$2,$L68
	lw	$2,20($fp)
	sll	$3,$2,2
	la	$2,typeMaps
	addu	$2,$3,$2
	la	$4,$LC6
	lw	$5,0($2)
	jal	PrintfNormal
	jal	Exit
$L68:
	lw	$3,16($fp)
	li	$2,1			# 0x1
	bne	$3,$2,$L69
	la	$2,convertSTRING_TO_INT
	sw	$2,OP1_TYPECAST
$L69:
	lw	$3,20($fp)
	li	$2,1			# 0x1
	bne	$3,$2,$L70
	la	$2,convertSTRING_TO_INT
	sw	$2,OP2_TYPECAST
$L70:
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
	la	$6,op_PLUS
	jal	typecheck_GENERIC_INT_STRING_3OP
	move	$sp,$fp
	lw	$31,20($sp)
	lw	$fp,16($sp)
	addu	$sp,$sp,24
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
	beq	$3,$2,$L77
	lw	$3,16($fp)
	li	$2,1			# 0x1
	beq	$3,$2,$L77
	lw	$3,20($fp)
	li	$2,2			# 0x2
	beq	$3,$2,$L77
	lw	$3,20($fp)
	li	$2,1			# 0x1
	beq	$3,$2,$L77
	la	$4,$LC7
	jal	PrintfNormal
	jal	Exit
$L77:
	lw	$3,16($fp)
	li	$2,2			# 0x2
	beq	$3,$2,$L78
	lw	$3,16($fp)
	li	$2,1			# 0x1
	beq	$3,$2,$L78
	lw	$2,16($fp)
	sll	$3,$2,2
	la	$2,typeMaps
	addu	$2,$3,$2
	la	$4,$LC8
	lw	$5,0($2)
	jal	PrintfNormal
	jal	Exit
$L78:
	lw	$3,20($fp)
	li	$2,2			# 0x2
	beq	$3,$2,$L79
	lw	$3,20($fp)
	li	$2,1			# 0x1
	beq	$3,$2,$L79
	lw	$2,20($fp)
	sll	$3,$2,2
	la	$2,typeMaps
	addu	$2,$3,$2
	la	$4,$LC8
	lw	$5,0($2)
	jal	PrintfNormal
	jal	Exit
$L79:
	lw	$3,16($fp)
	li	$2,2			# 0x2
	bne	$3,$2,$L80
	la	$2,convertINT_TO_STRING
	sw	$2,OP1_TYPECAST
$L80:
	lw	$3,20($fp)
	li	$2,2			# 0x2
	bne	$3,$2,$L81
	la	$2,convertINT_TO_STRING
	sw	$2,OP2_TYPECAST
$L81:
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
	beq	$3,$2,$L85
	lw	$3,16($fp)
	li	$2,1			# 0x1
	beq	$3,$2,$L85
	lw	$3,20($fp)
	li	$2,2			# 0x2
	beq	$3,$2,$L85
	lw	$3,20($fp)
	li	$2,1			# 0x1
	beq	$3,$2,$L85
	la	$4,$LC7
	jal	PrintfNormal
	jal	Exit
$L85:
	lw	$3,16($fp)
	li	$2,2			# 0x2
	beq	$3,$2,$L86
	lw	$3,16($fp)
	li	$2,1			# 0x1
	beq	$3,$2,$L86
	lw	$2,16($fp)
	sll	$3,$2,2
	la	$2,typeMaps
	addu	$2,$3,$2
	la	$4,$LC8
	lw	$5,0($2)
	jal	PrintfNormal
	jal	Exit
$L86:
	lw	$3,20($fp)
	li	$2,2			# 0x2
	beq	$3,$2,$L87
	lw	$3,20($fp)
	li	$2,1			# 0x1
	beq	$3,$2,$L87
	lw	$2,20($fp)
	sll	$3,$2,2
	la	$2,typeMaps
	addu	$2,$3,$2
	la	$4,$LC8
	lw	$5,0($2)
	jal	PrintfNormal
	jal	Exit
$L87:
	lw	$3,16($fp)
	li	$2,2			# 0x2
	bne	$3,$2,$L88
	la	$2,convertINT_TO_STRING
	sw	$2,OP1_TYPECAST
$L88:
	lw	$3,20($fp)
	li	$2,1			# 0x1
	bne	$3,$2,$L89
	la	$2,convertSTRING_TO_INT
	sw	$2,OP2_TYPECAST
$L89:
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
	beq	$3,$2,$L91
	lw	$2,16($fp)
	sll	$3,$2,2
	la	$2,typeMaps
	addu	$2,$3,$2
	la	$4,$LC9
	lw	$5,0($2)
	jal	PrintfNormal
	jal	Exit
$L91:
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
	beq	$3,$2,$L93
	lw	$2,16($fp)
	sll	$3,$2,2
	la	$2,typeMaps
	addu	$2,$3,$2
	la	$4,$LC10
	lw	$5,0($2)
	jal	PrintfNormal
	jal	Exit
$L93:
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
	beq	$3,$2,$L95
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
$L95:
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
	bne	$3,$2,$L98
	lw	$3,20($fp)
	li	$2,2			# 0x2
	bne	$3,$2,$L98
	j	$L97
$L98:
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
$L97:
	move	$sp,$fp
	lw	$31,28($sp)
	lw	$fp,24($sp)
	addu	$sp,$sp,32
	j	$31
	.end	typecheck_GENERIC_INT_3OP
