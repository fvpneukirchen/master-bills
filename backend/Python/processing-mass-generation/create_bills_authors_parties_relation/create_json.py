# coding: utf8
import asyncio
import json


async def main():
    with open('../generate_mass/preps_autores.json', 'r', encoding='utf8') as openfile:
        items = json.load(openfile)

        with open('../../nodes_creation/deputies.json', 'r', encoding='utf8') as openfile2:
            deputies = json.load(openfile2)

            out = []
            for d in items:
                out.append({"i": d['processing'], "a": [x['uri'] for x in d['data']]})

            out2 = []
            for o in out:

                t = set()
                for a in o['a']:
                    for d in deputies:
                        if str(d['id']) == a:
                            t.add(d['siglaPartido'])
                            break

                out2.append({"i": o['i'], "a": o['a'], "t": list(t)})

        with open('output2.json', "w", encoding='utf8') as outfile:
            json.dump(out2, outfile, indent=4, ensure_ascii=False)


asyncio.run(main())
