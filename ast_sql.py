from anytree import Node, RenderTree
from enum import Enum
import pandas as pd
import re

class Type(Enum):
    PREDICATE = "PREDICATE"
    RELATION = "RELATION"
    CONST = "CONST"
    CONST_SET = "CONST_SET"
    EMPTY = "EMPTY"

# each of the types that can be returned by a node
class CompleteType(Enum):
    BOOLEAN = "BOOLEAN" # returns a single value
    INTEGER = "INTEGER"
    STRING = "STRING"
    TIME = "TIME"
    OTHERS = "OTHERS"
    SET = "SET" # returns a single column
    RELATION = "RELATION" # returns multiple columns
    ERROR = "ERROR"
    UNKNOWN = "UNKNOWN"

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
    BETWEEN = "BETWEEN"
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
    ARITHMETIC = "ARITHMETIC"

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
    Operator.BETWEEN: Type.PREDICATE,
    Operator.EQUAL: Type.PREDICATE,
    Operator.NOT_EQUAL: Type.PREDICATE,
    Operator.UNION_CONST: Type.CONST_SET,
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
    Operator.EMPTY: Type.EMPTY,
    Operator.ARITHMETIC: Type.CONST,
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
    Operator.BETWEEN: (Type.CONST, Type.CONST),
    Operator.EQUAL: (Type.CONST, Type.CONST),
    Operator.NOT_EQUAL: (Type.CONST, Type.CONST),
    Operator.UNION_CONST: (Type.CONST_SET, Type.CONST_SET),
    Operator.ORDERBY_ASC: (Type.CONST, Type.RELATION),
    Operator.ORDERBY_DSC: (Type.CONST, Type.RELATION),
    Operator.GROUPBY: (Type.CONST, Type.RELATION),
    Operator.LIMIT: (Type.CONST, Type.RELATION),
    Operator.IN: (Type.CONST, Type.RELATION),
    Operator.NOTIN: (Type.CONST, Type.RELATION),
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
    Operator.RELATION_LEAF: (Type.EMPTY, Type.EMPTY),
    Operator.ARITHMETIC: (Type.CONST, Type.CONST)
}

counter = 0
tables = pd.read_json("spider/tables.json")
tables = tables.set_index('db_id')

