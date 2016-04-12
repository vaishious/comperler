#define TYPE_UNKNOWN 0
#define TYPE_STRING 1
#define TYPE_INT 2
#define TYPE_ARRAY 3
#define TYPE_HASH 4

#include "dynlib.c"

const char *typeMaps[5] = {"UNKNOWN", "STRING", "INT", "ARRAY", "HASH"};

void * Exit() {
    asm("
            li $v0, 10
            syscall
        ");
}

void * typecheck_PLUS(void *src1, void *src2) {

    int type1 = (int) src1;
    int type2 = (int) src2;

    OP1_TYPECAST = &dummyFunc;
    OP2_TYPECAST = &dummyFunc;
    OPCONTROL = &op_PLUS;

    if ((type1 != TYPE_INT) && (type2 != TYPE_INT)) {
        PrintfNormal("Atleast one argument of PLUS has to be an INTEGER");
        Exit();
    }

    if ((type1 != TYPE_INT) && (type1 != TYPE_STRING)) {
        PrintfNormal("Cannot add %s to an INT", typeMaps[type1]);
        Exit();
    }

    if ((type2 != TYPE_INT) && (type2 != TYPE_STRING)) {
        PrintfNormal("Cannot add %s to an INT", typeMaps[type2]);
        Exit();
    }

    if (type1 == TYPE_STRING) { OP1_TYPECAST = &convertSTRING_TO_INT; }
    if (type2 == TYPE_STRING) { OP2_TYPECAST = &convertSTRING_TO_INT; }

    return (void *)TYPE_INT;
}

void * typecheck_HASH_INDEX_CHECK(void *typeIndex) {

    int type = (int) typeIndex;

    if ((type != TYPE_STRING)) {
        PrintfNormal("Hash index needs to be a STRING, not %s\n", typeMaps[type]);
        Exit();
    }
}

void * typecheck_ARRAY_INDEX_CHECK(void *typeIndex) {

    int type = (int) typeIndex;

    if ((type != TYPE_INT)) {
        PrintfNormal("Array index needs to be an INT, not %s\n", typeMaps[type]);
        Exit();
    }
}

void * typecheck_TYPE_EQUAL(void *inpType1, void *inpType2) {

    int type1 = (int) inpType1;
    int type2 = (int) inpType2;

    if (type1 != type2) {
        PrintfNormal("Need types %s and %s to be equal\n", typeMaps[type1], typeMaps[type2]);
        Exit();
    }
}

void * typecheck_GENERIC_INT_3OP(void * inpType1, void *inpType2) {

    int type1 = (int) inpType1;
    int type2 = (int) inpType2;

    if ((type1 != TYPE_INT) || (type2 != TYPE_INT)) {
        PrintfNormal("Cannot perform the required arithmetic operation between types %s and %s\n", typeMaps[type1], typeMaps[type2]);
        Exit();
    }
}
