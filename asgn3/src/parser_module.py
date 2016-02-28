import ply.yacc as yacc

class Parser(object):

    precedence = (
        ('left', 'OR', 'XOR'),
        ('left', 'AND'),
        ('right', 'NOT'),
        ('left', 'COMMA', 'HASHARROW'),
        ('right', 'EQUALS', 'TIMESEQUAL', 'DIVEQUAL', 'MODEQUAL', 'PLUSEQUAL', 'MINUSEQUAL',
                  'LSHIFTEQUAL','RSHIFTEQUAL', 'ANDEQUAL', 'XOREQUAL', 'OREQUAL', 'EXPEQUAL'),
        ('right', 'TERNARY_CONDOP', 'COLON'),
        ('nonassoc', 'RANGE'),
        ('left', 'LOR'),
        ('left', 'LAND'),
        ('left', 'BOR', 'BXOR'),
        ('left', 'BAND'),
        ('nonassoc', 'EQ', 'NE', 'CMP', 'STREQ', 'STRNE', 'STRCMP'),
        ('nonassoc', 'LT', 'GT', 'LE', 'GE', 'STRLT', 'STRGT', 'STRLE', 'STRGE'),
        ('left', 'LSHIFT', 'RSHIFT'),
        ('left', 'PLUS', 'MINUS', 'DOT'),
        ('left', 'TIMES','DIVIDE', 'MODULUS', 'REPEAT'),
        ('right', 'BNOT', 'LNOT'),
        ('right', 'EXPONENT'),
        ('nonassoc', 'INC', 'DEC'),
        ('left', 'ARROW'),
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
        ''' statement : expression SEMICOLON
                      | function-def
                      | function-ret SEMICOLON
                      | branch 
                      | loop
                      | labelled-loop
                      | loop-control SEMICOLON
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

    # (expression -> var assign-sep expression) corresponds to scalar assignment expression
    # (expression -> var EQUALS LPAREN expression RPAREN) corresponds to array and hash assignment expressions
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
                       | expression DOT expression
                       | expression REPEAT expression
                       | expression HASHARROW expression
                       | expression RANGE expression
                       | BNOT expression

                       | expression LAND expression
                       | expression AND expression
                       | expression LOR expression
                       | expression OR expression
                       | expression XOR expression
                       | LNOT expression
                       | NOT expression

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

                       | var INC
                       | INC var
                       | var DEC
                       | DEC var
                       | MINUS expression
                       | PLUS expression

                       | expression COMMA expression
                       | expression COMMA empty
                       | ternary-op

                       | function-call
                       | const
                       | var

                       | var assign-sep expression %prec EQUALS
        '''

    def p_branch(self, p):
        ''' branch : if-elsif-else
                   | unless
        '''

    def p_if_elsif_else(self, p):
        ''' if-elsif-else : if-elsif else '''

    def p_if_elsif(self, p):
        ''' if-elsif : IF LPAREN expression RPAREN codeblock elsif '''

    def p_elsif(self, p):
        ''' elsif : ELSIF LPAREN expression RPAREN codeblock elsif
                  | empty
        '''

    def p_else(self, p):
        ''' else : ELSE codeblock
                 | empty
        '''

    def p_unless(self, p):
        ''' unless : UNLESS LPAREN expression RPAREN codeblock elsif else '''

    def p_continue_block(self, p):
        ''' continue : CONTINUE codeblock
                     | empty
        '''

    # Foreach-loop semantics need to be good
    def p_loop(self, p):
        ''' loop : WHILE LPAREN expression RPAREN codeblock continue
                 | UNTIL LPAREN expression RPAREN codeblock
                 | FOR LPAREN expression SEMICOLON expression SEMICOLON expression RPAREN codeblock
                 | FOREACH var LPAREN var RPAREN codeblock continue
                 | DO codeblock WHILE LPAREN expression RPAREN SEMICOLON
        '''

    def p_labelled_loop(self, p):
        ''' labelled-loop : ID COLON loop '''

    def p_loop_control_statement(self, p):
        ''' loop-control : NEXT
                         | NEXT ID
                         | LAST 
                         | LAST ID
                         | REDO
                         | REDO ID
                         | GOTO ID
        '''

    def p_variable_name(self, p):
        ''' var-name : VARIABLE
                     | REFERENCE
                     | DEREFERENCE
        '''

    # For array and hash access
    def p_access(self, p):
        ''' access : LBRACKET expression RBRACKET
                   | LBLOCK expression RBLOCK
        '''

    # ARROW is used as follows with references
    #   $arrayref->[0] = "January";   # Array element
    #   $hashref->{"KEY"} = "VALUE";  # Hash element
    def p_variable(self, p):
        ''' var : var-name
                | var ARROW access
                | var access
        '''
        # Needs verification

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

    def p_builtin_function(self, p):
        ''' builtin-func : PRINTF
                         | PRINT
                         | KEYS
                         | VALUES
                         | EXISTS
                         | DELETE
        '''

    # In Perl, built-in functions or functions which are declared before 
    # calling can be called without parentheses. For now, our implementation
    # of function calls necessarily requires parentheses to be supplied for all
    # functions except the builtin ones. They may be called without parentheses.
    def p_function_call(self, p):
        ''' function-call : ID LPAREN expression RPAREN
                          | ID LPAREN RPAREN
                          | builtin-func LPAREN RPAREN
                          | builtin-func expression %prec COMMA
        '''
        # This has gotten messy. We should handle this more cleanly.

    def p_function_def(self, p):
        ''' function-def : SUB ID codeblock '''

    def p_function_return(self, p):
        ''' function-ret : RETURN expression '''

    def p_ternary_operator(self, p):
        ''' ternary-op : expression TERNARY_CONDOP expression COLON expression '''

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
