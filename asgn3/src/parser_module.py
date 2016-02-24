import ply.yacc as yacc

class Parser(object):

    # Dummy rule for now
    def p_assignment(self, p):
        'assignment : VARIABLE EQUALS NUMBER SEMICOLON'
        print "%s %s %d%s"%(p[1], p[2], p[3], p[4])

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
