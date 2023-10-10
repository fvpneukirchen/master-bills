# coding: utf-8-sig
import asyncio
import json

def flatten_array(arr):
    flattened = []
    for i in arr:
        if type(i) == list:
            flattened += flatten_array(i)
        else:
            flattened.append(i)
    return flattened
async def main():
    with open('temaDasPl.json', 'r', encoding='utf-8-sig') as openfile:
        pls_and_thmes = json.load(openfile)

        with open('output2.json', 'r', encoding='utf-8-sig') as openfile2:
            p_a = json.load(openfile2)

            ids = set()
            for element in pls_and_thmes:
                ids.add(element["id"])

            out = []
            for idi in list(ids):
                out.append({"id": str(idi), "c": [], "t": [], "a": flatten_array([p['a'] for p in p_a if p['i'] == str(idi)]), "p": flatten_array([p['t'] for p in p_a if p['i'] == str(idi)])})

            for element in pls_and_thmes:
                for o in out:
                    if o['id'] == str(element['id']):
                        o['c'].append(element['value'])
                        o['t'].append(element['label'])
                # for p in p_a:
                #     if p['i'] == str(element['id']):
                #         o['t'] = p['t']
                #         o['a'] = p['a']

            with open('output.json', "w", encoding='utf-8-sig') as outfile:
                json.dump(out, outfile, indent=4, ensure_ascii=False)


asyncio.run(main())
