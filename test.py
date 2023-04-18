import pandas as pd

tables = pd.read_json("spider/tables.json")
tables = tables.set_index('db_id')

db_id = "customers_and_addresses"

   # Code iterates through the json version of the tables to create a dataframe for all data in the db
   # which has the column names, table name, types, is_primary, and foreign key pairs in list [(table, column),...]
ct = 1
temp = tables.loc[db_id]
curr_table = []
schema = []

while ct < len(temp["column_names_original"]):
    (index, name) = temp["column_names_original"][ct]

            # if index > len(self.schema):
            #    df = pd.DataFrame(curr_table.copy(), columns=["name","type","is_primary","foreign_keys"]).set_index("name")
            #    self.schema[(temp["table_names_original"][index-1]).lower()] = df
            #    curr_table = []

            # name of column, table, type of column, is primary, matching foreigns in list [(table, column),...]
    is_primary = True if ct in temp["primary_keys"] else False
    table = (temp["table_names_original"][index]).lower()
    curr_table.append([name.lower(), table, temp["column_types"][ct], is_primary, []])

    ct += 1

schema = pd.DataFrame(curr_table.copy(), columns=["clm_name", "table_name", "clm_type", "is_primary", "foreign_keys"]).set_index(["table_name", "clm_name"])

for (key1, key2) in temp["foreign_keys"]:
    (table_1, name_1) = temp["column_names_original"][int(key1)]
    (table_2, name_2) = temp["column_names_original"][int(key2)]

    table_1 = temp["table_names_original"][int(table_1)].lower()
    table_2 = temp["table_names_original"][int(table_2)].lower()

    print (table_1, name_1.lower())

    schema.loc[table_1, name_1.lower()]["foreign_keys"].append((table_2, name_2.lower()))
    
    print (table_2, name_2.lower())

    schema.loc[table_2, name_2.lower()]["foreign_keys"].append((table_1, name_1.lower()))

print(temp)
print(temp['column_types'])
print(schema)
