# coding: utf8

import asyncio
import aiohttp
import time
import json

def capitalize_first_character(string):
    return string[0].upper() + string[1:]

with open('partidos_detalhes.json', 'r', encoding='utf-8-sig') as openfile:
    parties = json.load(openfile)

    results = []
    for p in parties:
        # Extract the "lider" attribute
        # lider_data = p["dados"]["status"]["lider"]

        # Add "lider_" as a prefix to lider_data keys
        # prefixed_lider_data = {"lider" + capitalize_first_character(key): value for key, value in lider_data.items()}

        # Remove the "lider" attribute from the original hierarchy
        del p["dados"]["status"]["lider"]

        status_data = p["dados"]["status"]

        del p["dados"]["status"]

        # Add the prefixed lider_data back to the top level of the hierarchy
        # p['dados'].update(prefixed_lider_data)
        p['dados'].update(status_data)

        results.append(p)

    with open("partidos_detalhes_limpos.json", "w", encoding='utf8') as outfile:
        json.dump(results, outfile, indent=4, ensure_ascii=False)