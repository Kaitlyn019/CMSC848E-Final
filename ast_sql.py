from anytree import Node, RenderTree
from ast_consts import *
import pandas as pd
import re
import json

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
            curr_table.append([name.lower(), table, table_types[temp["column_types"][ct]], is_primary, []])

            ct += 1
        
        self.schema = pd.DataFrame(curr_table.copy(), columns=["clm_name", "table_name", "clm_type", "is_primary", "foreign_keys"]).set_index(["table_name", "clm_name"])
        
        for (key1, key2) in temp["foreign_keys"]:
            (table_1, name_1) = temp["column_names_original"][int(key1)]
            (table_2, name_2) = temp["column_names_original"][int(key2)]

            table_1 = temp["table_names_original"][int(table_1)].lower()
            table_2 = temp["table_names_original"][int(table_2)].lower()

            self.schema.loc[table_1, name_1.lower()]["foreign_keys"].append((table_2, name_2.lower()))
            self.schema.loc[table_2, name_2.lower()]["foreign_keys"].append((table_1, name_1.lower()))

        clms = list(map(lambda x: str.lower(x), list(self.schema.index.get_level_values(1))))
        clms.sort(key=len)
        clms.reverse() # sort by length so that we match longest possible first

        self.clms_rgx = re.compile("^("+"|".join(clms)+")$", re.IGNORECASE)

        tbls = list(set(list(map(lambda x: str.lower(x), list(self.schema.index.get_level_values(0))))))
        tbls.sort(key=len)
        tbls.reverse() # sort by length so that we match longest possible first

        self.tbls_rgx = re.compile("^("+"|".join(tbls)+")$", re.IGNORECASE)

    def constType(self, text):
        if (self.tbls_rgx.match(text)):
            return "relation"
        elif (self.clms_rgx.match(text)):
            return "const"

    # When node is created, it is given a specific type
    # BOOLEAN = "BOOLEAN"
    # INTEGER = "INTEGER"
    # STRING = "STRING"
    # COLUMN = "COLUMN"
    # RELATION = "RELATION"

    # We presume that it will be bottom up
    # Returns true if node is valid, returns false if node is not valid
    def getCompleteType(self, node):

        # Case 1: It is a leaf node
        if node.op == Operator.CONST_LEAF:
            value = node.value 
            
            clm_match = self.clms_rgx.match(value)
            tbl_match = self.tbls_rgx.match(value)
            
            if type(value) is int: # the value is a number
                node.type = CompleteType.INTEGER
                return True
            
            elif re.match(r'(\w+)\.(\w+)', value): # i.e. "T1.party_id"
                match = re.match(r'(\w+)\.(\w+)', value)

                if self.clms_rgx.match(match.group(2)): # check that the column is valid i.e. party_id in db
                    node.type = CompleteType.SET # then this returns a column
                    self.schema[[match.group(1), match.group(2)]] = ["", False, []]
                    return True
                else:
                    node.type = CompleteType.ERROR # if it is not in the db, this column is invalid to call upon
                    return False
                
            elif clm_match and tbl_match: # i.e. "customer" in both table and column
                clm = self.clms_rgx.match(value)
                tbl = self.tbls_rgx.match(value)

                if len(clm) > len(tbl): 
                    node.type = CompleteType.SET
                elif len(clm) < len(tbl):
                    node.type = CompleteType.RELATION
                else: # there exists a column that matches a table name, will need to propogate up to determine?
                    print ("FLAG THIS EXAMPLE FOR LOOKING INTO")
                    node.type = CompleteType.UNKNOWN
            
                return True
            
            elif self.clms_rgx.match(value): 
                node.type = CompleteType.SET
            elif self.tbls_rgx.match(value):
                node.type = CompleteType.RELATION
            elif re.match(r'[\'][^\']*[\']|[\"][^\"]*[\"]', value): # is some string in quotes
                node.type = CompleteType.STRING
            elif re.match(r'\w+', value): # is some string (usually in an As, will handle above)
                node.type = CompleteType.STRING
            else:
                node.type = CompleteType.ERROR
                return False
            return True
        
        elif node.op in [Operator.AVG, Operator.SUM, Operator.MAX, Operator.MIN, Operator.COUNT]: # is an aggregate
            (child,) = node.children
            if node.op == Operator.AVG or node.op == Operator.SUM: # the child must be type int or set with type int
                if child.type == CompleteType.SET: # the child must be type int or set with type int
                    self.schema.loc[child.value] 
                    
                    
    # Creating node in AST
    def createNode(self, op, left, right, value, root = True):
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

        if root:
            self.nodes.insert(0, node)
        else:
            self.nodes.append(node)

        return node

    # Deep copying a node in AST 
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

    # Checks if it is valid based on SmBoP type system
    # Takes: rooted node to check if entire tree is valid, verbose whether or not to print each step
    def valid(self, node, verbose = False):
        if verbose: print ("Target: " + str(ops_inputs[node.op]))

        if (node.op == Operator.KEEP):
            return self.valid(node.children[0])

        if (len(node.children) == 0): 
            # if it is a leaf node, we assume valid if the following hold true:
            # if it is a column node, it is valid if it is a 
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

        if (node.op == Operator.SELECT and 
            ops_outputs[node.children[0].op] == Type.CONST):
                return self.valid(node.children[0]) and self.valid(node.children[1])

        print ("Error: " + str(node))
        return False
    
    # Returns the tree rooted at the most recent node added
    def getTree(self): # returns most recent node
        if self.nodes == []:
            return []
        else:
            return self.nodes[0]

    def size(self, node):
        if len(node.children) == 2:
            return 1 + max(self.size(node.children[0]), self.size(node.children[1]))
        elif len(node.children) == 1:
            return 1 + self.size(node.children[0])
        else:
            return 1

    def balanceTreeHelper(self, node, size):        
        # balance the children to be of the correct size which is the max of either children

        if len(node.children) == 2:
            left = node.children[0]
            right = node.children[1]
            left = self.balanceTreeHelper(left, size - 1)
            right = self.balanceTreeHelper(right, size - 1)
            node.children = (left, right)
            return node
        elif len(node.children) == 1:
            node.children = (self.balanceTreeHelper(node.children[0], size - 1),)
            return node
        else:
            # at the leaf node, do keeps until it is the correct size
            prev = node
            while (size >= 1):
                prev = self.createNode(Operator.KEEP, prev, None, None, root=False)
                size -= 1
            
            return prev

    def balanceTree(self):  
        root = self.nodes[0]
        size = self.size(root)
        root = self.balanceTreeHelper(root, size-1)

        return root
    
    # Prints tree prettily
    def prettify(self):
        if self.nodes == []:
            print ("")
        else:
            print (RenderTree(self.nodes[0]))
        
    # gives a serialized version of the tree from some rooted node
    def serialize(self, root):
        result = ""
        for pre, fill, node in RenderTree(root):
            pre = "\t" * int(len(pre)/4)
            if len(node.children) != 0:
                result += ("%s%s" % (pre, node.op.value))
            else:
                result += ("%s value: %s" % (pre, node.value))
            
            result += "\n"
            
        return result

    def serializeJSON(self, node):
        if len(node.children) == 2:
            left = node.children[0]
            right = node.children[1]
            left = self.serializeJSON(left)
            right = self.serializeJSON(right)
            
            return {"operation": node.op.value, "children": [left, right]}
        elif len(node.children) == 1:
            child = self.serializeJSON(node.children[0])
            return {"operation": node.op.value, "children": [child]}
        else:
            return {"value": node.value}        

    def convertToSQL(self, node, select=False):
        if len(node.children) == 2:
            left = node.children[0]
            right = node.children[1]
            
            left = self.convertToSQL(left, select or node.op == Operator.SELECT)
            right = self.convertToSQL(right, select or node.op == Operator.SELECT)
            
            if (node.op in binary_ops_SQL.keys()):
                if (node.op == Operator.IN or node.op == Operator.NOTIN):
                    right = "(" + right + ")"
                
                if binary_ops_SQL[node.op][1]:
                    sql = left + " " + binary_ops_SQL[node.op][0] + " " + right
                else:
                    sql = right + " " + binary_ops_SQL[node.op][0] + " " + left
                                                    
                if (node.op == Operator.SELECT and select):
                    sql = "(" + sql + ")"
                
                return sql
            elif (node.op == Operator.OR):
                if ((node.children[0].op == Operator.GREATER_THAN) and (node.children[1].op == Operator.EQUAL)):
                    if (left.replace(">", "") == right.replace("=", "")):
                        sql = left.replace(">", ">=")
                        return sql
                elif ((node.children[0].op == Operator.LESS_THAN) and (node.children[1].op == Operator.EQUAL)):
                    if (left.replace("<", "") == right.replace("=", "")):
                        sql = left.replace("<", "<=")
                        return sql
                
                sql = left + " OR " + right
                return sql
            elif (node.op == Operator.AND):
                if (node.children[0].op == Operator.GREATER_THAN and node.children[1].op == Operator.LESS_THAN):
                    if (left.split(">")[0] == right.split("<")[0]):
                        sql = left.split(">")[0] + "BETWEEN" + left.split(">")[1] + " AND" + right.split("<")[1]
                        return sql
                sql = left + " AND " + right
                return sql
        
            elif (node.op == Operator.SELECT):
                if (node.children[0].op == Operator.DISTINCT):
                    data = re.match((r"DISTINCT\((.*)\)"), left)
                    left = "DISTINCT "+ data[1]

                if (select):
                    sql = "(SELECT " + left + " FROM " + right + ")"
                else:
                    sql = "SELECT " + left + " FROM " + right
                        
                return sql
            elif (node.op == Operator.ARITHMETIC):
                sql = left + " " + node.value + " " + right
                return sql
            elif (node.op == Operator.ORDERBY_ASC):
                sql = right + " ORDER BY " + left + " ASC"
                return sql
            elif (node.op == Operator.ORDERBY_DSC):
                sql = right + " ORDER BY " + left + " DESC"
                return sql
            elif (node.op == Operator.JOIN):
                # for each join stmt, return a list of relations deepest first
                sql = left + " JOIN " + right
                return sql
            elif (node.op == Operator.WHERE):
                if (node.children[1].op == Operator.JOIN):
                    # left is the relation, right is the join statements
                    if ("JOIN" in right):
                        right = right.split(" JOIN ")
                        right[1] = right[1] + " ON " + left
                        sql = " JOIN ".join(right)
                    else:
                        sql = right + " ON " + left
                    
                elif (node.children[1].op == Operator.SELECT):
                    sql = right + " HAVING " + left
                else:
                    sql = right + " WHERE " + left
                return sql
            else:
                print (node.op)
                print (left)
                print (right)
                return "ERROR"     
                   
        elif len(node.children) == 1:
            child = self.convertToSQL(node.children[0], select)
            if (node.children[0].op == Operator.DISTINCT):
                data = re.match((r"DISTINCT\((.*)\)"), child)
                child = "DISTINCT "+ data[1]

            if (node.op in unary_ops_SQL.keys()):
                sql = unary_ops_SQL[node.op] + "(" + child + ")"
                return sql
            elif (node.op == Operator.KEEP):
                return child
            
            return "ERROR"
        else:
            if (node.value == "STAR"):
                return "*"
            
            if type(node.value) is float:
                if (str(node.value)[-1] == "0"):
                    return str(int(node.value))

            return str(node.value)

def unserialize_helper(lst, ast, idx):
    if ("value" in lst[idx]):
        leaf = lst[idx].split(":")[1]
        if (ast.constType(leaf) == "relation"):    
            return (ast.createNode(Operator.RELATION_LEAF, None, None, value = leaf), idx+1)
        else:
            return (ast.createNode(Operator.CONST_LEAF, None, None, value = leaf), idx+1)
    elif ((ops_inputs[Operator(lst[idx])])[1] == Type.EMPTY):
        op = Operator(lst[idx])
        (child,new_idx) = unserialize_helper(lst, ast, idx+1)
        return (ast.createNode(op, child, None, None), new_idx)
    else:
        op = Operator(lst[idx])
        (left, new_idx) = unserialize_helper(lst, ast, idx+1)
        (right, final_idx) = unserialize_helper(lst, ast, new_idx)
        return (ast.createNode(op, left, right, None), final_idx)

def unserialize(text, db_id):
    lst = text.split("\n")
    lst = [x.strip() for x in lst]
    
    ast = AST(db_id)
    tree, _ = unserialize_helper(lst, ast, 0)
    
    return tree
