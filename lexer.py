from rply import LexerGenerator
import pandas as pd
import re 

tables = pd.read_json("spider/tables.json")
tables = tables.set_index('db_id')

class Lexer():
    def __init__(self, db_id):
        self.lexer = LexerGenerator()
        self.db_id = db_id

    def _add_tokens(self):
        # Clauses
        self.lexer.add('SELECT', r'SELECT')
        self.lexer.add('WHERE', r'WHERE')
        self.lexer.add('FROM', r'FROM')
        self.lexer.add('ORDER_BY', r'ORDER BY')
        self.lexer.add('GROUP_BY', r'GROUP BY')
        self.lexer.add('HAVING', r'HAVING')
        self.lexer.add('LIMIT', r'LIMIT')

        # Schema Const
        clms = list(map(lambda x: str.lower(x[1]), tables.loc[self.db_id]['column_names_original']))
        clms.remove('*')
        clms.sort(key=len)
        clms.reverse()

        self.lexer.add('CLM_NAME', re.compile("\w+\.("+("|".join(clms))+")", re.IGNORECASE))
        
        ts = list(map(lambda x: str.lower(x), tables.loc[self.db_id]['table_names_original']))
        ts.sort(key=len)
        ts.reverse()

        i = 0
        j = 0
        while (i < len(clms) and j < len(ts)):
            if (len(clms[i]) >= len(ts[j])):
                self.lexer.add('CLM_NAME', re.compile(clms[i], re.IGNORECASE))
                i += 1
            else:
                self.lexer.add('RELATION', re.compile(ts[j], re.IGNORECASE))
                j += 1
        
        if (i < len(clms)):
            self.lexer.add('CLM_NAME', re.compile("|".join(clms[i:]), re.IGNORECASE))
        else:
            self.lexer.add('RELATION', re.compile("|".join(ts[j:]), re.IGNORECASE))

        # self.lexer.add('CLM_NAME', re.compile("|".join(clms), re.IGNORECASE))
        # self.lexer.add('RELATION', re.compile("|".join(ts), re.IGNORECASE))

        # Asc/Dsc
        self.lexer.add('ASC', r'asc|ASC')
        self.lexer.add('DSC', r'desc|DESC')

        # Select
        self.lexer.add('DISTINCT', r'distinct|DISTINCT')
        self.lexer.add('STAR', r'\*')
        self.lexer.add('AS', r'as |AS ')
        self.lexer.add('JOIN', r'join|JOIN')
        self.lexer.add('ON', r'on|ON')
        self.lexer.add('INTERSECT', r'intersect|INTERSECT')
        self.lexer.add('UNION', r'union|UNION')        
        self.lexer.add('EXCEPT', r'except|EXCEPT')

        # Aggregates
        self.lexer.add('COUNT', r'count|COUNT')
        self.lexer.add('MAX', r'max|MAX')
        self.lexer.add('MIN', r'min|MIN')
        self.lexer.add('SUM', r'sum|SUM')
        self.lexer.add('AVG', r'avg|AVG')

        # SYMBOLS
        self.lexer.add('COMMA', r',')
        self.lexer.add('OPEN_PAREN', r'\(')
        self.lexer.add('CLOSE_PAREN', r'\)')

        # Math
        self.lexer.add('MINUS', r'-')
        self.lexer.add('DIVIDE', r'/')
        self.lexer.add('ADD', r'\+')
        self.lexer.add('MULTIPLY', r'\*')

        # Operators
        self.lexer.add('GREATER_EQUAL', r'>=')
        self.lexer.add('GREATER', r'>')
        self.lexer.add('LESS_EQUAL', r'<=')
        self.lexer.add('LESS', r'<')
        self.lexer.add('EQUAL', r'=')
        self.lexer.add('NOT_EQUAL', r'!=')
        self.lexer.add('AND',r'and|AND')
        self.lexer.add('OR', r'or|OR')
        self.lexer.add('NOTIN', r'NOT IN|not in')
        self.lexer.add('IN', r'in|IN')
        self.lexer.add('BETWEEN', r'between|BETWEEN')
        self.lexer.add('NOTLIKE', r'not like|NOT LIKE')
        self.lexer.add('LIKE', r'like|LIKE')

        # Number
        # self.lexer.add('REGEX', r'[\'|"]%[A-z ]+%[\'|"]')
        self.lexer.add('NUMBER', r'\d+(\.\d+)?')
        self.lexer.add('STRING', r'[\'][^\']*[\']|[\"][^\"]*[\"]')

        self.lexer.add('TEXT', r'\w+')

        # Ignore spaces
        self.lexer.ignore('\s+')
        self.lexer.ignore(';')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()