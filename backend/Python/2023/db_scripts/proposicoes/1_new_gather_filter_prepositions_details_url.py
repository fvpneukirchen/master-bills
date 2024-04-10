# coding: utf8

import json

def capitalize_first_character(string):
    return string[0].upper() + string[1:]

with open('output/lista_preposicoes_2.json', 'r', encoding='utf-8-sig') as openfile:
    prepositions = json.load(openfile)

    results = []
    for inner_preps in prepositions["200"]:
        for p in inner_preps['dados']:
            if p['siglaTipo'] not in ('REQ','RIC'):
                results.append(p['uri'])

    with open("output/lista_preposicoes_detalhes_urls_2.json", "w", encoding='utf8') as outfile:
        json.dump(results, outfile, indent=4, ensure_ascii=False)