import ply.yacc as yacc

class Parser(object):

    precedence = (
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'BOR', 'BXOR'),
        ('left', 'BAND'),
        ('nonassoc', 'EQ', 'NE', 'CMP', 'STREQ', 'STRNE', 'STRCMP'),
        ('nonassoc', 'LT', 'GT', 'LE', 'GE', 'STRLT', 'STRGT', 'STRLE', 'STRGE'),
        ('left', 'LSHIFT', 'RSHIFT'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES','DIVIDE', 'MODULUS'),
        ('right', 'EXPONENT'),
    )

    def p_statements(self, p):
        ''' statements : statement statements
                       | statement
        '''

    def p_codeblock(self, p):
        ''' codeblock : LBLOCK statements RBLOCK '''

    def p_empty(self, p):
        ''' empty : '''

    def p_statement(self, p):
        ''' statement : assignment SEMICOLON
                      | branch 
                      | loop
        '''

    # assignment -> empty is the no assignment. Can be used in init of for loops
    def p_assignment(self, p):
        ''' assignment : var assign-sep expression
                       | var assign-sep expression COMMA assignment
                       | empty
        '''

    def p_assign_sep(self, p):
        ''' assign-sep : EQUALS
                       | TIMESEQUAL
                       | DIVEQUAL
                       | MODEQUAL
                       | PLUSEQUAL
                       | MINUSEQUAL
                       | LSHIFTEQUAL
                       | RSHIFTEQUAL
                       | ANDEQUAL
                       | XOREQUAL
                       | OREQUAL
                       | EXPEQUAL
        '''

    def p_expression(self, p):
        ''' expression : LPAREN expression RPAREN
                       | expression PLUS expression
                       | expression MINUS expression
                       | expression TIMES expression
                       | expression DIVIDE expression
                       | expression MODULUS expression
                       | expression EXPONENT expression
                       | expression BOR expression
                       | expression BAND expression
                       | expression BXOR expression
                       | expression LSHIFT expression
                       | expression RSHIFT expression
                       | function-call
                       | var
                       | const
        '''

    # Add parentheses to this
    def p_condition(self, p):
        ''' condition : LPAREN condition RPAREN
                      | condition AND condition
                      | condition OR condition
                      | expression LT expression
                      | expression GT expression
                      | expression LE expression
                      | expression GE expression
                      | expression EQ expression
                      | expression NE expression
                      | expression CMP expression
                      | expression STRLT expression
                      | expression STRGT expression
                      | expression STRLE expression
                      | expression STRGE expression
                      | expression STREQ expression
                      | expression STRNE expression
                      | expression STRCMP expression
        '''

    def p_branch(self, p):
        ''' branch : if-elsif-else
                   | unless
        '''

    def p_if_elsif_else(self, p):
        ''' if-elsif-else : if-elsif else '''

    def p_if_elsif(self, p):
        ''' if-elsif : IF LPAREN condition RPAREN codeblock elsif '''

    def p_elsif(self, p):
        ''' elsif : ELSIF LPAREN condition RPAREN codeblock elsif
                  | empty
        '''

    def p_else(self, p):
        ''' else : ELSE codeblock
                 | empty
        '''

    def p_unless(self, p):
        ''' unless : UNLESS LPAREN condition RPAREN codeblock elsif '''

    # Foreach-loop semantics need to be good
    def p_loop(self, p):
        ''' loop : WHILE LPAREN condition RPAREN codeblock
                 | UNTIL LPAREN condition RPAREN codeblock
                 | FOR LPAREN assignment SEMICOLON condition SEMICOLON assignment RPAREN codeblock
                 | FOREACH var LPAREN var RPAREN codeblock
                 | DO codeblock WHILE LPAREN condition RPAREN SEMICOLON
        '''

    # Need to handle many other cases
    def p_variable(self, p):
        ''' var : VARIABLE
                | REFERENCE
                | DEREFERENCE
        '''

    # Need to handle many other cases
    def p_constant(self, p):
        ''' const : numeric
                  | SINGQUOTSTR
                  | DOUBQUOTSTR
        '''

    def p_numeric(self, p):
        ''' numeric : NUMBER
                    | BINARY
                    | OCTAL
                    | HEXADECIMAL
        '''

    def p_function_call(self, p):
        ''' function-call : ID LPAREN expression RPAREN '''

    def p_function_def(self, p):
        ''' function-def : SUB ID codeblock '''

    # Error rule for syntax errors
    def p_error(self, p):
        print("Syntax error in input!")

    # Build the parser
    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)

    # Set the token map which is obtained from the lexer
    def set_tokens(self, tokens):
        self.tokens = tokens

    # A wrapper
    def parse(self, input):
        return self.parser.parse(input)