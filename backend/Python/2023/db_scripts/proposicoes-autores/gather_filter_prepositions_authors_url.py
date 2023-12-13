# coding: utf8

import json
with open('preposicoes_detalhes_limpos.json', 'r', encoding='utf-8-sig') as openfile:
    prepositions = json.load(openfile)

    results = []
    for inner_preps in prepositions:
            results.append(inner_preps['uriAutores'])

    with open("lista_preposicoes_autores.json", "w", encoding='utf8') as outfile:
        json.dump(results, outfile, indent=4, ensure_ascii=False)