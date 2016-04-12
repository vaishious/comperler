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
        if (variable.value == "ARRAY___"):
            return "16($fp)"
        return G.AsmData.varSet[variable.value]
    else:
        if (variable == "ARRAY___"):
            return "16($fp)"
        return G.AsmData.varSet[variable]

def GetStrAddr(variable):
    """ Get address of a string as $STR_(stringNum) """
    if type(variable) == INSTRUCTION.Entity:
        return "$STR_" + G.AsmData.GetStringLabel(str(variable.value))
    else:
        return "$STR_" + G.AsmData.GetStringLabel(str(variable))

class DataRegion(object):

    def __init__(self, funcActRecords, symTabManager):
        self.varSet = {}
        self.globalVars = []
        self.specialVars = ["OPCONTROL", "OP1_TYPECAST", "OP2_TYPECAST"]
        self.stringSet = {}
        self.stringCnt = 0

        for func, record in funcActRecords.items():
            if func == "main":
                for var in record.varLocationMap:
                    self.varSet[var] = var
                    self.globalVars += [var]

                for var, pos in record.tempVarMap.items():
                    self.varSet[var] = "%d($fp)"%(32 + pos) # MIPS calling convention stores arguments in the first 16 bytes

                G.StackSpaceMap[func] = record.tempOffset + 40; # Extra 16 bytes for callee arguments, 8 bytes for fp and ra, and 16 bytes for custom function arguments 
            else:
                for var, pos in record.varLocationMap.items():
                    self.varSet[var] = "%d($fp)"%(pos)

                for var, pos in record.tempVarMap.items():
                    self.varSet[var] = "%d($fp)"%(32 + record.varOffset + pos) # MIPS calling convention stores arguments in the first 16 bytes

                G.StackSpaceMap[func] = record.varOffset + record.tempOffset + 40; 

    def AllocateString(self, strEntity):
        DEBUG.Assert(type(strEntity) == INSTRUCTION.Entity, "Type for AllocateString in Data-Region is not Entity")
        DEBUG.Assert(strEntity.is_STRING(), "Only string variables allowed for AllocateString in Data-Region")

        if not self.stringSet.has_key(strEntity.value):
            self.stringSet[strEntity.value] = str(self.stringCnt)
            self.stringCnt += 1

    def GetHashType(self, varName):
        return self.hashSet[varName]

    def GetStringLabel(self, string):
        return self.stringSet[string]

    def GenerateDataRegion(self, filePtr):
        """ Uses the global object AsmText to write its data to """

        dataText = ".data\n"

        dataText += "# VARIABLES\n"
        for var in self.globalVars:
            dataText += ".align 2\n"
            dataText += "%s : .word 0\n\n"%(var)

        dataText += "\n# STRINGS\n"
        for (string, label) in self.stringSet.items():
            dataText += ".align 2\n"
            dataText += "$STR_%s : .asciiz \"%s\"\n"%(label, string)

        dataText += "\n# SPECIAL VARIABLES\n"
        for var in self.specialVars:
            dataText += ".align 2\n"
            dataText += "%s : .word 0\n\n"%(var)

        dataText += "\n# Library Static Data\n"
        dataText += LIB.LinkLibData()

        filePtr.write(dataText + "\n")


class TextRegion(object):
    """ This class simply represents the text region. All it does is provide abstraction for adding code """

    def __init__(self, fileName):
        self.header  = """ ### GENERATED MIPS ASSEMBLY - COMPERLER ###""" + "\n"
        self.header += """ ### FILENAME : """ + str(fileName) + " ###\n" 
        self.text    = ""
        self.data    = ""
        self.fileName = fileName

    def AddText(self, text, sideComment = ""):
        if text == "":
            return 

        if sideComment:
            self.text += '{:<30} # {}'.format(text, sideComment)
        else:
            self.text += text

        if "jal " in text:
            G.LibraryFunctionsUsed.add(text.split(" ")[-1])

        self.text += "\n"

    def AddComment(self, comment):
        self.text += "\n"
        self.text += G.INDENT + "# " + comment
        self.text += "\n"

    def WriteHeader(self, filePtr):
        filePtr.write(self.header + "\n")

    def AddLibraryFunctions(self):
        for func in G.LibraryFunctionsUsed:
            self.text += "\n" + LIB.LinkFunction(func)

    def WriteFunctionStacks(self):
        for (func, space) in G.StackSpaceMap.items():
            stackSpaceRequired = space

            loadSegment = "%s:\n"%(func)
            loadSegment += G.INDENT + ".frame $fp,%d,$31\n"%(stackSpaceRequired) 
            loadSegment += G.INDENT + "subu $sp, $sp, %d\n"%(stackSpaceRequired) 
            loadSegment += G.INDENT + "sw $a0, %d($sp)\n"%(16)
            loadSegment += G.INDENT + "sw $fp, %d($sp)\n"%(stackSpaceRequired-4)
            loadSegment += G.INDENT + "sw $ra, %d($sp)\n"%(stackSpaceRequired-8)
            loadSegment += G.INDENT + "move $fp, $sp\n"

            if func == "main":
                loadSegment += G.INDENT + "la $t9, %s\n"%("dummyFunc")
                loadSegment += G.INDENT + "sw $t9, %s\n"%("OP1_TYPECAST")
                loadSegment += G.INDENT + "sw $t9, %s\n"%("OP2_TYPECAST")

            self.text = self.text.replace("%s:\n"%(func), loadSegment)

    def WriteToFile(self, filePtr):
        self.text = ".text\nmain:\n" + self.text

        self.WriteFunctionStacks()

        self.AddLibraryFunctions()
        filePtr.write(self.text + "\n")


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

    def GetEarliestNextUse(self):
        regVars = G.CurrRegAddrTable.GetVars(self)
        minNextUse = G.CurrSymbolTable.GetNextUse(regVars[0])

        for i in xrange(1, len(regVars)):
            minNextUse = min(minNextUse, G.CurrSymbolTable.GetNextUse(regVars[i]))

        return minNextUse

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

                    if G.CurrSymbolTable.IsLiveOnExit(var):
                        # However we need to write it back only if it is live on exit
                        # If not, it means that it is overwritten in this block itself

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





