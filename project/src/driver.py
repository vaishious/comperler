from codegen import *
from irgen import *

import os, sys

def Compile(fileName):

    myLexer = LEXER.Lexer()
    myLexer.build()

    myParser = PARSER.Parser()
    myParser.set_tokens(myLexer.tokens)
    myParser.build()

    with open(fileName, 'r') as filePtr:
        irFileName = os.path.splitext(os.path.basename(fileName))[0] + '.ir'
        symTabManager, funcActRecords = myParser.parse(filePtr.read(), irFileName)

    with open(irFileName, 'r') as filePtr:
        codeGen = CodeGenerator(filePtr.read(), irFileName, symTabManager, funcActRecords)
        codeGen.GenBasicBlocks()
        codeGen.BuildCode()

    



    
