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

    def p_start_state(self, p):
        ''' start-state : statements '''
        p[0] = ('start-state', self.get_children(p))
        if self.error_seen is False:
            self.gen_rightmost(p[0])

    def p_statements(self, p):
        ''' statements : statement statements
                       | statement
        '''
        p[0] = ('statements', self.get_children(p))

    def p_codeblock(self, p):
        ''' codeblock : LBLOCK statements RBLOCK '''
        p[0] = ('codeblock', self.get_children(p))

    def p_codeblock_error(self, p):
        ''' codeblock : LBLOCK error RBLOCK
        '''
        start, end = p.linespan(2)
        starti, endi = p.lexspan(2)
        self.error_seen = True
        print "Error in statement from Line %d, Column %d to Line %d, Column %d"%(start, end, starti, endi)

    def p_empty(self, p):
        ''' empty : '''
        p[0] = ('empty', self.get_children(p))

    def p_statement(self, p):
        ''' statement : expression SEMICOLON
                      | function-def
                      | function-ret SEMICOLON
                      | branch 
                      | loop
                      | labelled-loop
                      | loop-control SEMICOLON
        '''
        p[0] = ('statement', self.get_children(p))

    def p_statement_error(self, p):
        ''' statement : error SEMICOLON
        '''
        start, end = p.linespan(1)
        starti, endi = p.lexspan(1)
        self.error_seen = True
        print "Error in statement from Line %d, Column %d to Line %d, Column %d"%(start, end, starti, endi)

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
        p[0] = ('assign-sep', self.get_children(p))

    # (expression -> var assign-sep expression) corresponds to scalar assignment expression
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
        p[0] = ('expression', self.get_children(p))

    def p_branch(self, p):
        ''' branch : if-elsif-else
                   | unless
        '''
        p[0] = ('branch', self.get_children(p))

    def p_if_elsif_else(self, p):
        ''' if-elsif-else : if-elsif else '''
        p[0] = ('if-elsif-else', self.get_children(p))

    def p_if_elsif(self, p):
        ''' if-elsif : IF LPAREN expression RPAREN codeblock elsif '''
        p[0] = ('if-elsif', self.get_children(p))

    def p_if_elsif_error(self, p):
        ''' if-elsif : IF LPAREN error RPAREN codeblock elsif '''
        start, end = p.linespan(3)
        starti, endi = p.lexspan(3)
        self.error_seen = True
        print "Error in statement from Line %d, Column %d to Line %d, Column %d"%(start, end, starti, endi)

    def p_elsif(self, p):
        ''' elsif : ELSIF LPAREN expression RPAREN codeblock elsif
                  | empty
        '''
        p[0] = ('elsif', self.get_children(p))

    def p_elsif_error(self, p):
        ''' elsif : ELSIF LPAREN error RPAREN codeblock elsif
        '''
        start, end = p.linespan(3)
        starti, endi = p.lexspan(3)
        self.error_seen = True
        print "Error in statement from Line %d, Column %d to Line %d, Column %d"%(start, end, starti, endi)

    def p_else(self, p):
        ''' else : ELSE codeblock
                 | empty
        '''
        p[0] = ('else', self.get_children(p))

    def p_unless(self, p):
        ''' unless : UNLESS LPAREN expression RPAREN codeblock elsif else '''
        p[0] = ('unless', self.get_children(p))

    def p_unless_error(self, p):
        ''' unless : UNLESS LPAREN error RPAREN codeblock elsif else '''
        start, end = p.linespan(3)
        starti, endi = p.lexspan(3)
        self.error_seen = True
        print "Error in statement from Line %d, Column %d to Line %d, Column %d"%(start, end, starti, endi)

    def p_continue_block(self, p):
        ''' continue : CONTINUE codeblock
                     | empty
        '''
        p[0] = ('continue', self.get_children(p))

    # Foreach-loop semantics need to be good
    def p_loop(self, p):
        ''' loop : WHILE LPAREN expression RPAREN codeblock continue
                 | UNTIL LPAREN expression RPAREN codeblock
                 | FOR LPAREN expression SEMICOLON expression SEMICOLON expression RPAREN codeblock
                 | FOREACH var LPAREN var RPAREN codeblock continue
                 | DO codeblock WHILE LPAREN expression RPAREN SEMICOLON
        '''
        p[0] = ('loop', self.get_children(p))

    def p_loop_error_a(self, p):
        ''' loop : WHILE LPAREN error RPAREN codeblock continue
                 | UNTIL LPAREN error RPAREN codeblock
                 | FOR LPAREN error RPAREN codeblock
        '''
        start, end = p.linespan(3)
        starti, endi = p.lexspan(3)
        self.error_seen = True
        print "Error in statement from Line %d, Column %d to Line %d, Column %d"%(start, end, starti, endi)

    def p_loop_error_b(self, p):
        ''' loop : FOREACH var LPAREN error RPAREN codeblock continue
        '''
        start, end = p.linespan(4)
        starti, endi = p.lexspan(4)
        self.error_seen = True
        print "Error in statement from Line %d, Column %d to Line %d, Column %d"%(start, end, starti, endi)

    def p_loop_error_c(self, p):
        ''' loop : DO codeblock WHILE LPAREN error RPAREN SEMICOLON
        '''
        start, end = p.linespan(5)
        starti, endi = p.lexspan(5)
        self.error_seen = True
        print "Error in statement from Line %d, Column %d to Line %d, Column %d"%(start, end, starti, endi)

    def p_labelled_loop(self, p):
        ''' labelled-loop : ID COLON loop '''
        p[0] = ('labelled-loop', self.get_children(p))

    def p_loop_control_statement(self, p):
        ''' loop-control : NEXT
                         | NEXT ID
                         | LAST 
                         | LAST ID
                         | REDO
                         | REDO ID
                         | GOTO ID
        '''
        p[0] = ('loop-control', self.get_children(p))

    def p_variable_name(self, p):
        ''' var-name : VARIABLE
                     | REFERENCE
                     | DEREFERENCE
        '''
        p[0] = ('var-name', self.get_children(p))

    # For array and hash access
    def p_access(self, p):
        ''' access : LBRACKET expression RBRACKET
                   | LBLOCK expression RBLOCK
        '''
        p[0] = ('access', self.get_children(p))

    def p_access_error(self, p):
        ''' access : LBRACKET error RBRACKET
                   | LBLOCK error RBLOCK
        '''
        start, end = p.linespan(2)
        starti, endi = p.lexspan(2)
        self.error_seen = True
        print "Error in statement from Line %d, Column %d to Line %d, Column %d"%(start, end, starti, endi)

    # ARROW is used as follows with references
    #   $arrayref->[0] = "January";   # Array element
    #   $hashref->{"KEY"} = "VALUE";  # Hash element
    def p_variable(self, p):
        ''' var : var-name
                | var ARROW access
                | var access
        '''
        p[0] = ('var', self.get_children(p))
        # Needs verification

    def p_constant(self, p):
        ''' const : numeric
                  | SINGQUOTSTR
                  | DOUBQUOTSTR
        '''
        p[0] = ('const', self.get_children(p))

    def p_numeric(self, p):
        ''' numeric : NUMBER
                    | BINARY
                    | OCTAL
                    | HEXADECIMAL
        '''
        p[0] = ('numeric', self.get_children(p))

    def p_builtin_function(self, p):
        ''' builtin-func : PRINTF
                         | PRINT
                         | KEYS
                         | VALUES
                         | EXISTS
                         | DELETE
        '''
        p[0] = ('builtin-func', self.get_children(p))

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
        p[0] = ('function-call', self.get_children(p))

    def p_function_def(self, p):
        ''' function-def : SUB ID codeblock '''
        p[0] = ('function-def', self.get_children(p))

    def p_function_return(self, p):
        ''' function-ret : RETURN expression '''
        p[0] = ('function-ret', self.get_children(p))

    def p_ternary_operator(self, p):
        ''' ternary-op : expression TERNARY_CONDOP expression COLON expression '''
        p[0] = ('ternary-op', self.get_children(p))

    # Build the parser
    # error_seen decides if we should print the .html file or not at the end
    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)
        self.error_seen = False

    # Set the token map which is obtained from the lexer
    def set_tokens(self, tokens):
        self.tokens = tokens

    # A wrapper
    def parse(self, input, output_file):
        self.output_file = output_file
        return self.parser.parse(input, tracking=True)

    def get_children(self, p):
        children = []
        for i in xrange(1,len(p)):
            children.append(p[i])
        return children

    def gen_rightmost(self, ast):
        filePtr = open(self.output_file, 'w')
        filePtr.write("<html><body>\n")
        left_symbols = [ast]
        right_derived = []
        while left_symbols:
            while left_symbols and type(left_symbols[-1]) is not tuple:
                right_derived.append(left_symbols.pop())

            if left_symbols:
                reduce_nt = left_symbols.pop()
                for sym in left_symbols:
                    if type(sym) is tuple:
                        filePtr.write(str(sym[0])+" ")
                    else:
                        filePtr.write(str(sym)+" ")
                filePtr.write("<b> "+str(reduce_nt[0])+" </b>\n")
                left_symbols += reduce_nt[1]

            for term in reversed(right_derived):
                if type(term) is tuple:
                    filePtr.write(str(term[0])+" ")
                else:
                    filePtr.write(str(term)+" ")
            filePtr.write("<br><br><br>\n")
        filePtr.write("</body></html>\n")
        filePtr.close()
