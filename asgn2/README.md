### CS335 - Compilers - Assignment 2 - Code Generation ###

Source : Perl

Implementation : Python

Target : MIPS

#### Features 

* Arrays

* Hashes/Dictionaries with integer and string keys

* Strings and string comparision

* Printf/Scanf with IO formatting

* Dynamic Memory allocation using "alloc"

* Exception handler for key misses in dictionaries

* Automatic comment generation for the final assembly output

#### Implementation Details

* Local Register Allocation used at the basic block level

* Minimal stack allocation done to accomodate variable arguments for printf/scanf, and storing return addresses of functions

#### Code Structure

* instr3ac - This module holds all the classes required for parsing and storing the IR in a usable form.

* basic_blocks - This module holds the class whose objects represent a basic block. Also contains classes used to implement symbol tables and register address descriptors. The entire register allocation algorithm has been implemented here.

* mips_assembly - This module holds the classes used to implement the text and data region. Global data handling/allocation is performed here. Also contains the class used to implement a register which generates code for load/store etc.

* registers - Holds the entire register set of MIPS. Also encodes our policy for using registers.

* library - Holds translations for all the library functions (Printf, Scanf, Alloc)

* translator - This module contains the entire translation code used to generate the assembly file

* global_objects - This module holds all the critical data accessed/modified by all the other modules

* debug - Usual exception and debugging functions
