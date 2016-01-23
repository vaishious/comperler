"""

MODULE  : basic_blocks

Purpose : * Class used to represent a basic block. Will be an array of instructions.
          * All required algorithms such as register allocation etc. will be a part of this 
            class
"""

# List of Imports Begin
import debug as DEBUG
import instr3ac as INSTRUCTION
# List of Imports End


class BasicBlock(object):
    """ 
        This class holds an array of instructions corresponding to a single basic block.

        Member Variables :

                * bbNum            : Basic Block Number
                
                * instructions     : The actual sequence of instructions corresponding to the basic block.

                TODO: Add more stuff as and how we need it.

        Member Functions : 

                * RegisterAllocate : Perform register allocation for this block

                TODO: Add more stuff as and how we need it.
    """

    def __init__(self, bbNum=0, instructions=[]):

        self.bbNum        = bbNum
        self.instructions = instructions[:]

    def AddInstruction(self, instr):
        """ Add instructions incrementally. Will help in the basic block algorithm """

        DEBUG.Assert(type(instr) == INSTRUCTION.Instr3AC, "Input is not of instr3AC type")

        self.instructions += [instr]

    def IsEmpty(self):
        return len(self.instructions) == 0

    def PrettyPrint(self):
        print "BASIC BLOCK #" + str(self.bbNum)
        for instr in self.instructions:
            instr.PrettyPrint()
