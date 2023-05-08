from lexer import Lexer
from parser_2 import Parser
from anytree import Node, RenderTree
import json
import csv

f = open("spider/train_spider.json", "r")
results = []
data = json.load(f)

with open('serialized_data.csv', mode='w', encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    for q in data:
        db_id = q["db_id"]
        #if "phone_1" in db_id or "match_season" in db_id: pass
        #else:
        text = q["query"]

        l = Lexer(db_id).get_lexer()
        p = Parser(db_id)

        p2 = p.get_parser()
        
        tree = p2.parse(l.lex(text))
        tree = p.get_ast().balanceTree()
        
        serialized_tree = (p.get_ast().serialize(tree))
        
        json_data = json.dumps(p.get_ast().serializeJSON(tree))

        csv_writer.writerow([q["question"], db_id, text, serialized_tree, json_data])

f.close()