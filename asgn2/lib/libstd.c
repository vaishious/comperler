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

void ExitWithMessage(char *message, char *reference)
{
    if(reference != NULL)
        Printf("%s : %s", message, reference);
    else
        PrintString(message);

    asm("
            li $v0, 10
            syscall
        ");
}
