from lexer import Lexer
from parser_2 import Parser
from anytree import Node, RenderTree
import json
from ast_sql import *

# removed the following from train_gold.sql:
# SELECT T1.company_name FROM Third_Party_Companies AS T1 JOIN Maintenance_Contracts AS T2 ON T1.company_id  =  T2.maintenance_contract_company_id JOIN Ref_Company_Types AS T3 ON T1.company_type_code  =  T3.company_type_code ORDER BY T2.contract_end_date DESC LIMIT 1	assets_maintenance

# stmt = "SELECT count(*) FROM head WHERE age  >  56	department_management"
f = open("spider/train_gold.sql", "r")

test = ["SELECT DISTINCT T1.artist_name ,  T1.country FROM artist AS T1 JOIN song AS T2 ON T1.artist_name  =  T2.artist_name WHERE T2.rating  >  9  music_1"]

for stmt in test: #f.readlines():

    print (stmt)

    db_id = stmt.split()[-1]
    #if "phone_1" in db_id or "match_season" in db_id: pass
    #else:
    text = " ".join(stmt.split()[:-1])

    l = Lexer(db_id).get_lexer()
    p = Parser(db_id)

    p2 = p.get_parser()
    
    #print (list(l.lex(text)))
    tree = p2.parse(l.lex(text))
    #tree = p.get_ast().balanceTree()
    
    print (RenderTree(tree))
    print (p.get_ast().serialize(tree))
    
    serialize = p.get_ast().serialize(tree)
    
    print (RenderTree(unserialize(serialize, db_id)))
    
    #json_data = json.dumps(p.get_ast().serializeJSON(tree))
    #print (json_data)
    
    print (p.get_ast().convertToSQL(tree))
    
    _ = '''
    if not (Parser(db_id).get_ast().valid(tree)):
        print (RenderTree(tree))
        Parser().get_ast().valid(tree, True)
    '''
    
f.close()