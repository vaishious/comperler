/*
 * 1. Cross compile this file on the NachOS cross compiler without
 *    assembling or linking.
 * 
 * 2. Then remove the "jal __main" line from the generated .s file
 *
 * 3. Now the .s file will run on SPIM
 */

#define NULL 0

typedef struct structArray {
    int length;
    int *addr;
} Array_t;

Array_t *initArray()
{
    // Working under the assumption that addresses are 4-bytes and so are integers
    // We initialize with only one entry
    Array_t *arrayPtr = (Array_t *)alloc(sizeof(Array_t));
    arrayPtr->addr = (int *)alloc(4);
    
    if (arrayPtr != NULL) {
            arrayPtr->length = 1;
    }

    return arrayPtr;
}

int lengthOfArray(Array_t *arrayPtr)
{
    if (arrayPtr != NULL) {
        return arrayPtr->length;
    } else {
        return 0;
    }
}

void *accessIndex(Array_t *arrayPtr, int index)
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
        }
        
    }

    return (void *)((arrayPtr->addr) + index);
}
