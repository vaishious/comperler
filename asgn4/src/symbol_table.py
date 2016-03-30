"""
Module : symbol_table
Function : Contains class and function definitions used to implement a symbol table
"""

class SymTabEntry(object):

    SCALAR, ARRAY, HASH = range(3)

    def __init__(self, variable):

        self.scopeNum = -1               # Indicates the fact that it has not 
                                         # been entered into the symtable as of yet
        self.varName = variable
        
        if variable[0] == '$'    : self.externalType = SymTabEntry.SCALAR 
        elif variable[0] == '@'  : self.externalType = SymTabEntry.ARRAY
        elif variable[0] == '%'  : self.externalType = SymTabEntry.HASH
        else:
            raise Exception("Unrecognized variable type")

        self.baseVarName = variable[1:]

    def CheckDeclaration(self):
        return self.scopeNum != -1

    def __str__(self):
        return repr(self.varName)

    def InsertGlobally(self, symTabManager):
        if self.scopeNum == -1:
            self.scopeNum = 0
            symTabManager.symtables[0].Insert(self, self.varName)

    def InsertLocally(self, symTabManager):
        self.scopeNum = symTabManager.curScope
        symTabManager.curSymTab.Insert(self, self.varName)


class SymTable(object):

    def __init__(self, scopeNum, parentScope):
        self.entries = {}        # Map from ID(name) to entry
        self.scopeNum = scopeNum
        self.parentScope = parentScope

    def Insert(self, entry, varName):
        self.entries[varName] = entry

    def IsPresent(self, varName):
        return self.entries.has_key(varName)

    def Lookup(self, varName):
        return self.entries.get(varName, None)


class SymTabManager(object):
    """
        Purpose : Manages all the symbol tables associated with all scopes.
    """

    def __init__(self):

        self.symtables = {-1 : None}   # Indexed by the scope number
        self.nextScopeNumber = 0
        self.curScope = -1
        self.curSymTab = None

        self.scopeStack = []

    def PushScope(self):

        lastScope = self.curScope
        self.scopeStack.append(self.nextScopeNumber)
        self.curScope = self.nextScopeNumber
        self.curSymTab = SymTable(self.curScope, lastScope)
        self.symtables[self.curScope] = self.curSymTab
        
        self.nextScopeNumber += 1

    def PopScope(self):

        self.scopeStack.pop()
        self.curScope = self.scopeStack[-1]
        self.curSymTab = self.symtables[self.curScope]

    def Lookup(self, varName):

        itScope = self.curScope
        while (itScope != -1):

            symTab = self.symtables[itScope]
            if symTab.IsPresent(varName):
                return symTab.entries[varName]

            itScope = symTab.parentScope

        # Create new entry to be entered later
        return SymTabEntry(varName)
