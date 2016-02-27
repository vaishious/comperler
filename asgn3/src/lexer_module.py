import ply.lex as lex
import sys

class Lexer(object): # Inheriting from object provides extra functionality

    # List of keywords
    keywords = (
    # Logical Operator Keywords
    'AND', 'OR', 'XOR',

    # Branch Keywords
    'IF', 'ELSE', 'ELSIF', 'UNLESS', 'SWITCH',

    # Loop Keywords
    'WHILE', 'UNTIL', 'FOR', 'FOREACH', 'DO',

    # Loop Control Statement Keywords
    'NEXT', 'LAST', 'CONTINUE', 'REDO', 'GOTO',

    # Function Keywords
    'NOT', 'PRINT', 'PRINTF', 'MY',
    'KEYS', 'VALUES', 'EXISTS', 'DELETE',

    # Miscellaneous Keywords
    'SUB', 'RETURN'
    )

    # String relational operators
    # Let's pass them as separate tokens. If they are used as functions we can resolve that in the parser.
    # This brings more clarity

    string_relops = (
       # String Relational Operators
       'STRLT', 'STRGT', 'STRLE', 'STRGE', 'STREQ', 'STRNE', 'STRCMP',
       )


    # Dictionary of keywords
    reserved = dict(zip(map(lambda x:x.lower(), keywords), keywords))
    reserved_relops = dict(zip(map(lambda x:x[3:].lower(), string_relops), string_relops))

    # List of token names.   This is always required
    tokens = (

       # Comments
       'SINGLINECOMM', 'MULTILINECOMM',

       # String Literals
       'SINGQUOTSTR', 'DOUBQUOTSTR',

       # Computational elements
       'NUMBER', 'HEXADECIMAL', 'BINARY', 'OCTAL', 'VARIABLE', 'ID',

       # Arithmetic Operators
       'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULUS', 'EXPONENT',
       'BOR', 'BAND', 'BNOT', 'BXOR', 'LSHIFT', 'RSHIFT',

       # Logical Operators
       'LOR', 'LAND', 'LNOT',

       # Relational Operators
       'LT', 'GT', 'LE', 'GE', 'EQ', 'NE', 'CMP', 'TERNARY_CONDOP',

       # Assignment Operators
       'EQUALS', 'TIMESEQUAL', 'DIVEQUAL', 'MODEQUAL',
       'PLUSEQUAL', 'MINUSEQUAL',
       'LSHIFTEQUAL','RSHIFTEQUAL', 'ANDEQUAL', 'XOREQUAL',
       'OREQUAL', 'EXPEQUAL',

       # Miscellaneous Operators
       'DOT', 'REPEAT', 'RANGE', 'INC', 'DEC', 'ARROW', 'HASHARROW',

       # Various Syntax elements
       'REFERENCE', 'DEREFERENCE',
       'LPAREN', 'RPAREN',
       'LBLOCK', 'RBLOCK',
       'LBRACKET', 'RBRACKET',
       'SEMICOLON', 'COLON',
       'COMMA',

       # For error checking
       'WRONG_ID'

    ) + keywords + string_relops

    # Tokens which are passed to functions
    wrong_identifier = r'[0-9]+[a-zA-Z_][a-zA-Z0-9_]*'
    identifier       = r'[a-zA-Z_][a-zA-Z0-9_]*'
    variable         = r'[$@%][ ]*' + identifier
    dereference      = r'[$@%][$ ]*' + identifier
    reference        = r'[\\][ ]*' + dereference
    octal            = r'0[0-7]+'
    hexadecimal      = r'0[xX][0-9a-fA-F]+'
    binary           = r'0[bB][01]+'
    number           = r'\d+'

    # Variables (Let's work with this for now)
    @lex.TOKEN(hexadecimal)
    def t_HEXADECIMAL(self, t):
        t.value = int(t.value, 16)
        return t

    @lex.TOKEN(binary)
    def t_BINARY(self, t):
        t.value = int(t.value, 2)
        return t

    # Incorrect identifier checking at the highest priority
    @lex.TOKEN(wrong_identifier)
    def t_WRONG_ID(self, t):
        print("Illegal identifier '%s' at line %d" % (t.value, t.lexer.lineno))
        sys.exit(1)

    # Adding these as functions as we can play with priority
    @lex.TOKEN(variable)
    def t_VARIABLE(self, t):
        t.value = t.value.replace(' ', '')
        return t

    # Relative priority of REFERENCE and DEREFERENCE doesn't matter
    @lex.TOKEN(reference)
    def t_REFERENCE(self, t):
        t.value = t.value.replace(' ','')
        return t

    # Priority of DEREFERENCE must be lower than that of VARIABLE
    @lex.TOKEN(dereference)
    def t_DEREFERENCE(self, t):
        t.value = t.value.replace(' ','')
        return t

    # IDs (Again, let's work with this for now)
    @lex.TOKEN(identifier)
    def t_ID(self, t):
        t.type = self.reserved.get(t.value, 'ID') # Look for keywords
        
        if t.type == 'ID':                        # Look for operator matches
            t.type = self.reserved_relops.get(t.value, 'ID') # Look for keywords

        # Check if it can be REPEAT.
        t.type = 'REPEAT' if t.value == 'x' else t.type

        return t

    @lex.TOKEN(octal)
    def t_OCTAL(self, t):
        t.value = int(t.value, 8)
        return t

    @lex.TOKEN(number)
    def t_NUMBER(self, t):
        t.value = int(t.value)    
        return t

    def t_SINGLELINECOMM(self, t):
        r'\#.*'
        pass

    # String Literals
    t_SINGQUOTSTR = r'\'([^\\]|(\\[\s\S]))*?\''
    t_DOUBQUOTSTR = r'\"([^\\]|(\\[\s\S]))*?\"'

    # Arithmetic Operators
    t_PLUS           = r'\+'
    t_MINUS          = r'-'
    t_TIMES          = r'\*'
    t_DIVIDE         = r'/'
    t_MODULUS        = r'%'
    t_EXPONENT       = r'\*\*'

    # Logical Operators
    t_LOR            = r'\|\|'
    t_LAND           = r'&&'
    t_LNOT           = r'!'

    # Bitwise Operators
    t_BOR            = r'\|'
    t_BAND           = r'&'
    t_BNOT           = r'~'
    t_BXOR           = r'\^'
    t_LSHIFT         = r'<<'
    t_RSHIFT         = r'>>'

    # Equality Operators
    t_LT             = r'<'
    t_GT             = r'>'
    t_LE             = r'<='
    t_GE             = r'>='
    t_EQ             = r'=='
    t_NE             = r'!='
    t_CMP            = r'<=>'
    t_TERNARY_CONDOP = r'\?'

    # String Equality Operators
    t_STRLT          = r'lt'
    t_STRGT          = r'gt'
    t_STRLE          = r'le'
    t_STRGE          = r'ge'
    t_STREQ          = r'eq'
    t_STRNE          = r'ne'
    t_STRCMP         = r'cmp'

    # Assignment Operators
    t_EQUALS         = r'='
    t_PLUSEQUAL      = r'\+='
    t_MINUSEQUAL     = r'-='
    t_TIMESEQUAL     = r'\*='
    t_DIVEQUAL       = r'/='
    t_MODEQUAL       = r'%='
    t_EXPEQUAL       = r'\*\*='
    t_LSHIFTEQUAL    = r'<<='
    t_RSHIFTEQUAL    = r'>>='
    t_ANDEQUAL       = r'&='
    t_XOREQUAL       = r'\^='
    t_OREQUAL        = r'\|='

    # Miscellaneous Operators
    t_DOT            = r'\.'
    t_RANGE          = r'\.\.'
    t_INC            = r'\+\+'
    t_DEC            = r'--'
    t_ARROW          = r'->'
    t_HASHARROW      = r'=>'

    t_LPAREN         = r'\('
    t_RPAREN         = r'\)'
    t_LBLOCK         = r'\{'
    t_RBLOCK         = r'\}'
    t_LBRACKET	     = r'\['
    t_RBRACKET	     = r'\]'
    t_SEMICOLON      = r';'
    t_COLON	     = r':'
    t_COMMA	     = r','

    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore  = ' \t'

    # Error handling rule
    def t_error(self, t):
        print("Illegal character '%s' at line %d" % (t.value[0], t.lexer.lineno))
        sys.exit(1) # Exit without traceback

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

    def prettyPrintTokenFreq(self):
        occurDict  = {}
        lexemeDict = {}

        for tok in self.lexer:
            lexemeDict[tok.type] = lexemeDict.get(tok.type, []) + [tok.value]
            occurDict[tok.type] = occurDict.get(tok.type, 0) + 1;
        
        # Heading
        print '#'*45
        print '{:<20} | {:<12} | {}'.format("Token", "Occurences", "Lexemes")
        print '#'*45

        lexemeDict = {i : list(set(lexemeDict[i])) for i in lexemeDict}
        for tok in lexemeDict:
            lexemeList = lexemeDict[tok]
            print '{:<20} | {:<12} | {}'.format(str(tok), str(occurDict[tok]), lexemeList[0])
            for j in xrange(1, len(lexemeList)):
                print '{:<20} | {:<12} | {}'.format("", "",  lexemeList[j])
	    print '-'*45
