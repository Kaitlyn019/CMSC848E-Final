from lexer import Lexer
from parser_2 import Parser
from anytree import Node, RenderTree

# stmt = "SELECT count(*) FROM head WHERE age  >  56	department_management"
f = open("spider/train_gold.sql", "r")

test = ['SELECT T2.name FROM Certificate AS T1 JOIN Aircraft AS T2 ON T2.aid  =  T1.aid WHERE T2.distance  >  5000 GROUP BY T1.aid ORDER BY count(*)  >=  5      flight_1']

for stmt in f.readlines():

    print (stmt)

    db_id = stmt.split()[-1]
    if "phone_1" in db_id or "match_season" in db_id: pass
    else:
        text = " ".join(stmt.split()[:-1])

        l = Lexer(db_id).get_lexer()
        p = Parser().get_parser()

        #print (list(l.lex(text)))
        tree = p.parse(l.lex(text))
        
        #print (RenderTree(tree))

        if not (Parser().get_ast().valid(tree)):
            print (RenderTree(tree))
            Parser().get_ast().valid(tree, True)

f.close()