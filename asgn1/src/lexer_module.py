import ply.lex as lex

class Lexer(object): # Inheriting from object provides extra functionality

    # Calculator template for our Perl Parser
    # Building this as a class should be better right? Will help us in 
    # structuring the code properly into separate modules

    # List of token names.   This is always required
    tokens = (
       'NUMBER',

       'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULUS', 'EXPONENT',
       'OR', 'AND', 'NOT', 'XOR', 'LSHIFT', 'RSHIFT',
       'LT', 'GT', 'LE', 'GE', 'EQ', 'NE', 'CMP',

       # Assignment Operators
       'EQUALS', 'TIMESEQUAL', 'DIVEQUAL', 'MODEQUAL',
       'PLUSEQUAL', 'MINUSEQUAL',
       'LSHIFTEQUAL','RSHIFTEQUAL', 'ANDEQUAL', 'XOREQUAL',
       'OREQUAL', 'EXPEQUAL',

       # Miscellaneous Operators
       'DOT', 'REPEAT', 'RANGE', 'INC', 'DEC', 'ARROW',

       'LPAREN',
       'RPAREN',
    )

    # Arithmetic Operators
    t_PLUS    = r'\+'
    t_MINUS   = r'-'
    t_TIMES   = r'\*'
    t_DIVIDE  = r'/'
    t_MODULUS = r'%'
    t_EXPONENT = r'\*\*'

    # Bitwise Operators
    t_OR = r'\|'
    t_AND = r'&'
    t_NOT = r'~'
    t_XOR = r'\^'
    t_LSHIFT = r'<<'
    t_RSHIFT = r'>>'

    # Equality Operators
    t_LT  = r'<'
    t_GT  = r'>'
    t_LE  = r'<='
    t_GE  = r'>='
    t_EQ  = r'=='
    t_NE  = r'!='
    t_CMP = r'<=>'

    # Assignment Operators
    t_EQUALS      = r'='
    t_PLUSEQUAL   = r'\+='
    t_MINUSEQUAL  = r'-='
    t_TIMESEQUAL  = r'\*='
    t_DIVEQUAL    = r'/='
    t_MODEQUAL    = r'%='
    t_EXPEQUAL    = r'\*\*='
    t_LSHIFTEQUAL = r'<<='
    t_RSHIFTEQUAL = r'>>='
    t_ANDEQUAL    = r'&='
    t_XOREQUAL    = r'\^='
    t_OREQUAL     = r'\|='

    # Miscellaneous Operators
    t_DOT = r'\.'
    t_REPEAT = r'x'	    ## Warning: Clashes with ID??
    t_RANGE = r'\.\.'
    t_INC = r'\+\+'
    t_DEC = r'--'
    t_ARROW = r'->'

    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'

    # A regular expression rule with some action code
    # Note addition of self parameter since we're in a class
    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)    
        return t

    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore  = ' \t'

    # Error handling rule
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer
    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # Sample helper functions for our main driver

    # Pass input for lexing
    def takeInput(self, data):
	self.lexer.input(data)

    # Get single token
    def getToken(self):
	return self.lexer.token()

    # Get all tokens at once
    def getAllTokens(self):
	return [tok for tok in self.lexer]

    
