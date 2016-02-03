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
import library as LIB
# List of Imports End

def GetVarAddr(variable):
    """ Get address of a variable as $V_(var_name) """
    if type(variable) == INSTRUCTION.Entity:
        return "$V_" + str(variable.value)
    else:
        return "$V_" + str(variable)

def GetArrAddr(variable):
    """ Get address of an array as $A_(arr_name) """
    if type(variable) == INSTRUCTION.Entity:
        return "$A_" + str(variable.value)
    else:
        return "$A_" + str(variable)

def GetStrAddr(variable):
    """ Get address of a string as $STR_(stringNum) """
    if type(variable) == INSTRUCTION.Entity:
        return "$STR_" + G.AsmData.GetStringLabel(str(variable.value))
    else:
        return "$STR_" + G.AsmData.GetStringLabel(str(variable))

def GetHashAddr(variable):
    """ Get address of a hash as $H_(var_name) """
    if type(variable) == INSTRUCTION.Entity:
        return "$H_" + str(variable.value)
    else:
        return "$H_" + str(variable)

class DataRegion(object):
    """
        Member Variables :
                
                VarSet                           : A set containing the variables declared so far

                ArraySet                         : A set containing the array variables declared so far

                StringSet                        : A set containing all the static strings defined so far

        Member Functions :

                Allocate32(var a)                : Allocate 4 bytes for the given variable "a" (using .word)

                AllocateArray(var arr, var size) : Allocate an array of "size" bytes for given variable arr (using .space)

                AllocateString(string)           : Allocate space for the given string

                GetStringLabel(string)           : Return label associated with the given static string

    """

    def __init__(self):
        self.varSet    = set([])
        self.hashSet   = {}
        self.arraySet  = {}
        self.stringSet = {}
        self.stringCnt = 0


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

    def AllocateString(self, strEntity):
        DEBUG.Assert(type(strEntity) == INSTRUCTION.Entity, "Type for AllocateString in Data-Region is not Entity")
        DEBUG.Assert(strEntity.is_STRING(), "Only string variables allowed for AllocateString in Data-Region")

        if not self.stringSet.has_key(strEntity.value):
            self.stringSet[strEntity.value] = str(self.stringCnt)
            self.stringCnt += 1

    def AllocateHash(self, hashEntity):
        DEBUG.Assert(type(hashEntity) == INSTRUCTION.Entity, "Type for AllocateHash in Data-Region is not Entity")
        DEBUG.Assert(hashEntity.is_HASH_VARIABLE(), "Only hash variable for AllocateHash in Data-Region")

        self.hashSet[hashEntity.value] = 0 if hashEntity.key.is_NUMBER() else 1

    def GetHashType(self, varName):
        return self.hashSet[varName]

    def GetStringLabel(self, string):
        return self.stringSet[string]

    def GenerateDataRegion(self):
        """ Uses the global object AsmText to write its data to """

        dataText = ".data\n"

        dataText += "# VARIABLES\n"
        for var32 in self.varSet:
            dataText += ".align 2\n"
            dataText += "$V_%s : .word 0\n\n"%(str(var32))

        dataText += "\n# ARRAYS\n"
        for (arr, size) in self.arraySet.items():
            dataText += ".align 2\n"
            dataText += "$A_%s : .word 0:%d\n\n"%(str(arr), size)

        dataText += "\n# STRINGS\n"
        for (string, label) in self.stringSet.items():
            dataText += ".align 2\n"
            dataText += "$STR_%s : .asciiz \"%s\"\n"%(label, string)

        dataText += "\n# HASHES\n"
        for hashVar in self.hashSet:
            dataText += ".align 2\n"
            dataText += "$H_%s : .word 0\n\n"%(str(hashVar))

        print dataText


