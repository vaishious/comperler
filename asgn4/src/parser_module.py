import ply.yacc as yacc
import symbol_table as SYMTAB
import ir_generation as IR
import debug as DEBUG

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
        if self.error_seen:
            self.error_list.sort()
            for error_item in self.error_list:
                print error_item[1]

    def p_statements(self, p):
        ''' statements : statement statements
                       | statement
        '''
        p[0] = ('statements', self.get_children(p))
        
    def p_mark_newscope(self, p):
        ''' MARK-newscope : '''
        
        self.symTabManager.PushScope()

    def p_codeblock(self, p):
        ''' codeblock : MARK-newscope LBLOCK statements RBLOCK '''
        p[0] = ('codeblock', self.get_children(p))

        self.symTabManager.PopScope()

    def p_codeblock_error(self, p):
        ''' codeblock : MARK-newscope LBLOCK error RBLOCK
        '''
        self.error_list.append((p.lineno(3), "Error in code block starting at line %d and ending at line %d"%(p.lineno(1), p.lineno(3))))

    def p_empty(self, p):
        ''' empty : '''
        p[0] = ('empty', self.get_children(p))

    def p_statement(self, p):
        ''' statement : expression SEMICOLON
                      | variable-strict-decl SEMICOLON
                      | codeblock
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
        self.error_list.append((p.lineno(1), "Line %d: Invalid statement"%(p.lineno(1))))

    def p_error(self, p):
        if not self.error_seen:
            print("Syntax error in input.")
            self.error_seen = True

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

    def p_binary_op(self, p):
        ''' binary-op : expression PLUS expression 
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
                      | expression LAND expression
                      | expression AND expression
                      | expression LOR expression
                      | expression OR expression
                      | expression XOR expression

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

        p[0] = ('binary-op', self.get_children(p))

    # (expression -> var assign-sep expression) corresponds to scalar assignment expression
    def p_expression(self, p):
        ''' expression : LPAREN expression RPAREN
                       | binary-op
                       | expression DOT expression
                       | expression REPEAT expression
                       | expression HASHARROW expression
                       | expression RANGE expression
                       | BNOT expression

                       | LNOT expression
                       | NOT expression

                       | var-lhs MARK-check-declaration INC 
                       | INC var-lhs MARK-check-declaration
                       | var-lhs MARK-check-declaration DEC
                       | DEC var-lhs MARK-check-declaration
                       | MINUS expression
                       | PLUS expression

                       | expression COMMA expression
                       | expression COMMA empty
                       | ternary-op

                       | function-call
                       | const
                       | var MARK-check-declaration

                       | global-assignment
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
        self.error_list.append((p.lineno(3), "Line %d: Invalid conditional passed to IF"%(p.lineno(3))))

    def p_elsif(self, p):
        ''' elsif : ELSIF LPAREN expression RPAREN codeblock elsif
                  | empty
        '''
        p[0] = ('elsif', self.get_children(p))

    def p_elsif_error(self, p):
        ''' elsif : ELSIF LPAREN error RPAREN codeblock elsif
        '''
        self.error_list.append((p.lineno(3), "Line %d: Invalid conditional passed to ELSIF"%(p.lineno(3))))

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
        self.error_list.append((p.lineno(3), "Line %d: Invalid conditional passed to UNLESS"%(p.lineno(3))))

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
                 | FOREACH var-lhs LPAREN var-lhs RPAREN codeblock continue
                 | DO codeblock WHILE LPAREN expression RPAREN SEMICOLON
        '''
        p[0] = ('loop', self.get_children(p))

    def p_loop_error_a(self, p):
        ''' loop : WHILE LPAREN error RPAREN codeblock continue
                 | UNTIL LPAREN error RPAREN codeblock
                 | FOR LPAREN error RPAREN codeblock
        '''
        if p[1] == 'while':
            self.error_list.append((p.lineno(3), "Line %d: Invalid conditional passed to WHILE loop"%(p.lineno(3))))
        elif p[1] == 'until':
            self.error_list.append((p.lineno(3), "Line %d: Invalid conditional passed to UNTIL loop"%(p.lineno(3))))
        elif p[1] == 'for':
            self.error_list.append((p.lineno(3), "Line %d: Invalid conditional passed to FOR loop"%(p.lineno(3))))

    def p_loop_error_b(self, p):
        ''' loop : FOREACH var-lhs LPAREN error RPAREN codeblock continue
        '''
        self.error_list.append((p.lineno(4), "Line %d: Invalid conditional passed to FOREACH loop"%(p.lineno(4))))

    def p_loop_error_c(self, p):
        ''' loop : DO codeblock WHILE LPAREN error RPAREN SEMICOLON
        '''
        self.error_list.append((p.lineno(5), "Line %d: Invalid conditional passed to DO-WHILE loop"%(p.lineno(5))))

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

    def p_variable_name_lhs_strict(self, p):
        ''' var-name-lhs-strict : VARIABLE '''

        p[0] = self.symTabManager.Lookup(p[1])

    def p_variable_name_lhs(self, p):
        ''' var-name-lhs : var-name-lhs-strict
                         | DEREFERENCE
        '''

        if type(p[1]) != SYMTAB.SymTabEntry:
            # Is a dereference
            strippedVarName = p[1][1:]
            derefDepth = strippedVarName.count('$')
            strippedVarName = '$' + strippedVarName[derefDepth:]

            if p[1][0] == '$'   : externalType = SYMTAB.SymTabEntry.SCALAR
            elif p[1][0] == '@' : externalType = SYMTAB.SymTabEntry.ARRAY
            elif p[1][0] == '%' : externalType = SYMTAB.SymTabEntry.HASH

            tabEntry = self.symTabManager.Lookup(strippedVarName)

            p[0] = IR.Dereference(tabEntry, externalType, derefDepth)

        else:
            p[0] = p[1]

    # For array and hash access
    def p_access(self, p):
        ''' access : LBRACKET expression RBRACKET
                   | LBLOCK expression RBLOCK
        '''

        if p[1] == '{':
            accessType = SYMTAB.SymTabEntry.HASH
        elif p[1] == "[":
            accessType = SYMTAB.SymTabEntry.ARRAY

        # LHS is defined later
        p[0] = IR.AccessOp(None, p[2], accessType)
 
    def p_access_error(self, p):
        ''' access : LBRACKET error RBRACKET
                   | LBLOCK error RBLOCK
        '''
        if p[1] == '[':
            self.error_list.append((p.lineno(2), "Line %d: Invalid array access token"%(p.lineno(2))))
        elif p[1] == '{':
            self.error_list.append((p.lineno(2), "Line %d: Invalid hash access token"%(p.lineno(2))))

    # ARROW is used as follows with references
    #   $arrayref->[0] = "January";   # Array element
    #   $hashref->{"KEY"} = "VALUE";  # Hash element

    def p_variable_arrows_and_accesses(self, p):
        ''' arrows_and_accesses : ARROW access
                                | access
        '''

        if len(p) == 2:
            if type(p[-1]) == SYMTAB.SymTabEntry:
                # Have to take corrective measures
                if p[1].accessType == SYMTAB.SymTabEntry.HASH : newVarName = '%' + p[-1].baseVarName 
                else : newVarName = '@' + p[-1].baseVarName

                p[-1] = self.SymTabManager.Lookup(newVarName)

                p[1].lhs = p[-1]
                p[0] = p[1]
        else:
            if p[-1].externalType != SYMTAB.SymTabEntry.SCALAR:
                raise PerlTypeError("Dereferenced object must be a scalar value")

            p[2].lhs = IR.ArrowOp(p[-1])
            p[0] = p[2]

    def p_variable_lhs(self, p):
        ''' var-lhs : var-name-lhs
                    | var-name-lhs arrows_and_accesses
        '''

        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[2]

    def p_variable(self, p):
        ''' var : var-lhs
                | REFERENCE 
        '''

        if type(p[1]) == str:
            # Is a reference

            tabEntry = self.symTabManager.Lookup(p[1][1:])
            p[0] = IR.Reference(tabEntry)

        else:
            p[0] = p[1]

    def p_mark_check_declaration(self, p):
        ''' MARK-check-declaration : '''

        if not p[-1].CheckDeclaration():
            raise DEBUG.PerlNameError(str(p[-1]) + " not defined")

    def p_global_assignment(self, p):
        ''' global-assignment : var-lhs assign-sep expression %prec EQUALS '''
        
        p[1].InsertGlobally(self.symTabManager)

    def p_variable_strict_decl(self, p):
        ''' variable-strict-decl : MY var-name-lhs-strict
                                 | MY var-name-lhs-strict assign-sep expression
        '''

        p[2].InsertLocally(self.symTabManager)

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

    # Our implementation of function calls necessarily requires parentheses
    # to be supplied for all functions.
    def p_function_call(self, p):
        ''' function-call : ID LPAREN expression RPAREN
                          | ID LPAREN RPAREN
                          | builtin-func LPAREN expression RPAREN
                          | builtin-func LPAREN RPAREN
        '''
        p[0] = ('function-call', self.get_children(p))

    def p_function_call_error(self, p):
        ''' function-call : ID LPAREN error RPAREN
                          | builtin-func LPAREN error RPAREN
        '''
        self.error_list.append((p.lineno(3), "Line %d: Invalid expression passed to function call"%(p.lineno(3))))

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
        self.error_list = []

    # Set the token map which is obtained from the lexer
    def set_tokens(self, tokens):
        self.tokens = tokens

    # A wrapper
    def parse(self, input, output_file):
        self.output_file = output_file
        self.symTabManager = SYMTAB.SymTabManager()
        self.symTabManager.PushScope()
        return self.parser.parse(input)

    def get_children(self, p):
        children = []
        for i in xrange(1,len(p)):
            children.append(p[i])
        return children
