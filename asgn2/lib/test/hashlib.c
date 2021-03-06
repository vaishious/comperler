/*
 * 1. Cross compile this file on the NachOS cross compiler without
 *    assembling or linking.
 * 
 * 2. Then remove the "jal __main" line from the generated .s file
 *
 * 3. Now the .s file will run on SPIM
 */

typedef struct Element {
	char *key;	// Should be NULL terminated
	void *valRef;
	struct Element *next;
} Element;

typedef struct Hash {
  	/* Data looks like [ <Hash> -> <Element> -> <Element> -> ... ] */

	Element *first,*last;
	int length;
} Hash;

void *alloc(unsigned int size)
{
        void *ptr;

	/* Inline assembly to call the sbrk syscall */
        asm("	
		move $a0, %1
        	li $v0,9
        	syscall
        	sw $v0, %0
	    "
	    :"=m"(ptr)
	    :"r"(size)
        );  
        return ptr;
}

int strCmp(char *s1,char *s2)
{
	int i;
	for(i = 0;s1[i] && s2[i];i++) {
		if(s1[i] != s2[i]) {
			return -1;
		}
	}
	if(s1[i] || s2[i])		// String lengths differ
		return -1;
	return 0;
}

Element *findMatch(Hash *hashPtr,char *s)
{
	int i;
	Element *elemPtr = hashPtr->first;

	while(elemPtr != 0) {
		if(!strCmp(elemPtr->key,s))
			break;
		elemPtr = elemPtr->next;
	}
	return elemPtr;		/* If no match, returns NULL */
}

Hash *initHash(void)
{
	Hash *hashPtr = (Hash *)alloc(sizeof(Hash));
	hashPtr->first = hashPtr->last = 0;
	hashPtr->length = 0;
	return hashPtr;
}

int addElement(Hash *hashPtr,char *key,void *valRef)
{
	Element *elemPtr;
	if((elemPtr = findMatch(hashPtr,key))) {
		elemPtr->key = key;
		elemPtr->valRef = valRef;
		return 0;
	}

	elemPtr = (Element *)alloc(sizeof(Element));
	elemPtr->key = key;
	elemPtr->valRef = valRef;
	if(hashPtr->length == 0)
		hashPtr->first = hashPtr->last = elemPtr;
	else {
		hashPtr->last->next = elemPtr;
		hashPtr->last = elemPtr;
	}
	hashPtr->length++;
	return 0;
}

void *getValue(Hash *hashPtr,char *key)
{
	Element *elemPtr;
	if((elemPtr = findMatch(hashPtr,key)))
		return elemPtr->valRef;
	return 0;
}

void PrintInt(signed int outNum) {
    asm("
            move $a0, %[Input]
            li   $v0, 1
            syscall
        "
        :
        : [Input] "r" (outNum));
}

void PrintString(char *stringPtr) {
    asm("
            move $a0, %[Input]
            li   $v0, 4
            syscall
        "
        :
        : [Input] "r" (stringPtr)

       );
}

void PrintChar(char outChar) {
    asm("
            move $a0, %[Input]
            li   $v0, 11
            syscall
        "
        :
        : [Input] "r" (outChar));
}

int main()
{
	Hash *hashPtr = initHash();

	/* 
	 * When a string is initialised as,
	 * ``` 
	 * 	char s[] = "abcd";
	 * ```
	 * the NachOS cross compiler throws an error.
	 */
	char s[10],u[10],t[10];
       	s[0] = 'a';		
       	s[1] = 'b';
       	s[2] = 'c';
       	s[3] = 'd';
       	s[4] = '\0';

       	u[0] = 'e';
       	u[1] = 'f';
       	u[2] = 'g';
       	u[3] = 'h';
       	u[4] = '\0';

	t[0] = 'p';
	t[1] = 'q';
	t[2] = 'r';
	t[3] = 's';
	t[4] = '\0';
	addElement(hashPtr,s,(void *)u);
	addElement(hashPtr,t,(void *)s);
	addElement(hashPtr,u,(void *)t);
	PrintString("Number of elements in the hash is: ");
	PrintInt(hashPtr->length);
	PrintChar('\n');
	PrintString(u);
	PrintString(" => ");
	PrintString((char *)getValue(hashPtr,u));
	PrintChar('\n');
	PrintString(s);
	PrintString(" => ");
	PrintString((char *)getValue(hashPtr,s));
	PrintChar('\n');
	PrintString(t);
	PrintString(" => ");
	PrintString((char *)getValue(hashPtr,t));
	PrintChar('\n');
	return 0;
}
