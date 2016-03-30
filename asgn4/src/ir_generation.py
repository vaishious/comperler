"""
Module : ir_generation
Function : Contains class and function definitions used to perform IR generation
"""

import debug as DEBUG

INT_DATA_TYPE, STR_DATA_TYPE, UNKNOWN_DATA_TYPE = range(3)

class Constant(object):

    def __init__(self, value, dataType):

        self.value = value
        self.dataType = dataType


class Dereference(object):

    def __init__(self, tabEntry, externalType, derefDepth):

        self.tabEntry = tabEntry
        self.externalType = externalType
        self.derefDepth = derefDepth

    def CheckDeclaration(self):
        return self.tabEntry.CheckDeclaration()

    def __str__(self):
        return str(self.tabEntry)

    def InsertGlobally(self, symTabManager):
        self.tabEntry.InsertGlobally(symTabManager)

    def InsertLocally(self, symTabManager):
        self.tabEntry.InsertLocally(symTabManager)

class ArrowOp(object):

    def __init__(self, dereferencedLHS):

        self.dereferencedLHS = dereferencedLHS

        if dereferencedLHS.externalType != SYMTAB.SymTabEntry.SCALAR:
            raise PerlTypeError("Dereferenced object must be a scalar value")

    def CheckDeclaration(self):
        return self.dereferencedLHS.CheckDeclaration()

    def __str__(self):
        return str(self.dereferencedLHS)

    def InsertGlobally(self, symTabManager):
        self.dereferencedLHS.InsertGlobally(symTabManager)

    def InsertLocally(self, symTabManager):
        self.dereferencedLHS.InsertLocally(symTabManager)

class AccessOp(object):

    def __init__(self, lhs, keyAccess, accessType):

        self.lhs = lhs
        self.keyAccess = keyAccess
        self.accessType = accessType

    def CheckDeclaration(self):
        return self.lhs.CheckDeclaration()

    def __str__(self):
        return str(self.lhs)

    def InsertGlobally(self, symTabManager):
        self.lhs.InsertGlobally(symTabManager)

    def InsertLocally(self, symTabManager):
        self.lhs.InsertLocally(symTabManager)

class Reference(object):

    def __init__(self, tabEntry):

        self.tabEntry = tabEntry

    def CheckDeclaration(self):
        return self.tabEntry.CheckDeclaration()

    def __str__(self):
        return str(self.tabEntry)

    def InsertGlobally(self, symTabManager):
        self.tabEntry.InsertGlobally(symTabManager)

    def InsertLocally(self, symTabManager):
        self.tabEntry.InsertLocally(symTabManager)

