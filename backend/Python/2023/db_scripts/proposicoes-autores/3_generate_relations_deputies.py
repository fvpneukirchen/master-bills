# coding: utf8

import asyncio
import aiohttp
import time
import json

with open('output/preposicoes_autores_detalhes.json', 'r', encoding='utf-8-sig') as openfile:
    autores = json.load(openfile)


async def main():

    deps = []
    groups = []
    for a in autores:
        for d in a['data']:
            if "orgaos" in d['uri']:
                groups.append({"prep": a['url'], "autor": d})
            else:
                deps.append({"prep": a['url'], "autor": d})



    with open("output/split_preposicoes_autores_deputados.json", "w", encoding='utf8') as outfile:
        json.dump(deps, outfile, indent=4, ensure_ascii=False)

    with open("output/split_preposicoes_autores_grupos.json", "w", encoding='utf8') as outfile:
        json.dump(groups, outfile, indent=4, ensure_ascii=False)


asyncio.run(main())
