/*
 * 1. Cross compile this file on the NachOS cross compiler without
 *    assembling or linking.
 * 
 * 2. Then remove the "jal __main" line from the generated .s file
 *
 * 3. Now the .s file will run on SPIM
 */

#define NULL 0

typedef struct Element {
    char *key;	// Should be NULL terminated
    int keyInt;
    void *valRef;
    struct Element *next;
} Element;

typedef struct Hash {
    /* Data looks like [ <Hash> -> <Element> -> <Element> -> ... ] */

    Element *first,*last;
    int length;

    // Integers or Addresses (strings/hashes)
    int type;
} Hash;

Element *findMatch(Hash *hashPtr, char *s, int keyInt)
{
    int i;
    Element *elemPtr = hashPtr->first;

    while(elemPtr != 0) {
        if (hashPtr->type == 0)
            if (elemPtr->keyInt == keyInt)
                break;
        else
            if(!strCmp(elemPtr->key, s))
                break;

        elemPtr = elemPtr->next;
    }

    return elemPtr;
}

Hash *initHash(int type)
{
    Hash *hashPtr = (Hash *)alloc(sizeof(Hash));
    hashPtr->first = hashPtr->last = 0;
    hashPtr->length = 0;
    hashPtr->type = type;
    return hashPtr;
}

int addElement(Hash *hashPtr, char *key, int keyInt, void *valRef)
{
    Element *elemPtr;
    if((elemPtr = findMatch(hashPtr, key, keyInt))) {
        elemPtr->key = key;
        elemPtr->keyInt = keyInt;
        elemPtr->valRef = valRef;
        return 0;
    }

    elemPtr = (Element *)alloc(sizeof(Element));
    elemPtr->key = key;
    elemPtr->keyInt = keyInt;
    elemPtr->valRef = valRef;
    elemPtr->next = 0;
    if(hashPtr->length == 0)
            hashPtr->first = hashPtr->last = elemPtr;
    else {
            hashPtr->last->next = elemPtr;
            hashPtr->last = elemPtr;
    }
    hashPtr->length++;
    return 0;
}

void *getValue(Hash *hashPtr, char *key, int keyInt, char *message)
{
    Element *elemPtr;
    if((elemPtr = findMatch(hashPtr, key, keyInt)))
            return elemPtr->valRef;

    // Raise an exception
    ExitWithMessage(message, key);
}
