from enum import Enum

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
    
    SET_UNKNOWN = "SET_UNKNOWN"
    SET_BOOL = "SET_BOOL" # returns a single column
    SET_INT = "SET_INT" # returns a single column
    SET_STR = "SET_STR" # returns a single column
    SET_TIME = "SET_TIME" # returns a single column
    SET_OTHERS = "SET_OTHERS" # returns a single column

    RELATION = "RELATION" # returns multiple columns
    ERROR = "ERROR"
    UNKNOWN = "UNKNOWN"

class Operator(Enum):
    UNION_SET = "UNION"
    INTERSECTION_SET = "INTERSECTION"
    DIFFERENCE_SET = "DIFFERENCE"
    WHERE = "WHERE"
    JOIN = "JOIN"
    SELECT = "SELECT" # used to be PROJECTION
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
    KEEP = "KEEP"

ops_outputs = {
    Operator.UNION_SET: Type.RELATION,
    Operator.INTERSECTION_SET: Type.RELATION,
    Operator.DIFFERENCE_SET: Type.RELATION,
    Operator.WHERE: Type.RELATION,
    Operator.JOIN: Type.RELATION,
    Operator.SELECT: Type.RELATION,
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
    Operator.WHERE: (Type.PREDICATE, Type.RELATION),
    Operator.JOIN: (Type.RELATION, Type.RELATION),
    Operator.SELECT: (Type.CONST_SET, Type.RELATION),
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

table_types = {
    'text': CompleteType.SET_STR,
    'boolean': CompleteType.SET_BOOL,
    'number': CompleteType.SET_INT,
    'time': CompleteType.SET_TIME,
    'others': CompleteType.SET_OTHERS
}

# True: left / op / right, False: right / op / left
binary_ops_SQL = {
    Operator.UNION_SET: ("UNION", True),
    Operator.INTERSECTION_SET: ("INTERSECT", True),
    Operator.DIFFERENCE_SET: ("DIFFERENCE", True),
    Operator.GREATER_THAN: (">", True), 
    Operator.LESS_THAN: ("<", True),
    Operator.BETWEEN: ("BETWEEN", True),
    Operator.EQUAL: ("=", True),
    Operator.NOT_EQUAL: ("!=", True),
    Operator.IN: ("IN", True), # left child should be surrounded in parentheses 
    Operator.NOTIN: ("NOT IN", True),
    Operator.LIKE: ("LIKE", True),
    Operator.NOTLIKE: ("NOT LIKE", True),
    Operator.AS: ("AS", False),
    Operator.GROUPBY: ("GROUP BY", False),
    Operator.LIMIT: ("LIMIT", False),
    Operator.UNION_CONST: (",", True)
}

unary_ops_SQL = {
    Operator.SUM: "SUM",
    Operator.MAX: "MAX",
    Operator.MIN: "MIN",
    Operator.COUNT: "COUNT",
    Operator.AVG: "AVG",
    Operator.DISTINCT: "DISTINCT",
}

special_ops_SQL = {
    Operator.EMPTY: "",
    Operator.ARITHMETIC: "",
    Operator.ORDERBY_ASC: "ORDER BY ASC",
    Operator.ORDERBY_DSC: "ORDER BY DSC",
    Operator.WHERE: "WHERE",
    Operator.SELECT: "SELECT", # if not first select, surround in parentheses
    Operator.OR: "OR",
    Operator.AND: "AND",
    Operator.JOIN: "JOIN"
}