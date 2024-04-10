# coding: utf8

import json
with open('../proposicoes/output/preposicoes_detalhes_limpos_2.json', 'r', encoding='utf-8-sig') as openfile:
    prepositions = json.load(openfile)

    results = []
    for inner_preps in prepositions["200"]:
            results.append(inner_preps['uriAutores'])

    with open("output/lista_preposicoes_autores_2.json", "w", encoding='utf8') as outfile:
        json.dump(results, outfile, indent=4, ensure_ascii=False)