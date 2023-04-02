from lexer import Lexer
from parser_2 import Parser
from anytree import Node, RenderTree

l = Lexer().get_lexer()
p = Parser().get_parser()

print (list(l.lex("SELECT age, count(name) FROM head WHERE age > 56 GROUP BY age")))
print (RenderTree(p.parse(l.lex("SELECT age, count(name) FROM head WHERE age > 56 GROUP BY age"))))