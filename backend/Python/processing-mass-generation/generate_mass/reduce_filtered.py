# coding: utf8
import asyncio
import json


async def main():
    with open('tramit_all_filter.json', 'r', encoding='utf8') as openfile:
        json_object = json.load(openfile)

        for p in json_object:
            i = 0
            for d in p['data']:
                if "Ordinário" in d['regime']:
                    p['r'] = 'O'
                else:
                    if "Prioridade" in d['regime']:
                        p['r'] = 'P'
                    else:
                        p['r'] = d['regime']

                p['data'][i] = {
                    'd': d['dataHora'],
                    'i': d['sequencia'],
                    'o': d['uriOrgao'].rsplit('/', 1)[-1],
                    't': d['codTipoTramitacao'],
                    's': d['codSituacao'],
                }
                i = i + 1

        with open('reduce_filtered.json', "w", encoding='utf8') as outfile:
            json.dump(json_object, outfile, indent=4, ensure_ascii=False)


asyncio.run(main())
