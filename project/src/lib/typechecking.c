#define TYPE_UNKNOWN 0
#define TYPE_STRING 1
#define TYPE_INT 2
#define TYPE_ARRAY 3
#define TYPE_HASH 4

extern void *(*OPCONTROL)(void *);
extern void *(*OP1_TYPECAST)(void *);
extern void *(*OP2_TYPECAST)(void *);

extern char *TYPE_ERROR_PLUS;

void * typecheck_PLUS(void *src1, void *src2) {

    int type1 = (int) src1;
    int type2 = (int) src2;

    if ((type1 != type2) || (type1 != TYPE_INT)) {
        PrintString(&TYPE_ERROR_PLUS);
        asm("
                li $v0, 10
                syscall
            ");
    }
}
