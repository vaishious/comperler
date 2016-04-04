/*
 * 1. Cross compile this file on the NachOS cross compiler without
 *    assembling or linking.
 * 
 * 2. Then remove the "jal __main" line from the generated .s file
 *
 * 3. Now the .s file will run on SPIM
 */

#define NULL 0

typedef struct Array {
    int length;
    int *addr;
} Array;

Array *initArray()
{
    // Working under the assumption that addresses are 4-bytes and so are integers
    // We initialize with only one entry
    Array *arrayPtr = (Array *)alloc(sizeof(Array));
    arrayPtr->addr = (int *)alloc(4);
    
    if (arrayPtr != NULL) {
            arrayPtr->length = 1;
    }

    return arrayPtr;
}

int lengthOfArray(Array *arrayPtr)
{
    if (arrayPtr != NULL) {
        return arrayPtr->length;
    } else {
        return 0;
    }
}

void *accessIndex(Array *arrayPtr, int index, char *message)
{
    if (index >= arrayPtr->length) {
        //Working under the assumption that addresses are 4-bytes and so are integers
        int *newAddr = (int *)alloc(2*(index+1)*4);
        if (newAddr != NULL) {
            int it;
                //Copy from old memory to new memory
            for (it=0; it < arrayPtr->length; it++) {
                newAddr[it] = (arrayPtr->addr)[it];
            }

            arrayPtr->length = 2*(index+1);
            arrayPtr->addr = newAddr;
        } else {
            // Raise an exception
            ExitWithMessage(message, index);
        }
    }

    return (void *)((arrayPtr->addr) + index);
}
