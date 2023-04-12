from rply import ParserGenerator
from ast_sql import AST, Type, Operator

# SELECT count(*) FROM head WHERE age  >  56

class Parser():
    def __init__(self):
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            ['SELECT','WHERE','FROM','ORDER_BY','GROUP_BY','HAVING','LIMIT',
             'DISTINCT','STAR','AS','JOIN','ON','COUNT','MAX','MIN','SUM',
             'AVG','COMMA','OPEN_PAREN','CLOSE_PAREN','GREATER_EQUAL','GREATER',
             'LESS_EQUAL','LESS','EQUAL','NOT_EQUAL','AND','OR','NOTIN','IN',
             'BETWEEN','NOTLIKE','LIKE','ASC','DSC','RELATION','CLM_NAME',
             'TEXT','NUMBER','STRING', 'INTERSECT','UNION','EXCEPT', 'MINUS', 'ADD', 'MULTIPLY', 'DIVIDE'
             ]
        )
        self.AST = AST()

        # Clauses
        @self.pg.production('expression : SELECT constList FROM fromStmt')
        @self.pg.production('expression : SELECT DISTINCT constList FROM fromStmt')
        def expression_select(p):
            if len(p) == 4:
                selectClause = p[1]
                (relation, post)  = p[3]
            
                result = self.AST.createNode(Operator.PROJECTION, selectClause, relation, None)
            else:
                selectClause = p[2]
                (relation, post)  = p[4]
            
                result = self.AST.createNode(Operator.PROJECTION, 
                                             self.AST.createNode(Operator.DISTINCT, selectClause, None, None), relation, None)

            if post['HAVING'] != None:
                result = self.AST.createNode(Operator.SELECTION, post['HAVING'], result, None)
            
            if post['ORDERBY'] != None:
                (asc, const) = post['ORDERBY']
                if asc:
                    result = self.AST.createNode(Operator.ORDERBY_ASC, const, result, None)
                else: 
                    result = self.AST.createNode(Operator.ORDERBY_DSC, const, result, None)

            if post['LIMIT'] != None:
                result = self.AST.createNode(Operator.LIMIT, post['LIMIT'], result, None)

            if post['SET'] != None:
                (op, expr) = post['SET']

                if op == "INTERSECT":
                    result = self.AST.createNode(Operator.INTERSECTION_SET, result, expr, None)
                elif op == "UNION":
                    result = self.AST.createNode(Operator.UNION_SET, result, expr, None)
                elif op == "EXCEPT":
                    result = self.AST.createNode(Operator.DIFFERENCE_SET, result, expr, None)

            return result         

        # each of these produce a predicate rule
        @self.pg.production('postFromStmt : whereStmt gbyStmt hvgStmt obyStmt limitStmt setStmt')
        def expression_postfrom(p):
            return {'WHERE': p[0], 'GROUPBY': p[1], 'HAVING': p[2], 'ORDERBY': p[3], 'LIMIT': p[4], 'SET': p[5]}

        @self.pg.production('setStmt : INTERSECT expression')
        @self.pg.production('setStmt : UNION expression')
        @self.pg.production('setStmt : EXCEPT expression')
        @self.pg.production('setStmt : ')
        def expression_setStmt(p):
            if len(p) == 0:
                return None
            if p[0].gettokentype() == "INTERSECT":
                expr = p[1]
                return ("INTERSECT", expr)
            elif p[0].gettokentype() == "UNION":
                expr = p[1]
                return ("UNION", expr)
            elif p[0].gettokentype() == "EXCEPT":
                expr = p[1]
                return ("EXCEPT", expr)

        @self.pg.production('fromStmt : relation postFromStmt')
        @self.pg.production('fromStmt : relation joinStmt postFromStmt')
        def expression_from(p):
            post = p[len(p)-1]
            fromClause = None
            if len(p) == 3: # has a join
                orig_relation = p[0]
                (join_relation, join_pred) = p[1]
                
                relation = self.AST.createNode(Operator.CARTESIAN, orig_relation, join_relation, None)
                fromClause = self.AST.createNode(Operator.SELECTION, join_pred, relation, None)

            else: # does not have join
                fromClause = p[0]

            if post['WHERE'] != None:
                fromClause = self.AST.createNode(Operator.SELECTION, post['WHERE'], fromClause, None)

            if post['GROUPBY'] != None:
                fromClause = self.AST.createNode(Operator.GROUPBY, post['GROUPBY'], fromClause, None)

            return (fromClause, post)


        @self.pg.production('relation : RELATION')
        @self.pg.production('relation : RELATION AS TEXT')
        def expression_relation(p):
            if len(p) == 1:
                return self.AST.createNode(Operator.RELATION_LEAF, None, None, p[0].getstr())
            else:
                relation = self.AST.createNode(Operator.RELATION_LEAF, None, None, p[0].getstr())
                rename = self.AST.createNode(Operator.CONST_LEAF, None, None, p[2].getstr())
                return self.AST.createNode(Operator.AS, rename, relation, None)

        @self.pg.production('joinCondList : clmName EQUAL clmName AND joinCondList')
        @self.pg.production('joinCondList : clmName EQUAL clmName')
        def expression_joincondlist(p):
            if len(p) == 3:
                clm1 = p[0]
                clm2 = p[2]

                return self.AST.createNode(Operator.EQUAL, clm1, clm2, None)
            else:
                join = p[4]
                clm1 = p[0]
                clm2 = p[2]

                return self.AST.createNode(Operator.AND, self.AST.createNode(Operator.EQUAL, clm1, clm2, None), join, None)

        @self.pg.production('joinStmt : JOIN relation ON joinCondList joinStmt')
        @self.pg.production('joinStmt : JOIN relation ON joinCondList')
        @self.pg.production('joinStmt : JOIN relation joinStmt')
        def expression_joinstmt(p):
            if len(p) == 4: # end of joins
                relation = p[1]
                pred = p[3]

                return (relation, pred)
            elif len(p) == 3: # more joins but no on stmt
                relation = p[1]
                (relation2, pred) = p[2]

                return (self.AST.createNode(Operator.CARTESIAN, relation, relation2, None), pred)

            else: # if there are multiple, connect with a selection first?
                relation = p[1]
                pred = p[3]
                
                (relation2, pred2) = p[4] # next join stmt
                
                selection = self.AST.createNode(Operator.SELECTION, pred2, 
                    self.AST.createNode(Operator.CARTESIAN, relation, relation2, None), None)
                
                return (selection, pred)
            
        # SELECT
        @self.pg.production('constList : constVal COMMA constList')
        @self.pg.production('constList : constVal')
        @self.pg.production('constList : calculate')
        def expression_constlist(p):
            if len(p) == 1:
                return p[0] 
            else:
                left = p[0]
                right = p[2]

                return self.AST.createNode(Operator.UNION_CONST, left, right, None)

        @self.pg.production('constVal : const')
        @self.pg.production('constVal : clmName')
        @self.pg.production('constVal : aggVal')
        @self.pg.production('constVal : OPEN_PAREN expression CLOSE_PAREN')
        def expression_constval(p):
            if len(p) == 1:
                return p[0]
            else:
                return p[1]

        @self.pg.production('clmName : OPEN_PAREN DISTINCT CLM_NAME CLOSE_PAREN')
        @self.pg.production('clmName : DISTINCT CLM_NAME')
        @self.pg.production('clmName : DISTINCT OPEN_PAREN CLM_NAME CLOSE_PAREN')
        @self.pg.production('clmName : CLM_NAME')
        @self.pg.production('clmName : STAR')
        def expression_clmname(p):
            if len(p) == 4:
                clm = self.AST.createNode(Operator.CONST_LEAF, None, None, p[2].getstr())
                return self.AST.createNode(Operator.DISTINCT, clm, None, None)
            elif len(p) == 2:
                clm = self.AST.createNode(Operator.CONST_LEAF, None, None, p[1].getstr())
                return self.AST.createNode(Operator.DISTINCT, clm, None, None)
            elif p[0].gettokentype() == "STAR":
                return self.AST.createNode(Operator.CONST_LEAF, None, None, "STAR")
            else:
                return self.AST.createNode(Operator.CONST_LEAF, None, None, p[0].getstr())

        @self.pg.production('calculate : constVal MINUS constVal')
        @self.pg.production('calculate : constVal ADD constVal')
        @self.pg.production('calculate : constVal MULTIPLY constVal')
        @self.pg.production('calculate : constVal DIVIDE constVal')
        def expression_calculate(p):
            left = p[0]
            right = p[2]

            return self.AST.createNode(Operator.ARITHMETIC, left, right, p[1].getstr())


        @self.pg.production('const : STRING')
        @self.pg.production('const : NUMBER')
        def expression_const(p):
            if p[0].gettokentype() == "STRING":
                return self.AST.createNode(Operator.CONST_LEAF, None, None, p[0].getstr())
            elif p[0].gettokentype() == "NUMBER":
                return self.AST.createNode(Operator.CONST_LEAF, None, None, float(p[0].getstr()))

        @self.pg.production('aggVal : COUNT OPEN_PAREN clmName CLOSE_PAREN')
        @self.pg.production('aggVal : SUM OPEN_PAREN clmName CLOSE_PAREN')
        @self.pg.production('aggVal : MAX OPEN_PAREN clmName CLOSE_PAREN')
        @self.pg.production('aggVal : MIN OPEN_PAREN clmName CLOSE_PAREN')
        @self.pg.production('aggVal : AVG OPEN_PAREN clmName CLOSE_PAREN')
        def expression_agg(p):
            v = p[2]
            if p[0].gettokentype()  == "COUNT":
                return self.AST.createNode(Operator.COUNT, v, None, None)
            elif p[0].gettokentype()  == "SUM":
                return self.AST.createNode(Operator.SUM, v, None, None)
            elif p[0].gettokentype()  == "MAX":
                return self.AST.createNode(Operator.MAX, v, None, None)
            elif p[0].gettokentype()  == "MIN":
                return self.AST.createNode(Operator.MIN, v, None, None)
            else:
                return self.AST.createNode(Operator.AVG, v, None, None)

        # WHERE
        @self.pg.production('whereStmt : WHERE conditionLst')
        @self.pg.production('whereStmt : ')
        def expression_wherestmt(p):
            if len(p) == 0: 
                return None
            else:
                return p[1]
        
        @self.pg.production('conditionLst : vCondition AND conditionLst')
        @self.pg.production('conditionLst : vCondition OR conditionLst')
        @self.pg.production('conditionLst : vCondition')
        def expression_conditionLst(p):
            if len(p) == 1:
                return p[0] 
            elif p[1].gettokentype() == "AND":
                left = p[0]
                right = p[2]

                return self.AST.createNode(Operator.AND, left, right, None)
            elif p[1].gettokentype() == "OR":
                left = p[0]
                right = p[2]

                return self.AST.createNode(Operator.OR, left, right, None)

        @self.pg.production('vCondition : clmName IN OPEN_PAREN expression CLOSE_PAREN')
        @self.pg.production('vCondition : clmName NOTIN OPEN_PAREN expression CLOSE_PAREN')
        @self.pg.production('vCondition : condition')
        def expression_vcondition(p):
            if len(p) == 1:
                return p[0]
            elif p[1].gettokentype() == "IN":
                clmName = p[0]
                relation = p[3]

                return self.AST.createNode(Operator.IN, clmName, relation, None)
            elif p[1].gettokentype() == "NOTIN":
                clmName = p[0]
                relation = p[3]

                return self.AST.createNode(Operator.NOTIN, clmName, relation, None)

        @self.pg.production('condition : compcondition')
        @self.pg.production('condition : condVal BETWEEN const AND const')
        @self.pg.production('condition : condVal LIKE STRING') # FLAG: UPDATE FOR REGEX
        @self.pg.production('condition : condVal NOTLIKE STRING') # FLAG: UPDATE FOR REGEX
        def expression_condition(p):
            if len(p) == 1:
                return p[0]
            if p[1].gettokentype() == "BETWEEN":
                val = p[0]
                val_copy = self.AST.copyNode(val)

                bound1 = p[2]
                bound2 = p[4]

                left = self.AST.createNode(Operator.GREATER_THAN, val, bound1, None)
                right = self.AST.createNode(Operator.LESS_THAN, val_copy, bound2, None)

                return self.AST.createNode(Operator.AND, left, right, None)
            elif p[1].gettokentype() == "LIKE":
                val = p[0]
                akin = self.AST.createNode(Operator.CONST_LEAF, None, None, p[2].getstr())

                return self.AST.createNode(Operator.LIKE, val, akin, None)
            elif p[1].gettokentype() == "NOTLIKE":
                val = p[0]
                akin = self.AST.createNode(Operator.CONST_LEAF, None, None, p[2].getstr())

                return self.AST.createNode(Operator.NOTLIKE, val, akin, None)

        @self.pg.production('compcondition : condVal GREATER condVal')
        @self.pg.production('compcondition : condVal LESS condVal')
        @self.pg.production('compcondition : condVal GREATER_EQUAL condVal')
        @self.pg.production('compcondition : condVal LESS_EQUAL condVal')
        @self.pg.production('compcondition : condVal EQUAL condVal')
        @self.pg.production('compcondition : condVal NOT_EQUAL condVal')
        def expression_comp(p):
            left = p[0]
            right = p[2]
            if p[1].gettokentype()  == "GREATER":
                return self.AST.createNode(Operator.GREATER_THAN, left, right, None)
            elif p[1].gettokentype() == "GREATER_EQUAL":
                left_copy = self.AST.copyNode(left)
                right_copy = self.AST.copyNode(right)

                return self.AST.createNode(Operator.AND,
                        self.AST.createNode(Operator.GREATER_THAN, left, right, None),
                        self.AST.createNode(Operator.EQUAL, left_copy, right_copy, None), None)
            elif p[1].gettokentype()  == "LESS":
                return self.AST.createNode(Operator.LESS_THAN, left, right, None)
            elif p[1].gettokentype() == "LESS_EQUAL":
                left_copy = self.AST.copyNode(left)
                right_copy = self.AST.copyNode(right)

                return self.AST.createNode(Operator.AND,
                        self.AST.createNode(Operator.LESS_THAN, left, right, None),
                        self.AST.createNode(Operator.EQUAL, left_copy, right_copy, None), None)
            elif p[1].gettokentype()  == "EQUAL":
                return self.AST.createNode(Operator.EQUAL, left, right, None)
            elif p[1].gettokentype() == "NOT_EQUAL":
                return self.AST.createNode(Operator.NOT_EQUAL, left, right, None)

        @self.pg.production('condVal : const')
        @self.pg.production('condVal : clmName')
        @self.pg.production('condVal : OPEN_PAREN expression CLOSE_PAREN')
        def expression_condval(p):
            if len(p) == 1:
                return p[0]
            else:
                return p[1]
        
        # Groupby
        @self.pg.production('gbyStmt : GROUP_BY gbyValLst')
        @self.pg.production('gbyStmt : ')
        def expression_gbystmt(p):
            if len(p) == 0: 
                return None
            else:
                return p[1]

        @self.pg.production('gbyValLst : gbyVal COMMA gbyValLst')
        @self.pg.production('gbyValLst : gbyVal')
        def expression_gbyvallst(p):
            if len(p) == 1:
                return p[0]
            else:
                left = p[0]
                right = p[2]

                return self.AST.createNode(Operator.UNION_CONST, left, right, None)

        @self.pg.production('gbyVal : OPEN_PAREN clmName CLOSE_PAREN')
        @self.pg.production('gbyVal : clmName')
        @self.pg.production('gbyVal : aggVal')
        def expression_gbyval(p):
            if len(p) == 1:
                return p[0]
            else:
                return p[1]
                
        # Having
        @self.pg.production('hvgStmt : HAVING hvgCompCondition')
        @self.pg.production('hvgStmt : ')
        def expression_hvgstmt(p):
            if len(p) == 0:
                return None;
            return p[1]
        
        # OrderBy
        @self.pg.production('obyStmt : ORDER_BY obyConstList order')
        @self.pg.production('obyStmt : ')
        def expression_orderby(p):   
            if len(p) == 0:
                return None         
            
            return (p[2], p[1])
        
        @self.pg.production('obyConstVal : const')
        @self.pg.production('obyConstVal : clmName')
        @self.pg.production('obyConstVal : aggVal')
        @self.pg.production('obyConstVal : calculate')
        @self.pg.production('obyConstVal : hvgCompCondition')
        @self.pg.production('obyConstVal : OPEN_PAREN expression CLOSE_PAREN')
        def expression_obyconstval(p):
            if len(p) == 1:
                return p[0]
            else:
                return p[1]


        @self.pg.production('obyConstList : obyConstVal COMMA obyConstList')
        @self.pg.production('obyConstList : obyConstVal')
        def expression_obyconstlist(p):
            if len(p) == 1:
                return p[0] 
            else:
                left = p[0]
                right = p[2]

                return self.AST.createNode(Operator.UNION_CONST, left, right, None)


        @self.pg.production('hvgCompCondition : constVal GREATER constVal')
        @self.pg.production('hvgCompCondition : constVal LESS constVal')
        @self.pg.production('hvgCompCondition : constVal GREATER_EQUAL constVal')
        @self.pg.production('hvgCompCondition : constVal LESS_EQUAL constVal')
        @self.pg.production('hvgCompCondition : constVal EQUAL constVal')
        @self.pg.production('hvgCompCondition : constVal NOT_EQUAL constVal')
        def expression_hvgComp(p):
            left = p[0]
            right = p[2]
            if p[1].gettokentype()  == "GREATER":
                return self.AST.createNode(Operator.GREATER_THAN, left, right, None)
            elif p[1].gettokentype() == "GREATER_EQUAL":
                left_copy = self.AST.copyNode(left)
                right_copy = self.AST.copyNode(right)

                return self.AST.createNode(Operator.OR,
                        self.AST.createNode(Operator.GREATER_THAN, left, right, None),
                        self.AST.createNode(Operator.EQUAL, left_copy, right_copy, None), None)
            elif p[1].gettokentype()  == "LESS":
                return self.AST.createNode(Operator.LESS_THAN, left, right, None)
            elif p[1].gettokentype() == "LESS_EQUAL":
                left_copy = self.AST.copyNode(left)
                right_copy = self.AST.copyNode(right)

                return self.AST.createNode(Operator.OR,
                        self.AST.createNode(Operator.LESS_THAN, left, right, None),
                        self.AST.createNode(Operator.EQUAL, left_copy, right_copy, None), None)
            elif p[1].gettokentype()  == "EQUAL":
                return self.AST.createNode(Operator.EQUAL, left, right, None)
            elif p[1].gettokentype() == "NOT_EQUAL":
                return self.AST.createNode(Operator.NOT_EQUAL, left, right, None)


        @self.pg.production('expression : OPEN_PAREN expression CLOSE_PAREN')
        def expression_parens(p):
            return p[1]

        @self.pg.production('order : ASC')
        @self.pg.production('order : DSC')
        @self.pg.production('order : ')
        def expression_order(p):
            if len(p) == 0:
                return "ASC"
            
            if p[0].gettokentype() == "ASC":
                return "ASC"
            elif p[0].gettokentype() == "DSC":
                return "DSC"

        @self.pg.production ('limitStmt : LIMIT NUMBER')
        @self.pg.production('limitStmt : ')
        def limitStmt(p):
            if len(p) == 0:
                return None
            else:
                return (self.AST.createNode(Operator.CONST_LEAF, None, None, int(p[1].getstr())))

        @self.pg.production('expression : STAR')
        def expression_string(p):
            # p is a list of the pieces matched by the right hand side of the
            # rule
            return self.AST.createNode(Operator.CONST_SET_LEAF, None, None, [p[0].getstr()])

        @self.pg.production('expression : NUMBER')
        def expression_number(p):
            # p is a list of the pieces matched by the right hand side of the
            # rule
            return self.AST.createNode(Operator.CONST_LEAF, None, None, float(p[0].getstr()))

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
    
    def get_ast(self):
        return self.AST
