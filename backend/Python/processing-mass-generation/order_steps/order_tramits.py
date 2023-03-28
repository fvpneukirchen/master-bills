# coding: utf8

import json
from operator import itemgetter

file_name = 'tramit_2277150'

in_file_name = str(file_name) + ".json"
out_file_name = str(file_name) + "_out.json"
out_file_name_2 = str(file_name) + "_out_2.json"

with open(in_file_name, 'r', encoding='utf8') as openfile:
    json_object = json.load(openfile)

newlist = sorted(json_object['dados'], key=itemgetter('sequencia'))
newlist = [e for e in newlist if e["ambito"] != "Protocolar"]

# with open("tramit_2268646_out_2.json", "w", encoding='utf8') as outfile:
with open(out_file_name_2, "w", encoding='utf8') as outfile:
    json.dump(newlist, outfile, indent=4, ensure_ascii=False)
