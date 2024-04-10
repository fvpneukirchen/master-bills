# coding: utf8

import asyncio
import aiohttp
import time
import json

with open('output/preposicoes_temas_detalhes_2.json', 'r', encoding='utf-8-sig') as openfile:
    preps = json.load(openfile)


async def main():
    preps_themes = []
    for a in preps["200"]:
        if a['data'] != None and a['data'] != '' and a['data'] != []:
            prep = (a['url']
                    .replace("https://dadosabertos.camara.leg.br/api/v2/proposicoes/", "")
                    .replace("/temas", ""))
            for theme in a['data']:
                codTema = theme['codTema']
                tema = theme['tema']
                relevancia = theme['relevancia']
                print(prep, theme, codTema, tema, relevancia, a['url'])
                match = ('MATCH (d:Prepositions {0}{1}{2}), (p:Themes {3}{4}{5}) '
                         'MERGE (d)'
                         '-[:HAS_THEME '
                         '{6}url: \'{7}\', '
                         'codTema:  \'{8}\', '
                         'tema:  \'{9}\', '
                         'relevancia:  \'{10}\''
                         '{11}'
                         ']'
                         '->(p)').format("{", "id: " + prep, "}",
                                         "{", "cod: \'" + str(codTema), "\'}",
                                         "{", a['url'], codTema, tema, relevancia, "}")
                preps_themes.append(match)

    with open("output/relations_preps_themes_2.json", "w", encoding='utf8') as outfile:
        json.dump(preps_themes, outfile, indent=4, ensure_ascii=False)


asyncio.run(main())
