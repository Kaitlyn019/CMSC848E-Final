from lexer import Lexer
from parser_2 import Parser
from anytree import Node, RenderTree

# removed the following from train_gold.sql:
# SELECT T1.company_name FROM Third_Party_Companies AS T1 JOIN Maintenance_Contracts AS T2 ON T1.company_id  =  T2.maintenance_contract_company_id JOIN Ref_Company_Types AS T3 ON T1.company_type_code  =  T3.company_type_code ORDER BY T2.contract_end_date DESC LIMIT 1	assets_maintenance

# stmt = "SELECT count(*) FROM head WHERE age  >  56	department_management"
f = open("spider/train_gold.sql", "r")

test = ['SELECT active_to_date - active_from_date FROM customer_contact_channels  customers_and_addresses']

for stmt in f.readlines():

    print (stmt)

    db_id = stmt.split()[-1]
    #if "phone_1" in db_id or "match_season" in db_id: pass
    #else:
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