class AST():
    def __init__(self, db_id):
        self.leaf = Node("EMPTY", op = Operator.EMPTY)
        self.counter = 0
        self.nodes = []
        
        # Code iterates through the json version of the tables to create a dataframe for all data in the db
        # which has the column names, table name, types, is_primary, and foreign key pairs in list [(table, column),...]
        ct = 1
        temp = tables.loc[db_id]
        curr_table = []
        while ct < len(temp["column_names_original"]):
            (index, name) = temp["column_names_original"][ct]
            
            #if index > len(self.schema):
            #    df = pd.DataFrame(curr_table.copy(), columns=["name","type","is_primary","foreign_keys"]).set_index("name")
            #    self.schema[(temp["table_names_original"][index-1]).lower()] = df
            #    curr_table = [] 
            
            # name of column, table, type of column, is primary, matching foreigns in list [(table, column),...]
            is_primary = True if ct in temp["primary_keys"] else False
            table = (temp["table_names_original"][index]).lower()
            curr_table.append([name.lower(), table, temp["column_types"][ct], is_primary, []])

            ct += 1
        
        self.schema = pd.DataFrame(curr_table.copy(), columns=["clm_name", "table_name", "clm_type", "is_primary", "foreign_keys"]).set_index(["table_name", "clm_name"])
        
        for (key1, key2) in temp["foreign_keys"]:
            (table_1, name_1) = temp["column_names_original"][int(key1)]
            (table_2, name_2) = temp["column_names_original"][int(key2)]

            table_1 = temp["table_names_original"][int(table_1)].lower()
            table_2 = temp["table_names_original"][int(table_2)].lower()

            self.schema.loc[table_1, name_1.lower()]["foreign_keys"].append((table_2, name_2.lower()))
            self.schema.loc[table_2, name_2.lower()]["foreign_keys"].append((table_1, name_1.lower()))

    # When node is created, it is given a specific type
    # BOOLEAN = "BOOLEAN"
    # INTEGER = "INTEGER"
    # STRING = "STRING"
    # COLUMN = "COLUMN"
    # RELATION = "RELATION"

    # We presume that it will be bottom up
    def getCompleteType(self, node):
        #(left, right) = (None, None) if len(node.children) == 0 else node.children

        if node.op == Operator.CONST_LEAF:
            value = node.value 
            
            # get the list of column names for this db
            self.clms = list(map(lambda x: str.lower(x[1]), list(self.schema["column_names"])))
            self.clms.remove('*')
            self.clms.sort(key=len)
            self.clms.reverse() # sort by length so that we match longest possible first

            clms_rgx = re.compile(re.compile("|".join(self.clms), re.IGNORECASE))
            tbls_rgx = re.compile(re.compile("|".join(list(self.schema.keys()))), re.IGNORECASE)
            
            if type(value) is int: # the value is a number
                node.type = CompleteType.INTEGER
                return 1
            elif re.match(r'(\w+)\.(\w+)', value): # i.e. "T1.party_id"
                match = re.match(r'(\w+)\.(\w+)', value)
                
                if clms_rgx.match(match.group(2)): # check that the column is valid i.e. party_id in db
                    node.type = CompleteType.SET # then this returns a table
                    return 1
                else:
                    node.type = CompleteType.ERROR # if it is not in the db, this column is invalid to call upon
                    return -1
            elif clms_rgx.match(value) and tbls_rgx.match(value): # i.e. "party_id"
                clm = clms_rgx.match(value)
                tbl = tbls_rgx.match(value)

                if len(clm) > len(tbl):
                    node.type = CompleteType.SET
                elif len(clm) < len(tbl):
                    node.type = CompleteType.RELATION
                else: # there exists a column that matches a table name, will need to propogate up to determine?
                    print ("FLAG THIS EXAMPLE FOR LOOKING INTO")
                    node.type = CompleteType.UNKNOWN
                
                return 1
            
            elif clms_rgx.match(value): 
                node.type = CompleteType.SET
            elif tbls_rgx.match(value):
                node.type = CompleteType.RELATION
            elif re.match(r'[\'][^\']*[\']|[\"][^\"]*[\"]', value): # is some string in quotes
                node.type = CompleteType.STRING
            elif re.match(r'\w+', value): # is some string (usually in an As, will handle above)
                node.type = CompleteType.STRING
            else:
                node.type = CompleteType.ERROR
                return -1
            return 1
        
        elif node.op in [Operator.AVG, Operator.SUM, Operator.MAX, Operator.MIN, Operator.COUNT]: # the aggregates
            (child,) = node.children
            if node.op == Operator.AVG or node.op == Operator.SUM: # the child must be type int or set with type int
                if child.type == CompleteType.SET: # the child must be type int or set with type int
                    self.schema.loc[child.value] 

    def createNode(self, op, left, right, value):
        id = "s" + str(self.counter)
        self.counter += 1

        if (left == None) and (right == None):
            node = Node(id, op = op, value=value) #, type = CompleteType.UNKNOWN)
            #self.getCompleteType(node)

        elif right == None:
            node = Node(id, op = op, children=(left,), value=value) #, type = CompleteType.UNKNOWN)
            #self.getCompleteType(node)

        else:
            node = Node(id, op = op, children=(left, right), value=value) #, type = CompleteType.UNKNOWN)
            #self.getCompleteType(node)

        self.nodes.insert(0, node)

        return node

    def copyNode(self, node):
        id = "s" + str(self.counter)
        self.counter += 1

        if len(node.children) == 2:
            node_copy = Node(id, op = node.op, 
                         children = (self.copyNode(node.children[0]), self.copyNode(node.children[1])), 
                         value = node.value)
        elif len(node.children) == 1:
            node_copy = Node(id, op = node.op, 
                         children = (self.copyNode(node.children[0]),), 
                         value = node.value)
        else:
            node_copy = Node(id, op=node.op, value = node.value)

        self.nodes.insert(0, node_copy)

        return node_copy

    def valid(self, node, verbose = False):
        if verbose: print ("Target: " + str(ops_inputs[node.op]))

        if (len(node.children) == 0):
            return True
        elif (len(node.children) == 1):
            if verbose: print ("Input: " + str(ops_outputs[node.children[0].op]) + " , " + str(Type.EMPTY))
            if ops_inputs[node.op] == (ops_outputs[node.children[0].op],Type.EMPTY):
                return self.valid(node.children[0]) and True
        else:
            if verbose: print ("Input: " + str(ops_outputs[node.children[0].op]) + " , " + str(ops_outputs[node.children[1].op]))
            if ops_inputs[node.op] == (ops_outputs[node.children[0].op], ops_outputs[node.children[1].op]):
                return self.valid(node.children[0]) and self.valid(node.children[1]) and True

        # Exceptions: if want const_set but given const, it is okay
        if (node.op == Operator.UNION_CONST and 
            (ops_outputs[node.children[0].op], ops_outputs[node.children[1].op]) in 
            [(Type.CONST, Type.CONST), (Type.CONST_SET, Type.CONST), (Type.CONST, Type.CONST_SET)]):
                return self.valid(node.children[0]) and self.valid(node.children[1]) and True

        if (node.op == Operator.PROJECTION and 
            ops_outputs[node.children[0].op] == Type.CONST):
                return self.valid(node.children[0]) and self.valid(node.children[1])

        print ("Error: " + str(node))
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
