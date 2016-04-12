#define NULL 0

extern void *(*OP1_TYPECAST)(void *);
extern void *(*OP2_TYPECAST)(void *);
extern void (*OPCONTROL)(void *);

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
