/*
 * 1. Cross compile this file on the NachOS cross compiler without
 *    assembling or linking.
 * 
 * 2. Then remove the "jal __main" line from the generated .s file
 *
 * 3. Now the .s file will run on SPIM
 */

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

int ReadInt() {
    int retValInt;
    asm("
            li  $v0, 5
            syscall
            move %[Output], $v0
        "
        : [Output] "=r" (retValInt));

    return retValInt;
}

char ReadChar() {
    char retValChar;
    asm("
            li  $v0, 12
            syscall
            move %[Output], $v0
        "
        : [Output] "=r" (retValChar));

    return retValChar;
}

void ReadString(char *buffer, unsigned int length) {
    asm("
            move $a0, %[BufferAddr]
            move $a1, %[Length]
            li   $v0, 8
            syscall
        "
        :
        : [BufferAddr] "r" (buffer), [Length] "r" (length));
}

void Printf(char *formatSpecifier, ...) {

    // Very inefficient implementation. System call for every character. 
    // Enough for this assignment. Will optimize during the final project compilation

    // va_start
    char *argPtr = (char *)(&formatSpecifier) + sizeof(char *);

    int argInt;

    char argChar;
    char *argStr;

    while((*formatSpecifier) != '\0') {
        if ((*formatSpecifier) == '%') {
            formatSpecifier++;

            if ((*formatSpecifier) == 'd') {
                argInt = *((int *)argPtr);
                PrintInt(argInt);
                argPtr += sizeof(int);
            } else if ((*formatSpecifier) == 's') {
                argStr = *((char **) argPtr);
                PrintString(argStr);
                argPtr += sizeof(char *);
            } else if ((*formatSpecifier) == 'c') {
                argChar = *((char *) argPtr);
                PrintChar(argChar);
                argPtr += sizeof(char);
            } else {
                return;
            }

        } else {
            PrintChar((*formatSpecifier));
        }

        formatSpecifier++;
    }
}


int main() {
    char *namePtr = (char *)alloc(sizeof(char) * 40);
    PrintString("Input Your Name Please : \n");
    ReadString(namePtr, 40);
    PrintString("Hello ");
    PrintString(namePtr);
    PrintChar('\n');
    PrintString("Input a Number : ");
    int a = ReadInt();
    int b = a * a;
    PrintString("Square of ");
    PrintInt(a);
    PrintString(" is ");
    PrintInt(b);
    PrintChar('\n');
    Printf("%d %d %d Hello World %s \nI am just trying here : %s %s", 1, 2, 3, "My String", "Maah Lifee", "Maah Ruless");
    return 0;
}

