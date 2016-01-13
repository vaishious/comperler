import ply.lex as lex

class Lexer(object): # Inheriting from object provides extra functionality

    # Calculator template for our Perl Parser

    # List of keywords
    keywords = (
	# Logical Operator Keywords
	'AND', 'OR',

	# Branch Keywords
	'IF', 'ELSE', 'ELSIF', 'UNLESS', 'SWITCH',

	# Loop Keywords
	'WHILE', 'UNTIL', 'FOR', 'FOREACH', 'DO',

	# Loop Control Statement Keywords
	'NEXT', 'LAST', 'CONTINUE', 'REDO', 'GOTO',

	# Function Keywords
	'NOT', 'PRINT', 'PRINTF', 'MY'
    )

    # Dictionary of keywords
    reserved = dict(zip(map(lambda x:x.lower(), keywords), keywords))

    # List of token names.   This is always required
    tokens = (
       'NUMBER', 'VARIABLE', 'ID',

       # Arithmetic Operators
       'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULUS', 'EXPONENT',
       'BOR', 'BAND', 'BNOT', 'BXOR', 'LSHIFT', 'RSHIFT',

       # Relational Operators
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
       'SEMICOLON'
    ) + keywords

    # Variables (Let's work with this for now)
    # Adding these as functions as we can play with priority
    def t_VARIABLE(self, t):
	r'[$@%][a-zA-Z_][a-zA-Z0-9_]*'
	return t

    # IDs (Again, let's work with this for now)
    def t_ID(self, t):
	r'[a-zA-Z_][a-zA-Z0-9_]*'
	t.type = self.reserved.get(t.value, 'ID') # Look for keywords
	return t

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)    
        return t

    # Arithmetic Operators
    t_PLUS      = r'\+'
    t_MINUS     = r'-'
    t_TIMES     = r'\*'
    t_DIVIDE    = r'/'
    t_MODULUS   = r'%'
    t_EXPONENT  = r'\*\*'

    # Bitwise Operators
    t_BOR    = r'\|'
    t_BAND   = r'&'
    t_BNOT   = r'~'
    t_BXOR   = r'\^'
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
    t_DOT 	= r'\.'
    t_REPEAT    = r'x'	    ## Warning: Clashes with ID??
    t_RANGE     = r'\.\.'
    t_INC       = r'\+\+'
    t_DEC       = r'--'
    t_ARROW     = r'->'

    t_LPAREN    = r'\('
    t_RPAREN    = r'\)'
    t_SEMICOLON = r';'


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
    def build(self, **kwargs):
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

