# coding: utf8

import asyncio
import aiohttp
import time
import json

with open('deputados_detalhes.json', 'r', encoding='utf-8-sig') as openfile:
    deputies = json.load(openfile)

    results = []
    for d in deputies:
        del d['links']

        # Move attributes from "ultimoStatus" to the top level
        ultimo_status = d['dados']['ultimoStatus']
        del d['dados']['ultimoStatus']

        if 'gabinete' in ultimo_status:
            del ultimo_status['gabinete']

        d['dados'].update(ultimo_status)

        results.append(d)

    with open("deputados_detalhes_limpos.json", "w", encoding='utf8') as outfile:
        json.dump(results, outfile, indent=4, ensure_ascii=False)