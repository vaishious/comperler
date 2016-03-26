"""
Module : symbol_table
Function : Contains class and function definitions used to implement a symbol table
"""

class SymTabEntry(object):
    """ 
        
        Member Variables :

                "name"  : Name of the variable.

                "scope" : The scope number it belongs to.
                
                "type"  : Current type associated with the variable. Aaarghh, the pains of dynamic typing.
                          I don't know if we'd be using this at some point.

        Member Functions :

    """

    def __init__(self, varName, scopeNum):

        self.name = varName
        self.scope = scopeNum


class SymTable(object):
    """
        Purpose : Symbol table corresponding to one scope

        Member Variables :
                
                "entries" : Obviously, the entries themselves

                "parent"  : The parent scope to checkout if a name is not found here

        Member Functions :
              
                "Insert"    : Insert a variable name. If present, returns False, True otherwise

                "IsPresent" : Self-explanatory

                "Lookup"    : Return the entry corresponding to the supplied variable name. Returns None if not present
    """

    def __init__(self, scopeNum):
        self.entries = {}        # Map from ID(name) to entry
        self.scopeNum = scopeNum

    def Insert(self, varName):
        if not self.entries.has_key(varName):
            self.entries[varName] = SymTabEntry(varName, self.scopeNum)
            return True   # Yes, it was inserted

        return False      # No, already present

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

        self.scopeStack.append(self.nextScopeNumber)
        self.curScope = self.nextScopeNumber
        self.symtables[self.curScope] = self.curSymTab
        self.curSymTab = SymTable(self.curScope)
        
        self.nextScopeNumber += 1

    def PopScope(self):

        self.curScope = self.scopeStack.pop()
        self.curSymTab = self.symtables[self.curScope]

    def Insert(self, varName):

        self.curSymTab.Insert(varName)
