from rply import LexerGenerator

class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        # Clauses
        self.lexer.add('SELECT', r'SELECT')
        self.lexer.add('WHERE', r'WHERE')
        self.lexer.add('FROM', r'FROM')
        self.lexer.add('ORDER_BY', r'ORDER BY')
        self.lexer.add('GROUP_BY', r'GROUP BY')

        # Select
        self.lexer.add('DISTINCT', r'distinct|DISTINCT')
        self.lexer.add('STAR', r'\*')
        self.lexer.add('AS', r'as|AS')
        self.lexer.add('JOIN', r'join|JOIN')
        self.lexer.add('ON', r'on|ON')

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

        # Operators
        self.lexer.add('GREATER', r'>')
        self.lexer.add('LESS', r'<')
        self.lexer.add('EQUAL', r'=')
        self.lexer.add('NOT_EQUAL', r'!=')

        # Asc/Dsc
        self.lexer.add('ASC', r'asc|ASC')
        self.lexer.add('DSC', r'dsc|DSC')

        # Schema Const
        self.lexer.add('RELATION', r'head')
        self.lexer.add('CLM_NAME', r'[A-z]+')

        # Number
        self.lexer.add('NUMBER', r'\d+')
        self.lexer.add('STRING', r'[A-z]+')
        # self.lexer.add('STRING', r'\'[A-z]+\'')

        # Ignore spaces
        self.lexer.ignore('\s+')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()