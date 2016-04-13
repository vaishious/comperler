/*
 * 1. Cross compile this file on the NachOS cross compiler without
 *    assembling or linking.
 * 
 * 2. Then remove the "jal __main" line from the generated .s file
 *
 * 3. Now the .s file will run on SPIM
 */

#define NULL 0
#define TYPE_UNKNOWN 0
#define TYPE_STRING 1
#define TYPE_INT 2
#define TYPE_ARRAY 3
#define TYPE_HASH 4

extern void *(*OP1_TYPECAST)(void *);

typedef struct Element {
    char *key;	// Should be NULL terminated
    void *valRef;
    int type;
    struct Element *next;
} Element;

typedef struct Hash {
    /* Data looks like [ <Hash> -> <Element> -> <Element> -> ... ] */

    Element *first,*last;
    int length;

    // Integers or Addresses (strings/hashes)
    // int type;
} Hash;

Element *findMatch(Hash *hashPtr, char *s)
{
    int i;
    Element *elemPtr = hashPtr->first;

    for (i=0; i < hashPtr->length; i++) {
		if(!strCmp(elemPtr->key, s))
			break;

        elemPtr = elemPtr->next;
    }

    return elemPtr;
}

Hash *initHash()
{
    Hash *hashPtr = (Hash *)alloc(sizeof(Hash));
    hashPtr->first = hashPtr->last = 0;
    hashPtr->length = 0;
    return hashPtr;
}

int addElementType(Hash *hashPtr, void *inpKey, void *valType)
{
    char *key = (char *)OP1_TYPECAST(inpKey);
    Element *elemPtr;

    if((elemPtr = findMatch(hashPtr, key))) {
        elemPtr->key = key;
        elemPtr->type = valType;
        return 0;
    }

    elemPtr = (Element *)alloc(sizeof(Element));
    elemPtr->key = key;
    elemPtr->type = valType;
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

int addElement(Hash *hashPtr, void *inpKey, void *valRef)
{
    char *key = (char *)OP1_TYPECAST(inpKey);

    Element *elemPtr;
    if((elemPtr = findMatch(hashPtr, key))) {
        elemPtr->key = key;
        elemPtr->valRef = valRef;
        return 0;
    }

    elemPtr = (Element *)alloc(sizeof(Element));
    elemPtr->key = key;
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

void *getHashValue(Hash *hashPtr, void *inpKey)
{
    char *key = (char *)OP1_TYPECAST(inpKey);
    Element *elemPtr;
    if((elemPtr = findMatch(hashPtr, key)))
            return elemPtr->valRef;

    // Add an element yourself
    addElement(hashPtr, key, (void *)0); 
    addElementType(hashPtr, key, (void *)TYPE_INT);

    if((elemPtr = findMatch(hashPtr, key)))
            return elemPtr->valRef;
}

void *getHashValueType(Hash *hashPtr, void *inpKey)
{
    char *key = (char *)OP1_TYPECAST(inpKey);
    Element *elemPtr;
    if((elemPtr = findMatch(hashPtr, key)))
            return elemPtr->type;

    // Add an element yourself
    addElement(hashPtr, key, (void *)0); 
    addElementType(hashPtr, key, (void *)TYPE_INT);

    if((elemPtr = findMatch(hashPtr, key)))
            return elemPtr->type;
}

void *getFirstKey(Hash *hashPtr)
{
	Element *fstEl = (hashPtr->first);
	if (fstEl == NULL) {
		return NULL;
	} else {
		return (void *)(fstEl->key);
	}
}

void *getNextKey(Hash *hashPtr, void *inpKey)
{
	Element *currEl = findMatch(hashPtr, (char *)inpKey);
	if (currEl == hashPtr->last) {
		return NULL;
	}
	else {
		return (void *)((currEl->next)->key);
	}
}
