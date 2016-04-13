"""

MODULE  : global_objects.py

Purpose : This file simply stores global objects like Data region, 
          Text Region etc. which are to be used and modified across multiple modules

Import Acronym : G

"""

AsmData = None
AsmText = None

# For library functions like printf, we'll need to put arguments on the stack
# For that we need to allocate some space beforehand. This variable just keeps
# track of it

# Indent to be used for the code
INDENT = " "*4

# While translating every instruction, these are the relevant tables that are required
# They need to be loaded for every instruction to be translated. These are kept global 
# so as to ease their usage by different modules
CurrRegAddrTable = None
CurrSymbolTable  = None
CurrInstruction  = None
NextSymbolTable  = None
CurrFunction     = 'main'

# This map provides an easier interface to see the register allocation for the current
# instruction
AllocMap = {}
StackSpaceMap = {}

# Library functions
LIBSRC = ['../lib/hashlib.s', '../lib/iolib.s', '../lib/libstd.s', '../lib/libstring.s', '../lib/arraylib.s', '../lib/typechecking.s', '../lib/dynlib.s']

# Debugging library functions

#LibraryFunctionsUsed = set(['typecheck_INT_{PLUS,MINUS,MULT,DIV,MOD}', 'typecheck_HASH_INDEX_CHECK', 'typecheck_TYPE_EQUAL', 'PrintString', 'PrintfNormal', 'PrintChar', 'PrintInt', 'dummyFunc'])
LibraryFunctionsUsed = set(['dummyFunc', 'PrintfNormal', 'PrintInt', 'PrintChar', 'PrintString', 'PrintArray'])
EssentialLibraries = ['../lib/dynlib.s', '../lib/typechecking.s']
