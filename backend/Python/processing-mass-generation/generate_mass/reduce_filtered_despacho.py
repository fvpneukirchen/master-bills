# coding: utf8
import asyncio
import json
import operator
from operator import itemgetter


async def main():
    with open('tramit_all_filter.json', 'r', encoding='utf8') as openfile:
        json_object = json.load(openfile)

        for p in json_object:
            i = 0

            try:
                sorted_list = sorted(p['data'], key=itemgetter('sequencia'))
            except Exception as e:
                print(e)
                print(p['data'])

            for d in sorted_list:
                p['data'][i] = {
                    'd': d['despacho'],
                    's': d['sequencia']
                }
                i = i + 1

        with open('reduce_filtered_despacho.json', "w", encoding='utf8') as outfile:
            json.dump(json_object, outfile, indent=4, ensure_ascii=False)


asyncio.run(main())
