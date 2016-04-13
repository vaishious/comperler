from codegen import *
from irgen import *

import os, sys

def Compile(fileName):

    myLexer = LEXER.Lexer()
    myLexer.build()

    myParser = PARSER.Parser()
    myParser.set_tokens(myLexer.tokens)
    myParser.build()

    try:
        with open(fileName, 'r') as filePtr:
            irFileName = os.path.splitext(os.path.basename(fileName))[0] + '.ir'
            symTabManager, funcActRecords = myParser.parse(filePtr.read(), irFileName)
    except:
        print "Encountered an error in IR Generation."

    try:
        with open(irFileName, 'r') as filePtr:
            codeGen = CodeGenerator(filePtr.read(), irFileName, symTabManager, funcActRecords)
            codeGen.GenBasicBlocks()
            codeGen.BuildCode()
    except:
        print "Encountered an error in Code Generation."
