from codegen import *
from irgen import *

import os, sys

def Compile(fileName):

    myLexer = LEXER.Lexer()
    myLexer.build()

    myParser = PARSER.Parser()
    myParser.set_tokens(myLexer.tokens)
    myParser.build()

    filePtr = open(fileName, 'r')
    myParser.parse(filePtr.read(), os.path.splitext(os.path.basename(fileName))[0] + '.ir')
    filePtr.close()
