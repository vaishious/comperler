#define NULL 0
#include "arraylib.c"

extern void *(*OP1_TYPECAST)(void *);
extern void *(*OP2_TYPECAST)(void *);
extern void (*OPCONTROL)(void *);
extern int LINENUM;

void *dummyFunc(void *arg) {
    return arg;
}

void *convertSTRING_TO_INT(void *arg) {
    char *str = (char *)arg;
	int negative = 0;
    int val = 0;
	if (*str == '-') {
		negative = 1;
		str++;
	}
	else if (*str == '+') {
		negative = 0;
		str++;
	}

    while (*str != 0) {
        if (*str > '9' || *str < '0') {
			if (negative == 1) {
				val = -val;
			}
            return (void *)val;
        }
        val = 10*val + ((int)(*str - '0'));
        str++;
    }

	if (negative == 1) {
		val = -val;
	}
    return (void *)val;
}

void * convertINT_TO_STRING(void *arg) {
    int numDigits = 1;
    int num = (int) arg;
    num /= 10;

    while (num > 0) {
        numDigits += 1;
        num /= 10;
    }

    char * buffer = (char *) alloc(sizeof(char) * (numDigits + 1));
    num = (int) arg;

    int bufIndex = numDigits - 1;
    buffer[bufIndex] = ('0' + num%10);
    num /= 10;
    bufIndex -= 1;

    while (num > 0) {
        buffer[bufIndex] = ('0' + num%10);
        num /= 10;
        bufIndex -= 1;
    }

    return (void *) buffer;
}

void * op_PLUS (void *inp1, void *inp2) {

    inp1 = OP1_TYPECAST(inp1);
    inp2 = OP2_TYPECAST(inp2);

    int first = (int)inp1;
    int second = (int)inp2;

    return (void *)(first + second);
}

void * op_MINUS (void *inp1, void *inp2) {

    inp1 = OP1_TYPECAST(inp1);
    inp2 = OP2_TYPECAST(inp2);

    int first = (int)inp1;
    int second = (int)inp2;

    return (void *)(first - second);
}

void * op_MULT (void *inp1, void *inp2) {

    inp1 = OP1_TYPECAST(inp1); inp2 = OP2_TYPECAST(inp2); 
    int first = (int)inp1;
    int second = (int)inp2;

    return (void *)(first * second);
}

void * op_DIV (void *inp1, void *inp2) {

    inp1 = OP1_TYPECAST(inp1);
    inp2 = OP2_TYPECAST(inp2);

    int first = (int)inp1;
    int second = (int)inp2;

    return (void *)(first / second);
}

void * op_MOD (void *inp1, void *inp2) {

    inp1 = OP1_TYPECAST(inp1);
    inp2 = OP2_TYPECAST(inp2);

    int first = (int)inp1;
    int second = (int)inp2;

    return (void *)(first % second);
}

void * op_STRING_CMP(void *inpString1, void *inpString2) {

    char * s1 = (char *)OP1_TYPECAST(inpString1);
    char * s2 = (char *)OP2_TYPECAST(inpString2);

    int i;
    for(i = 0; (s1[i] || s2[i]); i++) {	// Only end if both strings terminate 
        if(s1[i] > s2[i]) {    
            return (void *)1;
        } else if(s1[i] < s2[i]) {
            return (void *)(-1);
        }
    }
    return (void *) 0; // Will only reach here if both have same length and same characters at all points
}

void * op_STRING_DOT(void *inpString1, void *inpString2) {

    char * s1 = (char *)OP1_TYPECAST(inpString1);
    char * s2 = (char *)OP2_TYPECAST(inpString2);

    int len1 = 0, len2 = 0;
    for(len1=0; s1[len1]; len1++) ;
    for(len2=0; s2[len2]; len2++) ;

	char * s3 = (char *)alloc(sizeof(char)*(len1 + len2 + 1));
	int i;
	for (i=0; i<len1; i++) {
		s3[i] = s1[i];
	}
	for (i=0; i<len2; i++) {
		s3[len1 + i] = s2[i];
	}
	s3[len1 + len2] = '\0';
    return (void *)s3;
}

void * op_STRING_REPEAT(void *inpString1, void *repeatNum) {

    char * s1 = (char *)OP1_TYPECAST(inpString1);
    int n 	  = (int)   OP2_TYPECAST(repeatNum);

	if (n <= 0) {
		char * s2 = (char *)alloc(sizeof(char));
		s2[0] = '\0';
		return (void *)s2;
	}

    int len1 = 0;
    for(len1=0; s1[len1]; len1++) ;

	char * s2 = (char *)alloc(sizeof(char)*((len1*n) + 1));
	int i,j;
	for (i=0; i<n; i++) {
		for (j=0; j<len1; j++) {
			s2[i*len1 + j] = s1[j];
		}
	}
	s2[n*len1] = '\0';
    return (void *)s2;
}

void * op_ARRAY_CONCAT(void *inpArray1, void *inpArray2) {

    Array_t * a1 = (Array_t *)OP1_TYPECAST(inpArray1);
    Array_t * a2 = (Array_t *)OP2_TYPECAST(inpArray2);

    int len1 = lengthOfArray(a1), len2 = lengthOfArray(a2);

    Array_t * a3 = initArray();
    int i;

    for (i=0; i < len1; i++) {
            *accessIndex(a3, i) = *accessIndex(a1, i);
            *accessIndexType(a3, i) = *accessIndexType(a1, i);
    }

    for (i=0; i<len2; i++) {
            *accessIndex(a3, len1 + i) = *accessIndex(a2, i);
            *accessIndexType(a3, len1 + i) = *accessIndexType(a2, i);
    }

    return (void *)a3;
}