class TextRegion(object):
    """ This class simply represents the text region. All it does is provide abstraction for adding code """

    def __init__(self, fileName):
        self.header  = """ ### GENERATED MIPS ASSEMBLY - COMPERLER ###""" + "\n"
        self.header += """ ### FILENAME : """ + str(fileName) + " ###\n" 
        self.text    = ""
        self.data    = ""
        self.fileName = fileName

    def AddText(self, text, sideComment = ""):
        if sideComment:
            self.text += '{:<30} # {}'.format(text, sideComment)
        else:
            self.text += text
        self.text += "\n"

    def AddComment(self, comment):
        self.text += "\n"
        self.text += G.INDENT + "# " + comment
        self.text += "\n"

    def WriteHeader(self):
        print self.header

    def AddLibraryFunctions(self):
        for func in G.LibraryFunctionsUsed:
            self.text += "\n" + LIB.LinkFunction(func)

    def WriteToFile(self):

        stackSpaceRequired = G.StackSpaceMap['main']
        loadSegment = ".text\nmain:\n"
        loadSegment += G.INDENT + ".frame $fp,%d,$31\n"%(stackSpaceRequired) 
        loadSegment += G.INDENT + "subu $sp, $sp, %d\n"%(stackSpaceRequired) 
        loadSegment += G.INDENT + "sw $fp, %d($sp)\n"%(stackSpaceRequired-4)
        loadSegment += G.INDENT + "sw $ra, %d($sp)\n"%(stackSpaceRequired-8)
        loadSegment += G.INDENT + "move $fp, $sp\n"

        self.text = loadSegment + self.text
        self.AddLibraryFunctions()
        print self.text


class Register(object):
    """
        Member Variables :
                
                regName           :     The name of the register

        Member Functions :

                LoadImmediate()   :     Produce code for load the immediate value into the register

                LoadVar()         :     Produce code for loading the given variable into the register

                SpillVar()        :     Spill the contents of the register. Uses the G.AsmText to write code

                Score()           :     The amount of store operations we'll need to perform in order to write back
                                        the supplied variables


    """

    def __init__(self, regName):

        self.regName  =  str(regName)

    def __str__(self):
        return "$%s"%(self.regName)

    def __eq__(self, otherReg):
        if isinstance(otherReg, Register):
            return self.regName == otherReg.regName

        return NotImplemented

    def __ne__(self, otherReg):
        if isinstance(otherReg, Register):
            return self.regName != otherReg.regName

        return NotImplemented

    def LoadImmediate(self, num):
        codeLoad = G.INDENT + "li %s, %s"%(self, str(num))
        return codeLoad

    def LoadVar(self, var):
        codeLoad  = G.INDENT + "lw %s, %s\n"%(self, GetVarAddr(var))
        return codeLoad

    def SpillVar(self, var):
        codeStore = G.INDENT + "sw %s, %s\n"%(self, GetVarAddr(var))
        return codeStore

    def Score(self, targetVar, isInputVar=True, ):
        """ Use the current global reg-addr descriptor to calculate scores """

        if type(targetVar) == INSTRUCTION.Entity:
            DEBUG.Assert(targetVar.is_SCALAR_VARIABLE(), "Entity is not a scalar variable")
            targetVar = targetVar.value


        regVars = G.CurrRegAddrTable.GetVars(self)
        DEBUG.Assert(regVars != [] , "%s is empty. Why are we calculating the score?"%self)

        score = 0
        codeSegment = ""
        removeSet = []

        for var in regVars:
            if var == targetVar:
                continue

            removeSet += [var]
            

            if not G.CurrSymbolTable.IsLive(var):
                if not G.CurrRegAddrTable.IsElsewhere(var, self.regName):

                    # Variables are global. We need to write it back
                    codeSegment += self.SpillVar(var)
                    score += 1

                continue

            elif G.CurrRegAddrTable.IsElsewhere(var, self.regName):
                # One load in the future as it is live
                score += 1
                continue

            else: 
                # It is both live and only in the register. We have to store it and load it in the future too
                codeSegment += self.SpillVar(var)
                score += 2


        return score, codeSegment, removeSet





