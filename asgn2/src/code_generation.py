"""

MODULE  : code_generation.py

Purpose : * Class for parsing the text and launching the basic block algorithm.
            Also houses the code generation algorithm

"""

# List of Imports Begin
import debug as DEBUG
import instr3ac as INSTRUCTION
import basic_blocks as BB
# List of Imports End


class CodeGenerator(object):
    """ This class houses the basic-block generation and code-generation algorithm """

    def __init__(self, text):
        text = text.split('\n')
        text = [i.lstrip().rstrip() for i in text if i != '']
        text = [i.replace('\t', '') for i in text]

        self.instructions = []

        for line in text:
            instrTuple = line.split(',')
            instrTuple = [i.lstrip().rstrip() for i in instrTuple]
            self.instructions += [INSTRUCTION.Instr3AC(instrTuple)]
