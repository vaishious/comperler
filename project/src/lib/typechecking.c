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

void * typecheck_GENERIC_INT_STRING_3OP(void *src1, void *src2, void *(*op)(void *, void *)) {

    int type1 = (int) src1;
    int type2 = (int) src2;

    OP1_TYPECAST = &dummyFunc;
    OP2_TYPECAST = &dummyFunc;
    OPCONTROL = op;

    if (((type1 != TYPE_INT) && (type1 != TYPE_STRING)) && ((type2 != TYPE_INT) && (type2 != TYPE_STRING))) {
        PrintfNormal("Line <%d> Atleast one argument of arithmetic operation has to be an INT/STRING\n", LINENUM);
        Exit();
    }

    if ((type1 != TYPE_INT) && (type1 != TYPE_STRING)) {
        PrintfNormal("Line <%d> Cannot perform arithmetic operation on %s with a INT/STRING\n", LINENUM, typeMaps[type1]);
        Exit();
    }

    if ((type2 != TYPE_INT) && (type2 != TYPE_STRING)) {
        PrintfNormal("Line <%d> Cannot perform arithmetic operation on %s with a INT/STRING\n", LINENUM, typeMaps[type2]);
        Exit();
    }

    if (type1 == TYPE_STRING) { OP1_TYPECAST = &convertSTRING_TO_INT; }
    if (type2 == TYPE_STRING) { OP2_TYPECAST = &convertSTRING_TO_INT; }

    return (void *)TYPE_INT;
}

void * typecheck_INT_PLUS(void *src1, void *src2) {

    int type1 = (int) src1;
    int type2 = (int) src2;
	if ((type1 == TYPE_ARRAY) && (type2 == TYPE_ARRAY)) {
		OP1_TYPECAST = &dummyFunc;
		OP2_TYPECAST = &dummyFunc;
		OPCONTROL = &op_ARRAY_CONCAT;
		return (void *) TYPE_ARRAY;
	}

    return (void *)typecheck_GENERIC_INT_STRING_3OP(src1, src2, &op_PLUS);
}

void * typecheck_GENERIC_UNARY_INT_STRING_2OP(void *src, void *(*op)(void *)) {
    int type = (int) src;

    OP1_TYPECAST = &dummyFunc;
    OPCONTROL = op;

    if ((type != TYPE_INT) && (type != TYPE_STRING)) {
        PrintfNormal("Line <%d> Cannot perform arithmetic operation on %s\n", LINENUM, typeMaps[type]);
        Exit();
    }

    if (type == TYPE_STRING) { OP1_TYPECAST = &convertSTRING_TO_INT; }

    return (void *)TYPE_INT;
}

void * typecheck_UNARY_INT_PLUS(void *src) {
    return (void *)typecheck_GENERIC_UNARY_INT_STRING_2OP(src, &op_UNARY_PLUS);
}

void * typecheck_UNARY_INT_MINUS(void *src) {
    return (void *)typecheck_GENERIC_UNARY_INT_STRING_2OP(src, &op_UNARY_MINUS);
}

void * typecheck_INT_MINUS(void *src1, void *src2) {
    return (void *)typecheck_GENERIC_INT_STRING_3OP(src1, src2, &op_MINUS);
}

void * typecheck_INT_MULT(void *src1, void *src2) {
    return (void *)typecheck_GENERIC_INT_STRING_3OP(src1, src2, &op_MULT);
}

void * typecheck_INT_DIV(void *src1, void *src2) {
    return (void *)typecheck_GENERIC_INT_STRING_3OP(src1, src2, &op_DIV);
}

void * typecheck_INT_MOD(void *src1, void *src2) {
    return (void *)typecheck_GENERIC_INT_STRING_3OP(src1, src2, &op_MOD);
}

