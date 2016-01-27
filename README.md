# comperler
CS335A Assignment(s) and Project Repository

# Language Features

* Variables

* Scalars

* Arrays

* Hashes

* IF/ELSIF/ELSE/UNLESS

* Loops

* Operators

* Subroutines

* References

## TODO - ASSIGNMENT 2

#### Instructions

* Currently, only the basic instructions have been implemented. Add more to ease up translation work while retaining abstraction if possible.

* Variables can be hashes, arrays or simple variables. Implement separate checks to identify them, or set up a convention in the IR itself which helps us recognize them.

#### Library

* We might need to implement a string library as well if we want to handle string data-types well. Functions may include string length, string concatenation etc.

* We can make the print library a bit fancier if we want to use format strings. Can use ellipsis for variable number of arguments.

#### Data Region

* Set up a data-region allocator class. Functions are -

        * Will assign memory appropriately in the data segment for all the variables. (Should be .word for all of them. For strings, they will always hold the 32-bit address where the string is stored. Holds for both static and dynamically allocated string buffers)

        * Implement methods to get/set memory addresses with respect to the global pointer register.

#### Registers

* We should set up a separate class for registers providing the following functions -

        * Is the register free?

        * If the register is allocated, get/set the memory address of the variable.

        * Spilling the register if it is allocated. Since we have the memory address of the variable (using the data-region class), we can use load/store for the same.

* Implement the register allocator in the basic block class.

#### Translation

* Set up a separate translation module for each kind of instruction, which can output hand-crafted assembly. Will make integration a lot simpler. For example, a GOTO class with a "guard" member variable can mimick both IFGOTO and the simple GOTO.  
