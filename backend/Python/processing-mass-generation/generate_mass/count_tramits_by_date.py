# coding: utf8
import asyncio
import json
from operator import itemgetter
from datetime import datetime
import pandas as pd

import itertools


async def main():
    with open('tramit_all_filter.json', 'r', encoding='utf8') as openfile:
        json_object = json.load(openfile)

        r = []
        for p in json_object:
            for e in p['data']:
                e['processing'] = p['processing']
            r.append(p['data'])

        r = list(itertools.chain(*r))
        r = sorted(r, key=itemgetter('dataHora'))
        r = [dict(t) for t in {tuple(d.items()) for d in r}]
        # r = [e['dataHora'][0:10] for e in r]
        r = [{'t': e['codTipoTramitacao'], 'u': e['uriOrgao'], 'e': e['processing']} for e in r]

        with open('out.json', "w", encoding='utf8') as outfile:
            json.dump(r, outfile, indent=4, ensure_ascii=False)
        #
        # counts = pd.Series(r).value_counts()
        #
        # print(counts)

        # for p in json_object:
        #     r.append()


asyncio.run(main())