void * typecheck_GENERIC_STRING_3OP(void *src1, void *src2, void *(*op)(void *, void *)) {
    int type1 = (int) src1;
    int type2 = (int) src2;

    OP1_TYPECAST = &dummyFunc;
    OP2_TYPECAST = &dummyFunc;
    OPCONTROL = op;

    if (((type1 != TYPE_INT) && (type1 != TYPE_STRING)) && ((type2 != TYPE_INT) && (type2 != TYPE_STRING))) {
        PrintfNormal("Line <%d> Atleast one argument of string operation has to be an INT/STRING\n", LINENUM);
        Exit();
    }

    if ((type1 != TYPE_INT) && (type1 != TYPE_STRING)) {
        PrintfNormal("Line <%d> Cannot perform string operation on %s with a INT/STRING\n", LINENUM, typeMaps[type1]);
        Exit();
    }

    if ((type2 != TYPE_INT) && (type2 != TYPE_STRING)) {
        PrintfNormal("Line <%d> Cannot perform string operation on %s with a INT/STRING\n", LINENUM, typeMaps[type2]);
        Exit();
    }

    if (type1 == TYPE_INT) { OP1_TYPECAST = &convertINT_TO_STRING; }
    if (type2 == TYPE_INT) { OP2_TYPECAST = &convertINT_TO_STRING; }

    return (void *)TYPE_STRING;
}

void * typecheck_STRING_RELOP(void *src1, void *src2) {
    return (void *)typecheck_GENERIC_STRING_3OP(src1, src2, &op_STRING_CMP);
}

void * typecheck_STRING_DOT(void *src1, void *src2) {
    return (void *)typecheck_GENERIC_STRING_3OP(src1, src2, &op_STRING_DOT);
}

void * typecheck_STRING_REPEAT(void *src1, void *src2) {
    int type1 = (int) src1;
    int type2 = (int) src2;

    OP1_TYPECAST = &dummyFunc;
    OP2_TYPECAST = &dummyFunc;
    OPCONTROL = &op_STRING_REPEAT;

    if (((type1 != TYPE_INT) && (type1 != TYPE_STRING)) && ((type2 != TYPE_INT) && (type2 != TYPE_STRING))) {
        PrintfNormal("Line <%d> Atleast one argument of string operation has to be an INT/STRING\n", LINENUM);
        Exit();
    }

    if ((type1 != TYPE_INT) && (type1 != TYPE_STRING)) {
        PrintfNormal("Line <%d> Cannot perform string operation on %s with a INT/STRING\n", LINENUM, typeMaps[type1]);
        Exit();
    }

    if ((type2 != TYPE_INT) && (type2 != TYPE_STRING)) {
        PrintfNormal("Line <%d> Cannot perform string operation on %s with a INT/STRING\n", LINENUM, typeMaps[type2]);
        Exit();
    }

    if (type1 == TYPE_INT) { OP1_TYPECAST = &convertINT_TO_STRING; }
    if (type2 == TYPE_STRING) { OP2_TYPECAST = &convertSTRING_TO_INT; }

    return (void *)TYPE_STRING;
}

void * typecheck_HASH_INDEX_CHECK(void *typeIndex) {

    int type = (int) typeIndex;
    OP1_TYPECAST = &dummyFunc;

    if ((type != TYPE_STRING) && (type != TYPE_INT)) {
        PrintfNormal("Line <%d> Hash index needs to be a STRING or an INT, not %s\n", LINENUM, typeMaps[type]);
        Exit();
    }

    if (type == TYPE_INT) { OP1_TYPECAST = &convertINT_TO_STRING; }
}

void * typecheck_ARRAY_INDEX_CHECK(void *typeIndex) {

    int type = (int) typeIndex;

    if ((type != TYPE_INT)) {
        PrintfNormal("Line <%d> Array index needs to be an INT, not %s\n", LINENUM, typeMaps[type]);
        Exit();
    }
}

void * typecheck_TYPE_EQUAL(void *inpType1, void *inpType2) {

    int type1 = (int) inpType1;
    int type2 = (int) inpType2;

    if (type1 != type2) {
        PrintfNormal("Line <%d> Need types %s and %s to be equal\n", LINENUM, typeMaps[type1], typeMaps[type2]);
        Exit();
    }
}

void * typecheck_GENERIC_INT_3OP(void * inpType1, void *inpType2) {

    int type1 = (int) inpType1;
    int type2 = (int) inpType2;

    if ((type1 != TYPE_INT) || (type2 != TYPE_INT)) {
        PrintfNormal("Line <%d> Cannot perform the required arithmetic operation between types %s and %s\n", LINENUM, typeMaps[type1], typeMaps[type2]);
        Exit();
    }
}
