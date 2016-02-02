"""

MODULE  : code_generation.py

Purpose : * Class for parsing the text and launching the basic block algorithm.
            Also houses the code generation algorithm

"""

# List of Imports Begin
import debug as DEBUG
import instr3ac as INSTRUCTION
import basic_blocks as BB
import mips_assembly as ASM
import global_objects as G
# List of Imports End


class CodeGenerator(object):
    """ 
        This class houses the basic-block generation and code-generation algorithm 

        Member Variables:

                * instructions : Stores all the program instructions

                * basicBlocks  : Stores all the basic blocks

                * targets      : Which line IDs are goto targets. Used for basic block algorithm
        
    """

    def __init__(self, text, fileName):
        text = text.split('\n')
        text = [i.lstrip().rstrip() for i in text if i != '']
        text = [i.replace('\t', '') for i in text]

        self.instructions = []
        self.basicBlocks  = []
        self.targets      = set([])
        self.allLineIDs   = set([])

        # Build Global Objects
        G.AsmText = ASM.TextRegion(fileName)
        G.AsmData = ASM.DataRegion()

        # Create an instance of the instruction class for each line
        for line in text:
            instrTuple = line.split(',')
            instrTuple = [i.lstrip().rstrip() for i in instrTuple]
            instr = INSTRUCTION.Instr3AC(instrTuple)

            # Disallow multiple input lines with same lineID
            DEBUG.Assert(instr.lineID not in self.allLineIDs,"Multiple lines with same line ID.")

            self.allLineIDs.add(instr.lineID)
            self.instructions += [instr]

            # print self.instructions[-1]

            gotoTarget = self.instructions[-1].GetTarget()
            if gotoTarget:
                self.targets.add(gotoTarget)

        # Identify the branch targets and set their isTarget value to true 
        for instr in self.instructions:
            if "$LID_" + str(instr.lineID) in self.targets:
                instr.isTarget = True

    def GenBasicBlocks(self): 
        """ Generate basic blocks using the algorithm """

        if len(self.instructions) == 0:
            return

        bbCount = 0
        self.basicBlocks = [BB.BasicBlock()]

        # First statement is a leader
        self.basicBlocks[-1].AddInstruction(self.instructions[0])

        for instr in self.instructions[1:]:

            # Is the current instruction a branch target? If yes, it's a leader
            if instr.IsTarget():
                bbCount += 1
                self.basicBlocks += [BB.BasicBlock(bbCount)]

            self.basicBlocks[-1].AddInstruction(instr)

            # Is the current instruction a goto/call/ret statement? If yes, the next statement is a leader
            if instr.instrType.is_GOTO() or instr.instrType.is_IFGOTO() or instr.instrType.is_CALL() or instr.instrType.is_RETURN():
                bbCount += 1
                self.basicBlocks += [BB.BasicBlock(bbCount)]

        self.basicBlocks = [bb for bb in self.basicBlocks if not bb.IsEmpty()]
        for i, bb in enumerate(self.basicBlocks):
            bb.bbNum = i

    def PrintBasicBlocks(self):
        for bb in self.basicBlocks:
            bb.PrettyPrint()

    def BuildCode(self):
        for bb in self.basicBlocks:
            bb.Translate()

        G.AsmText.WriteHeader()
        G.AsmData.GenerateDataRegion()
        G.AsmText.WriteToFile()

