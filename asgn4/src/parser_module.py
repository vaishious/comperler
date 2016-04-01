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
        if self.error_seen:
            self.error_list.sort()
            for error_item in self.error_list:
                print error_item[1]
        else:
            IR.BackPatch(p[1].nextlist, IR.NextInstr)
            p[1].code.PrintIR()

    ### Special Rules ###

    def p_empty(self, p):
        ''' empty : '''
        p[0] = ('empty', self.get_children(p))

    def p_error(self, p):
        if not self.error_seen:
            print("Syntax error in input.")
            self.error_seen = True

    ##################################
    
    ### Marker Symbols ###

    def p_mark_newscope(self, p):
        ''' MARK-newscope : '''
        
        self.symTabManager.PushScope()

    def p_mark_check_declaration(self, p):
        ''' MARK-check-declaration : '''

        if not p[-1].symEntry.CheckDeclaration():
            raise DEBUG.PerlNameError("Variable %s not defined"%(p[-1].symEntry.baseVarName))

    ##################################

    def p_statements(self, p):
        ''' statements : statements MARK-backpatch statement
                       | statement
        '''

        p[0] = IR.Attributes()

        if len(p) == 2:
            p[0].code = p[1].code
            p[0].nextlist = p[1].nextlist
        else:
            p[0].code = p[1].code | p[3].code
            IR.BackPatch(p[1].nextlist, p[2].instr)
            p[0].nextlist = p[3].nextlist

    def p_loop_statements(self, p):
        ''' loop-statements : loop-statements MARK-backpatch loop-statement
                            | loop-statement
        '''

        p[0] = IR.Attributes()

        if len(p) == 2:
            p[0].code = p[1].code
            p[0].nextlist = p[1].nextlist
            p[0].loop_next_list = p[1].loop_next_list
            p[0].loop_redo_list = p[1].loop_redo_list
            p[0].loop_last_list = p[1].loop_last_list
        else:
            p[0].code = p[1].code | p[3].code
            IR.BackPatch(p[1].nextlist, p[2].instr)
            p[0].nextlist = p[3].nextlist

            p[0].loop_next_list = IR.MergeLoopLists(p[1].loop_next_list, p[3].loop_next_list)
            p[0].loop_redo_list = IR.MergeLoopLists(p[1].loop_redo_list, p[3].loop_redo_list)
            p[0].loop_last_list = IR.MergeLoopLists(p[1].loop_last_list, p[3].loop_last_list)
 
    def p_statement(self, p):
        ''' statement : expression SEMICOLON
                      | variable-strict-decl SEMICOLON
                      | codeblock
                      | function-def
                      | function-ret SEMICOLON
                      | branch 
                      | labelled-loop
        '''

        p[0] = p[1]

    def p_loop_statement(self, p):
        ''' loop-statement : statement
                           | loop-control SEMICOLON
        '''

        p[0] = p[1]

    def p_statement_error(self, p):
        ''' statement : error SEMICOLON
        '''
        self.error_list.append((p.lineno(1), "Line %d: Invalid statement"%(p.lineno(1))))       


    def p_codeblock(self, p):
        ''' codeblock : MARK-newscope LBLOCK statements RBLOCK '''

        p[0] = p[3]

        self.symTabManager.PopScope()

    def p_loop_codeblock(self, p):
        ''' loop-codeblock : MARK-newscope LBLOCK loop-statements RBLOCK '''

        p[0] = p[3]

        self.symTabManager.PopScope()

    def p_codeblock_error(self, p):
        ''' codeblock : MARK-newscope LBLOCK error RBLOCK
        '''
        self.error_list.append((p.lineno(3), "Error in code block starting at line %d and ending at line %d"%(p.lineno(1), p.lineno(3))))

    def p_expression(self, p):
        ''' expression : usable-expression
                       | normal-assignment
                       | ternary-op
        '''

        p[0] = p[1]

    def p_usable_expression(self, p):
        ''' usable-expression : arith-bool-string-expression
                              | list-expression
                              | hash-expression
        '''

        p[0] = p[1]

    def p_list_expression(self, p):
        ''' list-expression : LPAREN list-elements RPAREN '''

    def p_list_elements(self, p):
        ''' list-elements : arith-bool-string-expression COMMA list-elements
                          | arith-bool-string-expression COMMA
        '''

    def p_hash_expression(self, p):
        ''' hash-expression : LPAREN hash-elements RPAREN '''

    def p_hash_elements(self, p):
        ''' hash-elements : arith-bool-string-expression HASHARROW arith-bool-string-expression COMMA hash-elements
                          | arith-bool-string-expression HASHARROW arith-bool-string-expression
        '''

    def p_arith_bool_string_expression(self, p):
        ''' arith-bool-string-expression : arith-boolean-expression
                                         | string-expression
                                         | var
        '''

        p[0] = p[1]

        if p[0].isBooleanExpression:
            p[0].place = IR.TempVar()

            IR.BackPatch(p[0].truelist, IR.NextInstr)
            p[0].code = p[0].code | IR.GenCode("=, %s, 1"%(p[0].place))

            IR.BackPatch(p[1].falselist, IR.NextInstr)
            p[0].code = p[0].code | IR.GenCode("=, %s, 0"%(p[0].place))

    def p_arith_expression(self, p):
        ''' arith-expression : numeric
                             | arith-unary-op
                             | arith-binary-op
                             | arith-increment-decrement
                             | LPAREN arith-expression RPAREN
                             | LPAREN var RPAREN
        '''

        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[2]

    def p_arith_boolean_expression(self, p):
        ''' arith-boolean-expression : arith-expression
                                     | boolean-expression
        '''

        p[0] = p[1]

    def p_string_expression(self, p):
        ''' string-expression : string
                              | string-op
                              | LPAREN string-expression RPAREN
        '''

        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[2]


    def p_arith_unary_op(self, p):
        ''' arith-unary-op : MINUS arith-boolean-expression 
                           | PLUS arith-boolean-expression
                           | BNOT arith-boolean-expression
                           | MINUS var
                           | PLUS var
                           | BNOT var
        '''

        p[0] = IR.Attributes()

        p[0].place = TempVar()
        p[0].code = p[2].code | IR.GenCode("=, %s, %s, %s"%(p[1], p[0].place, p[2].place))

    def p_arith_increment_decrement(self, p):
        ''' arith-increment-decrement : var-lhs MARK-check-declaration INC 
                                      | INC var-lhs MARK-check-declaration
                                      | var-lhs MARK-check-declaration DEC
                                      | DEC var-lhs MARK-check-declaration
        '''

        p[0] = IR.Attributes()
        if type(p[1] == IR.Attributes):

            p[0].place = IR.TempVar()
            p[0].code = IR.GenCode("=, %s, %s"%(p[0].place, p[1].place)) | IR.GenCode("=, %s, %s, %s, %s"%(p[3][0], p[1].place, p[1].place, "1"))

        else:

            p[0].place = p[2].place
            p[0].code = IR.GenCode("=, %s, %s, %s, %s"%(p[1][0], p[2].place, p[2].place, "1"))

    def p_arith_binary_op(self, p):
        ''' arith-binary-op : arith-boolean-expression PLUS arith-boolean-expression 
                            | arith-boolean-expression MINUS arith-boolean-expression 
                            | arith-boolean-expression TIMES arith-boolean-expression 
                            | arith-boolean-expression DIVIDE arith-boolean-expression 
                            | arith-boolean-expression MODULUS arith-boolean-expression 
                            | arith-boolean-expression EXPONENT arith-boolean-expression 
                            | arith-boolean-expression BOR arith-boolean-expression 
                            | arith-boolean-expression BAND arith-boolean-expression 
                            | arith-boolean-expression BXOR arith-boolean-expression
                            | arith-boolean-expression LSHIFT arith-boolean-expression
                            | arith-boolean-expression RSHIFT arith-boolean-expression
                            | arith-boolean-expression XOR arith-boolean-expression

                            | var PLUS var 
                            | var MINUS var 
                            | var TIMES var 
                            | var DIVIDE var 
                            | var MODULUS var 
                            | var EXPONENT var 
                            | var BOR var 
                            | var BAND var 
                            | var BXOR var
                            | var LSHIFT var
                            | var RSHIFT var
                            | var XOR var

                            | arith-boolean-expression PLUS var 
                            | arith-boolean-expression MINUS var 
                            | arith-boolean-expression TIMES var 
                            | arith-boolean-expression DIVIDE var 
                            | arith-boolean-expression MODULUS var 
                            | arith-boolean-expression EXPONENT var 
                            | arith-boolean-expression BOR var 
                            | arith-boolean-expression BAND var 
                            | arith-boolean-expression BXOR var
                            | arith-boolean-expression LSHIFT var
                            | arith-boolean-expression RSHIFT var
                            | arith-boolean-expression XOR var

                            | var PLUS arith-boolean-expression 
                            | var MINUS arith-boolean-expression 
                            | var TIMES arith-boolean-expression 
                            | var DIVIDE arith-boolean-expression 
                            | var MODULUS arith-boolean-expression 
                            | var EXPONENT arith-boolean-expression 
                            | var BOR arith-boolean-expression 
                            | var BAND arith-boolean-expression 
                            | var BXOR arith-boolean-expression
                            | var LSHIFT arith-boolean-expression
                            | var RSHIFT arith-boolean-expression
                            | var XOR arith-boolean-expression
        '''

        p[0] = IR.Attributes()

        p[0].place = IR.TempVar()
        p[0].code = p[1].code | p[3].code | IR.GenCode("=, %s, %s, %s, %s"%(p[2], p[0].place, p[1].place, p[3].place))

    def p_mark_backpatch(self, p):
        ''' MARK-backpatch : '''

        p[0] = IR.Attributes()

        p[0].instr = IR.NextInstr

    def p_mark_backpatch_special(self, p): # For use with AND/OR/NOT
        ''' MARK-backpatch-special : '''

        p[0] = IR.Attributes()

        if not p[-2].isBooleanExpression:
            p[-2].truelist = IR.MakeList(IR.NextInstr)
            p[-2].code = p[-2].code | IR.GenCode("ifgoto, !=, %s, 0, LABEL#REQUIRED"%(p[-2].place))

            p[-2].falselist = IR.MakeList(IR.NextInstr)
            p[-2].code = p[-2].code | IR.GenCode("goto, LABEL#REQUIRED")

        p[0].instr = IR.NextInstr

    def p_boolean_and(self, p):
        ''' boolean-and : arith-boolean-expression LAND MARK-backpatch-special arith-boolean-expression
                        | arith-boolean-expression AND MARK-backpatch-special arith-boolean-expression

                        | var LAND MARK-backpatch-special var
                        | var AND MARK-backpatch-special var

                        | var LAND MARK-backpatch-special arith-boolean-expression
                        | var AND MARK-backpatch-special arith-boolean-expression

                        | arith-boolean-expression LAND MARK-backpatch-special var
                        | arith-boolean-expression AND MARK-backpatch-special var
        '''

        p[0] = IR.Attributes()

        if not p[4].isBooleanExpression:
            p[4].truelist = IR.MakeList(IR.NextInstr)
            p[4].code = p[4].code | IR.GenCode("ifgoto, !=, %s, 0, LABEL#REQUIRED"%(p[4].place))

            p[4].falselist = IR.MakeList(IR.NextInstr)
            p[4].code = p[4].code | IR.GenCode("goto, LABEL#REQUIRED")

        IR.BackPatch(p[1].truelist, p[3].instr)
        p[0].truelist = p[4].truelist
        p[0].falselist = IR.Merge(p[4].falselist, p[1].falselist)

        p[0].code = p[1].code | p[4].code

    def p_boolean_or(self, p):
        ''' boolean-or  : arith-boolean-expression LOR MARK-backpatch-special arith-boolean-expression
                        | arith-boolean-expression OR MARK-backpatch-special arith-boolean-expression

                        | var LOR MARK-backpatch-special var
                        | var OR MARK-backpatch-special var

                        | var LOR MARK-backpatch-special arith-boolean-expression
                        | var OR MARK-backpatch-special arith-boolean-expression

                        | arith-boolean-expression LOR MARK-backpatch-special var
                        | arith-boolean-expression OR MARK-backpatch-special var
        '''

        p[0] = IR.Attributes()

        if not p[4].isBooleanExpression:
            p[4].truelist = IR.MakeList(IR.NextInstr)
            p[4].code = p[4].code | IR.GenCode("ifgoto, !=, %s, 0, LABEL#REQUIRED"%(p[4].place))

            p[4].falselist = IR.MakeList(IR.NextInstr)
            p[4].code = p[4].code | IR.GenCode("goto, LABEL#REQUIRED")

        IR.BackPatch(p[1].falselist, p[3].instr)
        p[0].truelist = IR.Merge(p[1].truelist, p[4].truelist)
        p[0].falselist = p[4].falselist

        p[0].code = p[1].code | p[4].code

    def p_relop(self, p):
        ''' boolean-relop : arith-boolean-expression LT arith-boolean-expression
                          | arith-boolean-expression GT arith-boolean-expression
                          | arith-boolean-expression LE arith-boolean-expression
                          | arith-boolean-expression GE arith-boolean-expression
                          | arith-boolean-expression EQ arith-boolean-expression
                          | arith-boolean-expression NE arith-boolean-expression
                          | arith-boolean-expression CMP arith-boolean-expression

                          | var LT var
                          | var GT var
                          | var LE var
                          | var GE var
                          | var EQ var
                          | var NE var
                          | var CMP var

                          | arith-boolean-expression LT var
                          | arith-boolean-expression GT var
                          | arith-boolean-expression LE var
                          | arith-boolean-expression GE var
                          | arith-boolean-expression EQ var
                          | arith-boolean-expression NE var
                          | arith-boolean-expression CMP var

                          | var LT arith-boolean-expression
                          | var GT arith-boolean-expression
                          | var LE arith-boolean-expression
                          | var GE arith-boolean-expression
                          | var EQ arith-boolean-expression
                          | var NE arith-boolean-expression
                          | var CMP arith-boolean-expression
        '''

        p[0] = IR.Attributes()

        p[0].truelist = IR.MakeList(IR.NextInstr)
        p[0].code = p[1].code | p[3].code
        p[0].code = p[0].code | IR.GenCode("ifgoto, %s, %s, %s, LABEL#REQUIRED"%(p[2], p[1].place, p[3].place))

        p[0].falselist = IR.MakeList(IR.NextInstr)
        p[0].code = p[0].code | IR.GenCode("goto, LABEL#REQUIRED")

    def p_boolean_not(self, p):
        ''' boolean-not : LNOT var
                        | NOT var
                        | LNOT arith-boolean-expression
                        | NOT arith-boolean-expression
        '''

        p[0] = IR.Attributes()

        if not p[2].isBooleanExpression:
            p[2].truelist = IR.MakeList(IR.NextInstr)
            p[2].code = p[2].code | IR.GenCode("ifgoto, !=, %s, 0, LABEL#REQUIRED"%(p[2].place))

            p[2].falselist = IR.MakeList(IR.NextInstr)
            p[2].code = p[2].code | IR.GenCode("goto, LABEL#REQUIRED")

        p[0].truelist = p[2].falselist
        p[0].falselist = p[2].truelist

        p[0].code = p[2].code

    def p_boolean_expression(self, p):
        ''' boolean-expression : boolean-and
                               | boolean-or
                               | boolean-relop
                               | boolean-not
                               | string-boolean-expression
                               | LPAREN boolean-expression RPAREN

        '''

        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[2]

        p[0].isBooleanExpression = True

    def p_string_op(self, p):
        ''' string-op : string-expression PLUS arith-boolean-expression
                      | string-expression PLUS var
                      | var PLUS string-expression
                      | string-expression DOT string-expression
                      | string-expression DOT var
                      | var DOT string-expression
                      | var DOT var
                      | string-expression REPEAT arith-boolean-expression
                      | string-expression REPEAT var 
                      | var REPEAT arith-boolean-expression
                      | var REPEAT var 
        '''

    def p_string_boolean_op(self, p):
        ''' string-boolean-expression : string-expression STRLT string-expression
                                      | string-expression STRGT string-expression 
                                      | string-expression STRLE string-expression 
                                      | string-expression STRGE string-expression 
                                      | string-expression STREQ string-expression 
                                      | string-expression STRNE string-expression 
                                      | string-expression STRCMP string-expression 

                                      | var STRLT string-expression
                                      | var STRGT string-expression 
                                      | var STRLE string-expression 
                                      | var STRGE string-expression 
                                      | var STREQ string-expression 
                                      | var STRNE string-expression 
                                      | var STRCMP string-expression 

                                      | string-expression STRLT var 
                                      | string-expression STRGT var  
                                      | string-expression STRLE var  
                                      | string-expression STRGE var  
                                      | string-expression STREQ var  
                                      | string-expression STRNE var  
                                      | string-expression STRCMP var 

                                      | var STRLT var
                                      | var STRGT var 
                                      | var STRLE var 
                                      | var STRGE var 
                                      | var STREQ var 
                                      | var STRNE var 
                                      | var STRCMP var 
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

        p[0] = IR.Attributes()
        p[0].opCode = p[1]

    def p_branch(self, p):
        ''' branch : if-elsif-else
                   | unless-elsif-else
        '''

        p[0] = p[1]

    def p_if_elsif_else1(self, p):
        ''' if-elsif-else : if-elsif ''' 

        p[0] = p[1]

    def p_if_elsif_else2(self, p):
        ''' if-elsif-else : if-elsif MARK-backpatch-nextlist ELSE MARK-backpatch codeblock '''

        p[0] = IR.Attributes()
        IR.BackPatch(p[1].falselist, p[4].instr)

        p[0].nextlist = IR.Merge(IR.Merge(p[1].nextlist, p[2].nextlist), p[5].nextlist)
        p[0].code = p[1].code | p[2].code | p[5].code

    def p_if_elsif1(self, p):
        # if (B) codeblock
        ''' if-elsif : IF LPAREN boolean-expression RPAREN MARK-backpatch codeblock '''

        p[0] = IR.Attributes()
        p[0].code = p[3].code | p[6].code

        IR.BackPatch(p[3].truelist, p[5].instr)
        p[0].nextlist = IR.Merge(p[3].falselist, p[6].nextlist)
        p[0].falselist = p[3].falselist

    def p_mark_backpatch_nextlist(self, p):
        ''' MARK-backpatch-nextlist : '''

        p[0] = IR.Attributes()

        p[0].nextlist = IR.MakeList(IR.NextInstr)
        p[0].code = IR.GenCode("goto, LABEL#REQUIRED")

    def p_if_elsif2(self, p):
        ''' if-elsif : IF LPAREN boolean-expression RPAREN MARK-backpatch codeblock MARK-backpatch-nextlist MARK-backpatch elsif '''

        p[0] = IR.Attributes()
        IR.BackPatch(p[3].truelist, p[5].instr)
        IR.BackPatch(p[3].falselist, p[8].instr)
        p[0].nextlist = IR.Merge(IR.Merge(p[6].nextlist, p[7].nextlist), p[9].nextlist)

        p[0].code = p[3].code | p[6].code | p[7].code | p[9].code
        p[0].falselist = p[9].falselist

    def p_if_elsif_error(self, p):
        ''' if-elsif : IF LPAREN error RPAREN codeblock elsif '''
        self.error_list.append((p.lineno(3), "Line %d: Invalid conditional passed to IF"%(p.lineno(3))))

    def p_elsif1(self, p):
        ''' elsif : ELSIF LPAREN boolean-expression RPAREN MARK-backpatch codeblock MARK-backpatch-nextlist MARK-backpatch elsif '''

        p[0] = IR.Attributes()
        IR.BackPatch(p[3].truelist, p[5].instr)
        IR.BackPatch(p[3].falselist, p[8].instr)
        p[0].nextlist = IR.Merge(IR.Merge(p[6].nextlist, p[7].nextlist), p[9].nextlist)

        p[0].code = p[3].code | p[6].code | p[7].code | p[9].code
        p[0].falselist = p[9].falselist

    def p_elsif2(self, p):
        ''' elsif : ELSIF LPAREN boolean-expression RPAREN MARK-backpatch codeblock '''

        p[0] = IR.Attributes()
        p[0].code = p[3].code | p[6].code

        IR.BackPatch(p[3].truelist, p[5].instr)
        p[0].nextlist = IR.Merge(p[3].falselist, p[6].nextlist)
        p[0].falselist = p[3].falselist

    def p_elsif_error(self, p):
        ''' elsif : ELSIF LPAREN error RPAREN codeblock elsif
        '''
        self.error_list.append((p.lineno(3), "Line %d: Invalid conditional passed to ELSIF"%(p.lineno(3))))

    def p_unless_elsif_else1(self, p):
        ''' unless-elsif-else : unless-elsif '''

        p[0] = p[1]

    def p_unless_elsif_else2(self, p):
        ''' unless-elsif-else : unless-elsif MARK-backpatch-nextlist ELSE MARK-backpatch codeblock '''

        p[0] = IR.Attributes()
        IR.BackPatch(p[1].falselist, p[4].instr)

        p[0].nextlist = IR.Merge(IR.Merge(p[1].nextlist, p[2].nextlist), p[5].nextlist)
        p[0].code = p[1].code | p[2].code | p[5].code

    def p_unless_elsif(self, p):
        ''' unless-elsif : UNLESS LPAREN boolean-expression RPAREN MARK-backpatch codeblock MARK-backpatch-nextlist MARK-backpatch elsif '''

        p[0] = IR.Attributes()
        IR.BackPatch(p[3].falselist, p[5].instr)
        IR.BackPatch(p[3].truelist, p[8].instr)
        p[0].nextlist = IR.Merge(IR.Merge(p[6].nextlist, p[7].nextlist), p[9].nextlist)

        p[0].code = p[3].code | p[6].code | p[7].code | p[9].code
        p[0].falselist = p[9].falselist

    def p_unless(self, p):
        ''' unless-elsif : UNLESS LPAREN boolean-expression RPAREN MARK-backpatch codeblock '''

        p[0] = IR.Attributes()
        p[0].code = p[3].code | p[6].code

        IR.BackPatch(p[3].falselist, p[5].instr)
        p[0].nextlist = IR.Merge(p[3].falselist, p[6].nextlist)
        p[0].falselist = p[3].truelist

    def p_unless_error(self, p):
        ''' unless-elsif : UNLESS LPAREN error RPAREN codeblock elsif ELSE codeblock '''
        self.error_list.append((p.lineno(3), "Line %d: Invalid conditional passed to UNLESS"%(p.lineno(3))))

    def p_continue_block(self, p):
        ''' continue : CONTINUE loop-codeblock
        '''

        p[0] = p[2]

    def p_while_loop(self, p):
        ''' while-loop : WHILE MARK-backpatch LPAREN boolean-expression RPAREN MARK-backpatch loop-codeblock '''

        p[0] = IR.Attributes()
        loopID = p[-1].loopID
        defaultID = ''

        IR.BackPatch(p[7].nextlist, p[2].instr)
        IR.BackPatch(p[4].truelist, p[6].instr)

        full_next_list = IR.Merge(p[7].loop_next_list.get(loopID, []), p[7].loop_next_list.get(defaultID, []))
        full_redo_list = IR.Merge(p[7].loop_redo_list.get(loopID, []), p[7].loop_redo_list.get(defaultID, []))
        full_last_list = IR.Merge(p[7].loop_last_list.get(loopID, []), p[7].loop_last_list.get(defaultID, []))

        IR.BackPatch(full_next_list, p[2].instr)
        IR.BackPatch(full_redo_list, p[6].instr)

        p[0].nextlist = IR.Merge(p[4].falselist, full_last_list)

        p[0].loop_next_list = p[7].loop_next_list
        p[0].loop_next_list.pop(loopID, None)
        p[0].loop_next_list.pop(defaultID, None)

        p[0].loop_redo_list = p[7].loop_redo_list
        p[0].loop_redo_list.pop(loopID, None)
        p[0].loop_redo_list.pop(defaultID, None)

        p[0].loop_last_list = p[7].loop_last_list
        p[0].loop_last_list.pop(loopID, None)
        p[0].loop_last_list.pop(defaultID, None)

        p[0].code = p[4].code | p[7].code | IR.GenCode("goto, %d"%(p[2].instr))

    def p_while_loop_continue(self, p):
        ''' while-loop : WHILE MARK-backpatch LPAREN boolean-expression RPAREN MARK-backpatch loop-codeblock MARK-backpatch continue '''

        p[0] = IR.Attributes()
        loopID = p[-1].loopID
        defaultID = ''

        temp_next_list1 = IR.Merge(p[7].loop_next_list.get(loopID, []), p[7].loop_next_list.get(defaultID, []))
        temp_next_list2 = IR.Merge(p[9].loop_next_list.get(loopID, []), p[9].loop_next_list.get(defaultID, []))
        full_next_list = IR.Merge(temp_next_list1, temp_next_list2)

        temp_redo_list1 = IR.Merge(p[7].loop_redo_list.get(loopID, []), p[7].loop_redo_list.get(defaultID, []))
        temp_redo_list2 = IR.Merge(p[9].loop_redo_list.get(loopID, []), p[9].loop_redo_list.get(defaultID, []))
        full_redo_list = IR.Merge(temp_redo_list1, temp_redo_list2)

        temp_last_list1 = IR.Merge(p[7].loop_last_list.get(loopID, []), p[7].loop_last_list.get(defaultID, []))
        temp_last_list2 = IR.Merge(p[9].loop_last_list.get(loopID, []), p[9].loop_last_list.get(defaultID, []))
        full_last_list = IR.Merge(temp_last_list1, temp_last_list2)

        IR.BackPatch(p[7].nextlist, p[8].instr)
        IR.BackPatch(p[4].truelist, p[6].instr)
        IR.BackPatch(full_next_list, p[8].instr)
        IR.BackPatch(full_redo_list, p[6].instr)

        p[0].nextlist = IR.Merge(IR.Merge(p[4].falselist, p[9].nextlist), full_last_list)

        p[0].loop_next_list = IR.MergeLoopLists(p[7].loop_next_list, p[9].loop_next_list)
        p[0].loop_next_list.pop(loopID, None)
        p[0].loop_next_list.pop(defaultID, None)
        p[0].loop_redo_list = IR.MergeLoopLists(p[7].loop_redo_list, p[9].loop_redo_list)
        p[0].loop_redo_list.pop(loopID, None)
        p[0].loop_redo_list.pop(defaultID, None)
        p[0].loop_last_list = IR.MergeLoopLists(p[7].loop_last_list, p[9].loop_redo_list)
        p[0].loop_last_list.pop(loopID, None)
        p[0].loop_last_list.pop(defaultID, None)

        p[0].code = p[4].code | p[7].code | p[9].code | IR.GenCode("goto, %d"%(p[2].instr))

    # Foreach-loop semantics need to be good
    def p_loop(self, p):
        ''' loop : while-loop '''
                 #| UNTIL LPAREN boolean-expression RPAREN codeblock
                 #| FOR LPAREN expression SEMICOLON boolean-expression SEMICOLON expression RPAREN codeblock
                 #| FOREACH var-lhs LPAREN var-lhs RPAREN codeblock continue
                 #| DO codeblock WHILE LPAREN expression RPAREN SEMICOLON
        #'''

        p[0] = p[1]

    def p_loop_error_a(self, p):
        ''' loop : UNTIL LPAREN error RPAREN codeblock
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

    def p_loop_label(self, p):
        ''' loop-label : ID COLON
                       |
        '''

        p[0] = IR.Attributes()
        if len(p) == 1:
            p[0].loopID = ''
        else:
            p[0].loopID = p[1]

    def p_labelled_loop(self, p):
        ''' labelled-loop : loop-label loop '''

        p[0] = p[2]

    def p_loop_next(self, p):
        ''' loop-next : NEXT
                      | NEXT ID
        '''

        p[0] = IR.Attributes()
        
        if len(p) == 2:
            p[0].loop_next_list[''] = IR.MakeList(IR.NextInstr)
        else:
            p[0].loop_next_list[p[2]] = IR.MakeList(IR.NextInstr)

        p[0].code = IR.GenCode("goto, LABEL#REQUIRED")

    def p_loop_redo(self, p):
        ''' loop-redo : REDO
                      | REDO ID
        '''

        p[0] = IR.Attributes()
        
        if len(p) == 2:
            p[0].loop_redo_list[''] = IR.MakeList(IR.NextInstr)
        else:
            p[0].loop_redo_list[p[2]] = IR.MakeList(IR.NextInstr)

        p[0].code = IR.GenCode("goto, LABEL#REQUIRED")

    def p_loop_last(self, p):
        ''' loop-last : LAST
                      | LAST ID
        '''

        p[0] = IR.Attributes()
        
        if len(p) == 2:
            p[0].loop_last_list[''] = IR.MakeList(IR.NextInstr)
        else:
            p[0].loop_last_list[p[2]] = IR.MakeList(IR.NextInstr)

        p[0].code = IR.GenCode("goto, LABEL#REQUIRED")

    def p_loop_control_statement(self, p):
        ''' loop-control : loop-next
                         | loop-redo
                         | loop-last
                         | GOTO ID
        '''

        p[0] = p[1]

    def p_variable_name_lhs_strict(self, p):
        ''' var-name-lhs-strict : VARIABLE '''

        p[0] = IR.Attributes()
        p[0].symEntry = self.symTabManager.Lookup(p[1])
        p[0].place = p[0].symEntry.place
        p[0].code = IR.ListIR()

    def p_dereference(self, p):
        ''' dereference : DEREFERENCE
        '''

        p[0] = IR.Attributes() # is DEREFERENCE
            
        depthDeref = p[1][1:].count('$')
        varName = p[1][0] + p[1][1:][depthDeref:]

        p[0].depthDeref = depthDeref
        p[0].symEntry = self.symTabManager.Lookup(varName)
        
        p[0].code = IR.ListIR()
        targetVar = p[0].symEntry.place 

        for i in xrange(depthDeref):
            p[0].place = IR.TempVar()
            p[0].code = p[0].code | IR.GenCode("=, $, %s, %s"%(p[1].place, targetVar))
            targetVar = p[0].place

    # For array and hash access
    def p_access(self, p):
        ''' access : LBRACKET usable-expression RBRACKET
                   | LBLOCK usable-expression RBLOCK
        '''

        p[0] = IR.Attributes()

        p[0].symEntry = p[-1].symEntry
        if not p[-1].isArrowOp:
            if p[1] == '{':
                newVarName = '%' + p[0].symEntry.baseVarName
            else:
                newVarName = '@' + p[0].symEntry.baseVarName

            p[0].symEntry = self.symTabManager.Lookup(newVarName)

        p[0].place = "%s%s%s%s"%(p[-1].place, p[1], p[2].place, p[3])
        p[0].code = p[2].code | p[-1].code

    def p_arrow(self, p):
        ''' arrow : ARROW '''

        p[0] = IR.Attributes()

        p[0].symEntry = p[-1].symEntry
        if p[0].symEntry.externalType != SYMTAB.SymTabEntry.SCALAR:
            raise PerlTypeError("Dereferenced object must be a scalar value")

        p[0].place = IR.TempVar()
        p[0].code = p[-1].code | IR.GenCode("=, $, %s, %s"%(p[0].place, p[-1].place))
        p[0].isArrowOp = True
 
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
        ''' arrows_and_accesses : arrow access
                                | access
        '''

        if len(p) == 3:
            p[0] = p[2]
        else:
            p[0] = p[1]

    def p_variable_lhs(self, p):
        ''' var-lhs : var-name-lhs-strict
                    | var-name-lhs-strict arrows_and_accesses
        '''

        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[2]

    def p_reference(self, p):
        ''' reference : REFERENCE '''

        p[0] = IR.Attributes()

        varName = p[1][1:]
        p[0].symEntry = self.symTabManager.Lookup(varName)

        p[0].place = IR.TempVar()
        p[0].code = IR.GenCode("=, &, %s, %s"%(p[0].place, p[0].symEntry.place))

    def p_variable(self, p):
        ''' variable : var-lhs MARK-check-declaration
                     | reference MARK-check-declaration 
                     | dereference MARK-check-declaration
        '''

        p[0] = p[1]

    def p_var_function_call(self, p):
        ''' var : variable
                | function-call
        '''

        p[0] = p[1]


    def p_normal_assignment(self, p):
        ''' normal-assignment : var-lhs MARK-check-declaration assign-sep usable-expression %prec EQUALS '''

        p[0] = IR.Attributes()

        if p[3].opCode == '=':
            p[0].code = p[4].code | p[1].code | IR.GenCode("=, %s, %s"%(p[1].place, p[4].place)) 
        else:
            p[0].code = p[4].code | p[1].code | IR.GenCode("=, %s, %s, %s, %s"%(p[3].opCode, p[1].place, p[1].place, p[4].place))

    def p_variable_strict_decl(self, p):
        ''' variable-strict-decl : MY var-name-lhs-strict
                                 | MY var-name-lhs-strict EQUALS usable-expression
        '''

        p[2].symEntry.InsertLocally(self.symTabManager)

        p[0] = IR.Attributes()

        if len(p) == 5:
            p[0].code = p[4].code | IR.GenCode("=, %s, %s"%(p[2].place, p[4].place))
        else:
            p[0].code = IR.ListIR() # TODO

    def p_string(self, p):
        ''' string : SINGQUOTSTR
                   | DOUBQUOTSTR
        '''

        p[0] = IR.Attributes()

        p[0].place = str(p[1])
        p[0].code = IR.ListIR()  # No code

    def p_numeric(self, p):
        ''' numeric : NUMBER
                    | BINARY
                    | OCTAL
                    | HEXADECIMAL
        '''
        
        p[0] = IR.Attributes()

        p[0].place = str(p[1])
        p[0].code = IR.ListIR() # No code 

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

    def p_function_return(self, p):
        ''' function-ret : RETURN expression '''
        p[0] = ('function-ret', self.get_children(p))

    def p_ternary_operator(self, p):
        ''' ternary-op : boolean-expression TERNARY_CONDOP usable-expression COLON usable-expression
                       | LPAREN ternary-op RPAREN
        '''
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

        IR.NextInstr = 1
        IR.InstrMap += [0]
        return self.parser.parse(input)

    def get_children(self, p):
        children = []
        for i in xrange(1,len(p)):
            children.append(p[i])
        return children
