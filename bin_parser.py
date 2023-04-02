from rply import ParserGenerator
from ast import *

# SELECT count(*) FROM head WHERE age  >  56

class Parser():
    def __init__(self):
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            ['SELECT', 'FROM', 'ORDER_BY', 'ASC', 'DSC', 'COMMA', 'COUNT', 'OPEN_PAREN', 'CLOSE_PAREN',
             'STAR', 'FROM', 'STRING', 'WHERE', 'GREATER', 'NUMBER']
        )
        self.AST = AST()

        # Clauses
        @self.pg.production('expression : SELECT constList FROM expression')
        def expression_select(p):
            selectClause = p[1]
            predicate = p[3]
            
            return self.AST.createNode(Operator.PROJECTION, selectClause, predicate, None)

        @self.pg.production('expression : expression WHERE expression')
        def expression_from(p):
            fromClause = p[0]
            whereClause = p[2]
            
            return self.AST.createNode(Operator.SELECTION, fromClause, whereClause, None)

        @self.pg.production('expression : expression ORDER_BY constList order')
        def expression_orderby(p):
            relation = p[0]
            constlist = p[2]
            if (len(p) == 3):
                order = "ASC"
            else:
                order = p[3]

            if order == "ASC":
                return self.AST.createNode(Operator.ORDERBY_ASC, constlist, relation, None)
            else:
                return self.AST.createNode(Operator.ORDERBY_DSC, constlist, relation, None)

        @self.pg.production('expression : expression GREATER expression')
        def expression_comp(p):
            left = p[0]
            right = p[2]
            if p[1].gettokentype()  == "GREATER":
                return self.AST.createNode(Operator.GREATER_THAN, left, right, None)

        @self.pg.production('expression : COUNT expression')
        def expression_agg(p):
            v = p[1]
            if p[0].gettokentype()  == "COUNT":
                return self.AST.createNode(Operator.COUNT, v, None, None)

        @self.pg.production('expression : OPEN_PAREN expression CLOSE_PAREN')
        def expression_parens(p):
            return p[1]

        @self.pg.production('constList : constVal COMMA constList')
        @self.pg.production('constList : constVal')
        def expression_constlist(p):
            if len(p) == 1:
                return p[0] 
            else:
                left = p[0]
                right = p[2]

                return self.AST.createNode(Operator.UNION_CONST, left, right, None)

        @self.pg.production('constVal : STRING')
        @self.pg.production('constVal : NUMBER')
        @self.pg.production('constVal : STAR')
        def expression_constval(p):
            if p[0].gettokentype() == "STRING":
                return self.AST.createNode(Operator.CONST_LEAF, None, None, p[0].getstr())
            elif p[0].gettokentype() == "NUMBER":
                return self.AST.createNode(Operator.CONST_LEAF, None, None, int(p[0].getstr()))
            else:
                return self.AST.createNode(Operator.CONST_LEAF, None, None, "STAR")

        @self.pg.production('order : ASC')
        @self.pg.production('order : DSC')
        @self.pg.production('order : ')
        def expression_order(p):
            if (len(p) == 0):
                return "ASC"
            
            if p[0].gettokentype() == "ASC":
                return "ASC"
            elif p[0].gettokentype() == "DSC":
                return "DSC"

        @self.pg.production('expression : STAR')
        def expression_string(p):
            # p is a list of the pieces matched by the right hand side of the
            # rule
            return self.AST.createNode(Operator.CONST_SET_LEAF, None, None, [p[0].getstr()])

        @self.pg.production('expression : NUMBER')
        def expression_number(p):
            # p is a list of the pieces matched by the right hand side of the
            # rule
            return self.AST.createNode(Operator.CONST_LEAF, None, None, int(p[0].getstr()))

        @self.pg.production('expression : STRING')
        def expression_string(p):
            # p is a list of the pieces matched by the right hand side of the
            # rule
            return self.AST.createNode(Operator.CONST_LEAF, None, None, p[0].getstr())
        
        @self.pg.error
        def error_handle(token):
            raise ValueError(token)


    def get_parser(self):
        return self.pg.build()
