"""

MODULE  : mips_assembly.py

Purpose : * Class used to implement the data region. Allocates labels and sizes for variables
          * Class used to implement the text region. Add code, labels etc.
          * Class used to implement registers. Support load/spill/isEmpty operations.

"""

# List of Imports Begin
import instr3ac as INSTRUCTION
import debug as DEBUG
import global_objects as G
# List of Imports End

class DataRegion(object):
    """
        Member Variables :
                
                VarSet                           : A set containing the variables declared so far

                ArraySet                         : A set containing the array variables declared so far

        Member Functions :

                Allocate32(var a)                : Allocate 4 bytes for the given variable "a" (using .word)

                AllocateArray(var arr, var size) : Allocate an array of "size" bytes for given variable arr (using .space)

    """

    def __init__(self):
        self.varSet   = set([])
        self.arraySet = {}


    def Allocate32(self, varEntity):
        DEBUG.Assert(type(varEntity) == INSTRUCTION.Entity)
        DEBUG.Assert(varEntity.is_SCALAR_VARIABLE())

        self.varSet.add(varEntity.value)

    def AllocateArray(self, arrEntity):
        DEBUG.Assert(type(arrEntity) == INSTRUCTION.Entity)
        DEBUG.Assert(arrEntity.is_ARRAY_VARIABLE())


        # We assume that the "key" value is the size of the array.
        # We will declare it as "declare a[5]"

        DEBUG.Assert(arrEntity.key.is_NUMBER())

        self.arraySet[arrEntity.value] = arrEntity.key.value

    def GenerateDataRegion(self):
        """ Uses the global object AsmText to write its data to """
        G.AsmText.AddText(".data")

        for var32 in self.varSet:
            G.AsmText.AddText("%s : .word 0"%(str(var32)))

        for (arr, size) in self.arraySet.items():
            G.AsmText.AddText("%s : .space %d"%(str(arr), 4*size))



class TextRegion(object):
    """ This class simply represents the text region. All it does is provide abstraction for adding code """

    def __init__(self, fileName):
        self.text  = """ ### GENERATED MIPS ASSEMBLY - COMPERLER ###""" + "\n"
        self.text += """ ### FILENAME : """ + str(fileName) + " ###\n" 
        self.fileName = fileName

    def AddText(self, text):
        self.text += text
        self.text += "\n"

    def WriteToFile(self):
        self.AddText(".text")
        print self.text
