"""

MODULE  : mips_assembly.py

Purpose : * Class used to implement the data region. Allocates labels and sizes for variables
          * Class used to implement the text region. Add code, labels etc.
          * Class used to implement registers. Support load/spill/isEmpty operations.

Import Acronym : ASM

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
        DEBUG.Assert(type(varEntity) == INSTRUCTION.Entity, "Type for Allocate32 in Data-Region is not Entity")
        DEBUG.Assert(varEntity.is_SCALAR_VARIABLE(), "Only scalar variable for Allocate32 in Data-Region")

        self.varSet.add(varEntity.value)

    def AllocateArray(self, arrEntity):
        DEBUG.Assert(type(arrEntity) == INSTRUCTION.Entity, "Type for AllocateArray in Data-Region is not Entity")
        DEBUG.Assert(arrEntity.is_ARRAY_VARIABLE(), "Only array variables allowed for AllocateArray in Data-Region")


        # We assume that the "key" value is the size of the array.
        # We will declare it as "declare a[5]"

        DEBUG.Assert(arrEntity.key.is_NUMBER(), "Size of array has to be an integer")

        self.arraySet[arrEntity.value] = arrEntity.key.value

    def GenerateDataRegion(self):
        """ Uses the global object AsmText to write its data to """

        dataText = ".data\n"

        for var32 in self.varSet:
            dataText += "%s : .word 0\n"%(str(var32))

        for (arr, size) in self.arraySet.items():
            dataText += "%s : .space %d\n"%(str(arr), 4*size)

        print dataText


class TextRegion(object):
    """ This class simply represents the text region. All it does is provide abstraction for adding code """

    def __init__(self, fileName):
        self.header  = """ ### GENERATED MIPS ASSEMBLY - COMPERLER ###""" + "\n"
        self.header += """ ### FILENAME : """ + str(fileName) + " ###\n" 
        self.text    = ".text\n"
        self.data    = ""
        self.fileName = fileName

    def AddText(self, text):
        self.text += text
        self.text += "\n"

    def WriteHeader(self):
        print self.header

    def WriteToFile(self):
        print self.text


class Register(object):
    """
        Member Variables :
                
                regName           :     The name of the register

                var               :     The variable that has been allocated to this register

                empty             :     Whether this register is empty or not

        Member Functions :

                AllocateVar(var)  :     Allocate a variable to this register and load the contents.
                                        Uses the G.AsmText to write code

                SpillVar()        :     Spill the contents of the register. Uses the G.AsmText to write code

                IsEmpty()         :     Obvious

    """

    def __init__(self, regName):

        self.regName  =  str(regName)
        self.var      =  None
        self.empty    =  True

    def LoadVar(self):
        codeLoad  = "lw $%s, %s($gp)"%(self.regName, str(self.var.value))
        G.AsmText.AddText(codeLoad)

    def WriteBackVar(self):
        codeStore = "sw $%s, %s($gp)"%(self.regName, str(self.var.value))
        G.AsmText.AddText(codeStore)

    def AllocateVar(self, var):
        DEBUG.Assert(type(var) == INSTRUCTION.Entity, "Type of var in AllocateVar in Register should be Entity")

        self.var   = var
        self.empty = False
        self.LoadVar()

    def SpillVar(self):
        self.WriteBackVar()

        self.var = None
        self.empty = True

    def IsEmpty(self):
        return self.empty
