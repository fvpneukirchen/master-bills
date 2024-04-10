# coding: utf8

import json
with open('../proposicoes/output/preposicoes_detalhes_limpos_2.json', 'r', encoding='utf-8-sig') as openfile:
    prepositions = json.load(openfile)

    results = []
    for prep in prepositions["200"]:
        results.append('https://dadosabertos.camara.leg.br/api/v2/proposicoes/{0}/temas'.format(prep['id']))

    with open("output/lista_preposicoes_temas_urls_2.json", "w", encoding='utf8') as outfile:
        json.dump(results, outfile, indent=4, ensure_ascii=False)