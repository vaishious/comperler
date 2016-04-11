#define NULL 0

void *dummyFunc(void *arg) {
	return arg;
}

void *(*inp1_func)(void *) = &dummyFunc;
void *(*inp2_func)(void *) = &dummyFunc;
// Not sure what to set this default to?
void (*op)(int) = NULL;

void *convertStrInt(void *arg) {
	char *str = (char *)arg;
	int val = 0;
	while (*str != 0) {
		if (*str > '9' || *str < '0') {
			val = 0;
			return (void *)val;
		}
		val = 10*val + ((int)(*str - '0'));
	}
	return (void *)val;
}

void *add_int_int(void *inp1, void *inp2) {
	int first = (int)inp1;
	int second = (int)inp1;
	return (void *)(first + second);
}
