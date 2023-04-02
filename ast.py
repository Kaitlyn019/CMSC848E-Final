# SELECT count(*) FROM head WHERE age  >  56

from anytree import Node, RenderTree
from enum import Enum

class Type(Enum):
    PREDICATE = "PREDICATE"
    RELATION = "RELATION"
    CONST = "CONST"
    CONST_SET = "CONST_SET"
    EMPTY = "EMPTY"

class Operator(Enum):
    UNION_SET = "UNION_SET"
    INTERSECTION_SET = "INTERSECTION_SET"
    DIFFERENCE_SET = "DIFFERENCE_SET"
    SELECTION = "SELECTION"
    CARTESIAN = "CARTESIAN"
    PROJECTION = "PROJECTION"
    AND = "AND"
    OR = "OR"
    GREATER_THAN = "GREATER_THAN"
    LESS_THAN = "LESS_THAN"
    EQUAL = "EQUAL"
    NOT_EQUAL = "NOT_EQUAL"
    UNION_CONST = "UNION_CONST"
    ORDERBY_ASC = "ORDERBY_ASC"
    ORDERBY_DSC = "ORDERBY_DSC"
    GROUPBY = "GROUPBY"
    LIMIT = "LIMIT"
    IN = "IN"
    NOTIN = "NOT_IN"
    LIKE = "LIKE"
    NOTLIKE = "NOT_LIKE"
    COUNT = "COUNT"
    SUM = "SUM"
    MAX = "MAX"
    MIN = "MIN"
    AVG = "AVG"
    DISTINCT = "DISTINCT"
    AS = "AS"
    CONST_LEAF = "CONST_LEAF"
    CONST_SET_LEAF = "CONST_SET_LEAF"
    RELATION_LEAF = "RELATION_LEAF"
    EMPTY = "EMPTY"

ops_outputs = {
    Operator.UNION_SET: Type.RELATION,
    Operator.INTERSECTION_SET: Type.RELATION,
    Operator.DIFFERENCE_SET: Type.RELATION,
    Operator.SELECTION: Type.RELATION,
    Operator.CARTESIAN: Type.RELATION,
    Operator.PROJECTION: Type.RELATION,
    Operator.AND: Type.PREDICATE,
    Operator.OR: Type.PREDICATE,
    Operator.GREATER_THAN: Type.PREDICATE,
    Operator.LESS_THAN: Type.PREDICATE,
    Operator.EQUAL: Type.PREDICATE,
    Operator.NOT_EQUAL: Type.PREDICATE,
    Operator.UNION_CONST: Type.CONST,
    Operator.ORDERBY_ASC: Type.RELATION,
    Operator.ORDERBY_DSC: Type.RELATION,
    Operator.GROUPBY: Type.RELATION,
    Operator.LIMIT: Type.RELATION,
    Operator.IN: Type.PREDICATE,
    Operator.NOTIN: Type.PREDICATE,
    Operator.LIKE: Type.PREDICATE,
    Operator.NOTLIKE: Type.PREDICATE,
    Operator.SUM: Type.CONST,
    Operator.MAX: Type.CONST,
    Operator.MIN: Type.CONST,
    Operator.COUNT: Type.CONST,
    Operator.AVG: Type.CONST,
    Operator.DISTINCT: Type.CONST,
    Operator.AS: Type.RELATION,
    Operator.CONST_LEAF: Type.CONST,
    Operator.CONST_SET_LEAF: Type.CONST_SET,
    Operator.RELATION_LEAF: Type.RELATION,
    Operator.EMPTY: Type.EMPTY
}

ops_inputs = {
    Operator.UNION_SET: (Type.RELATION, Type.RELATION),
    Operator.INTERSECTION_SET: (Type.RELATION, Type.RELATION),
    Operator.DIFFERENCE_SET: (Type.RELATION, Type.RELATION),
    Operator.SELECTION: (Type.PREDICATE, Type.RELATION),
    Operator.CARTESIAN: (Type.RELATION, Type.RELATION),
    Operator.PROJECTION: (Type.CONST_SET, Type.RELATION),
    Operator.AND: (Type.PREDICATE, Type.PREDICATE),
    Operator.OR: (Type.PREDICATE, Type.PREDICATE),
    Operator.GREATER_THAN: (Type.CONST, Type.CONST),
    Operator.LESS_THAN: (Type.CONST, Type.CONST),
    Operator.EQUAL: (Type.CONST, Type.CONST),
    Operator.NOT_EQUAL: (Type.CONST, Type.CONST),
    Operator.UNION_CONST: (Type.CONST_SET, Type.CONST_SET),
    Operator.ORDERBY_ASC: (Type.CONST, Type.RELATION),
    Operator.ORDERBY_DSC: (Type.CONST, Type.RELATION),
    Operator.GROUPBY: (Type.CONST, Type.RELATION),
    Operator.LIMIT: (Type.CONST, Type.RELATION),
    Operator.IN: (Type.CONST, Type.RELATION),
    Operator.LIKE: (Type.CONST, Type.CONST),
    Operator.NOTLIKE: (Type.CONST, Type.CONST),
    Operator.SUM: (Type.CONST, Type.EMPTY),
    Operator.MAX: (Type.CONST, Type.EMPTY),
    Operator.MIN: (Type.CONST, Type.EMPTY),
    Operator.COUNT: (Type.CONST, Type.EMPTY),
    Operator.AVG: (Type.CONST, Type.EMPTY),
    Operator.DISTINCT: (Type.CONST, Type.EMPTY),
    Operator.AS: (Type.CONST, Type.RELATION),
    Operator.CONST_LEAF: (Type.EMPTY, Type.EMPTY),
    Operator.CONST_SET_LEAF: (Type.EMPTY, Type.EMPTY),
    Operator.RELATION_LEAF: (Type.EMPTY, Type.EMPTY)
}

counter = 0

class AST():
    def __init__(self):
        self.leaf = Node("EMPTY", op = Operator.EMPTY)
        self.counter = 0
        self.nodes = []

    def createNode(self, op, left, right, value):
        id = "s" + str(self.counter)
        self.counter += 1

        if (left == None) and (right == None):
            node = Node(id, op = op, value=value)
        elif right == None:
            node = Node(id, op = op, children=(left,), value=value)
        else:
            node = Node(id, op = op, children=(left, right), value=value)
        self.nodes.insert(0, node)

        return node

    def updateNodeValue(self, node, newVal):
        node = Node(node.id, op = node.op, value = newVal)

        return node

    def valid(self, node):
        print (ops_inputs[node.op])

        if (len(node.children) == 0):
            return True
        elif (len(node.children) == 1):
            print ((ops_outputs[node.children[0].op],))
            if ops_inputs[node.op] == (ops_outputs[node.children[0].op],):
                return True
        else:
            print ((ops_outputs[node.children[0].op], ops_outputs[node.children[1].op]))
            if ops_inputs[node.op] == (ops_outputs[node.children[0].op], ops_outputs[node.children[1].op]):
                return True
        return False
    
    def getTree(self): # returns most recent node
        if self.nodes == []:
            return []
        else:
            return self.nodes[0]

    def prettify(self):
        if self.nodes == []:
            print ("")
        else:
            print (RenderTree(self.nodes[0]))

''' class UnNode():
    def __init__(self, op, child):
        self.op = op
        self.child = child

        #return ops_outputs[self.op]
    
    def valid(self):
        if ops_inputs[self.op] == (ops_outputs[self.child],):
            return True
        return False
    
class LeafNode():
    def __init__(self, op, value):
        self.value = value
        self.op = op

        #return ops_outputs[self.op]

    def valid(self):
        return True
 '''
