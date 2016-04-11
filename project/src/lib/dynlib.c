#define NULL 0

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

