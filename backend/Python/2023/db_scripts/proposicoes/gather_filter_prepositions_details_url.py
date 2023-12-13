# coding: utf8

import json

def capitalize_first_character(string):
    return string[0].upper() + string[1:]

with open('lista_preposicoes.json', 'r', encoding='utf-8-sig') as openfile:
    prepositions = json.load(openfile)

    results = []
    for inner_preps in prepositions:
        for p in inner_preps['dados']:
            results.append(p['uri'])

    with open("lista_preposicoes_detalhes_urls.json", "w", encoding='utf8') as outfile:
        json.dump(results, outfile, indent=4, ensure_ascii=False)