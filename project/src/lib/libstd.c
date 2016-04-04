#define NULL 0
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

void ExitWithMessage(char *message, char *refChar, int refInt)
{
    if(refChar != NULL) {
        PrintString(message);
        PrintString(refChar);
        PrintChar('\n');
    }
    else {
        PrintString(message);
        PrintInt(refInt);
        PrintChar('\n');
    }
    asm("
            li $v0, 10
            syscall
        ");
}
