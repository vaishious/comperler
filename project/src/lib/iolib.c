/*
 * 1. Cross compile this file on the NachOS cross compiler without
 *    assembling or linking.
 * 
 * 2. Then remove the "jal __main" line from the generated .s file
 *
 * 3. Now the .s file will run on SPIM
 */

/*#include "arraylib.c"*/

#define TYPE_UNKNOWN 0
#define TYPE_STRING 1
#define TYPE_INT 2
#define TYPE_ARRAY 3
#define TYPE_HASH 4

typedef struct structArray {
    int length;
    int *addr;
} Array_t;

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

void PrintfNormal(char *formatSpecifier, ...) {

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

void PrintArray(Array_t *array) {
    int len = lengthOfArray(array);
    int i;

    for (i = 0; i < len; i++) {
        int type = *((int *) accessIndexType(array, i));
        void *val = (void *) *((int *) accessIndex(array, i));

        if (type == TYPE_INT)
            PrintInt((int) val);
        else if (type == TYPE_STRING)
            PrintString((char *) val);
        else if (type == TYPE_ARRAY)
            PrintArray((Array_t *) val);

        if (i != (len - 1)) {
            PrintChar(',');
            PrintChar(' ');
        }
    }
}

void Printf(Array_t *parameters) {

    char *formatSpecifier = (*((char **) accessIndex(parameters, 0)));
    int argIndex = 1;

    int argInt;

    char argChar;
    char *argStr;
    Array_t *argArray;

    while((*formatSpecifier) != '\0') {
        if ((*formatSpecifier) == '%') {
            formatSpecifier++;

            if ((*formatSpecifier) == 'd') {
                argInt = *((int *) accessIndex(parameters, argIndex));
                PrintInt(argInt);
                argIndex++;

            } else if ((*formatSpecifier) == 's') {
                argStr = (char *) *((char **) accessIndex(parameters, argIndex));
                PrintString(argStr);
                argIndex++;

            } else if ((*formatSpecifier) == 'c') {
                argChar = *((char *) accessIndex(parameters, argIndex));
                PrintChar(argChar);
                argIndex++;

            } else if ((*formatSpecifier) == 'a') { 
                argArray = (Array_t *) *((int *) accessIndex(parameters, argIndex));
                PrintArray(argArray);
                argIndex++;

            } else {
                return;
            }

        } else {
            PrintChar((*formatSpecifier));
        }

        formatSpecifier++;
    }
}

void Scanf(char *formatSpecifier, ...) {

    // We only care about %d, %c. We ignore all the other characters

    // va_start
    char *argPtr = (char *)(&formatSpecifier) + sizeof(char *);

    int *argInt;

    char *argChar;

    char *argString;

    while((*formatSpecifier) != '\0') {
        if ((*formatSpecifier) == '%') {
            formatSpecifier++;

            if ((*formatSpecifier) == 'd') {
                argInt = (int *) (*((int *)argPtr));
                (* argInt) = ReadInt();
                argPtr += sizeof(int *);
            } else if ((*formatSpecifier) == 'c') {
                argChar = (char *) (*((int *) argPtr));
                (* argChar) = ReadChar();
                argPtr += sizeof(char *);
            } else if ((*formatSpecifier) == 's') {
                argString = (char *) (*((int *) argPtr));
                ReadString(argString, 1000);
                argPtr += sizeof(char *);
            } else {
                return;
            }

        }

        formatSpecifier++;
    }
}
