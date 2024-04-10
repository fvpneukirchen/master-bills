# coding: utf8

import asyncio
import aiohttp
import time
import json

with open('output/split_preposicoes_autores_grupos.json', 'r', encoding='utf-8-sig') as openfile:
    autores = json.load(openfile)


async def main():

    groups = []
    for a in autores:
        if a['autor']['codTipo'] == 30000 or a['autor']['codTipo'] == 40000:
            groups.append(a)



    with open("output/split_autores_grupos_filtrados_codTipo.json", "w", encoding='utf8') as outfile:
        json.dump(groups, outfile, indent=4, ensure_ascii=False)

asyncio.run(main())
