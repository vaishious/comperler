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

