# coding: utf8
import asyncio
import json

with open('temaDasPl.json', 'r', encoding='utf-8-sig') as openfile:
    themes = json.load(openfile)

with open('idPlsPorAutorComSilgaPartido.json', 'r', encoding='utf-8-sig') as openfile:
    authors = json.load(openfile)


async def main():
    with open('reduce_filtered.json', 'r', encoding='utf8') as openfiler:
        bills = json.load(openfiler)
    result = []
    for b in bills:

        bt = []
        for t in themes:
            if b['processing'] == str(t['b.id']):
                bt.append(t['t.cod'])
        ba = []
        for a in authors:
            if b['processing'] == str(a['b.id']):
                ba.append(a['d.id'])

        result.append({
            "b": b['processing'],
            "c": b['data'],
            "r": b['r'],
            "t": bt,
            "a": ba
        })

    with open('aggregation.json', "w", encoding='utf8') as outfile:
        json.dump(result, outfile, indent=4, ensure_ascii=False)


asyncio.run(main())
