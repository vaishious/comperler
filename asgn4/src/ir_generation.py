"""
Module : ir_generation
Function : Contains class and function definitions used to perform IR generation
"""

class DataType(object):
    """ String or Integer/Real/Float if applicable """

    INT, STR, UNKNOWN = range(3)

    def __init__(self, dataType):

        self.dataType = dataType

    def is_INT_TYPE(self)       : return self.dataType == DataType.INT
    def is_STR_TYPE(self)       : return self.dataType == DataType.STR
    def is_UNDEFINED_TYPE(self) : return self.dataType == DataType.UNKNOWN


class Entity(object):
    """ Can represent variables, numbers and strings """

    VARIABLE, NUMBER, STRING = range(3)

    def __init__(self, value, entityType, dataTypeObj):

        self.value = value
        self.entityType = entityType
        self.dataTypeObj = dataTypeObj

    def is_VARIABLE(self) : return self.entityType == Entity.VARIABLE
    def is_NUMBER(self)   : return self.entityType == Entity.NUMBER
    def is_STRING(self)   : return self.entityType == Entity.STRING

    def is_INT_TYPE(self)       : return self.dataTypeObj.is_INT_TYPE()
    def is_STR_TYPE(self)       : return self.dataTypeObj.is_STR_TYPE()
    def is_UNDEFINED_TYPE(self) : return self.dataTypeObj.is_UNDEFINED_TYPE()


class BinaryOp(object):
    """ Represents all binary ops. Useful for defining a generic code generation template """

    def __init__(self, op, op1, op2):

        self.op  = op
        self.op1 = op1
        self.op2 = op2

class UnaryOp(object):
    """ Represents all unary ops. Useful for defining a generic code generation template """

    def __init__(self, op, op1):

        self.op  = op
        self.op1 = op1
