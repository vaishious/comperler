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
    return 0;
}
