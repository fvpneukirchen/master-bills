# coding: utf8
import asyncio
import json
from operator import itemgetter
from datetime import datetime
import time
import itertools

import aiohttp

file_name = 'tramit_all'

in_file_name = str(file_name) + ".json"
out_file_name = str(file_name) + "_filter.json"
steps_out_file_name = str(file_name) + "_steps.json"
parent_out_file_name = str(file_name) + "_steps_parents.json"
parent_out_file_name3 = str(file_name) + "_3_steps_parents.json"


async def gather_with_concurrency(n, *tasks):
    semaphore = asyncio.Semaphore(n)

    async def sem_task(task):
        async with semaphore:
            return await task

    return await asyncio.gather(*(sem_task(task) for task in tasks))


async def get_async(input_data, session, results):
    # url = str(input_data['u'])
    # print("Calling page " + str(input_data))
    obj = None
    try:
        async with session.get(input_data) as response:
            obj = await response.text()

            o_json = json.loads(str(obj))

            # input_data['p'] = o_json["dados"]
            # results['p'].append({'c': o_json['dados']["codTipoOrgao"], 't': o_json['dados']["tipoOrgao"]})

            if response.status == 200:
                results['p'].append({'c': o_json['dados']["codTipoOrgao"], 't': o_json['dados']["tipoOrgao"]})
                # results['c'].append(input_data)
                time.sleep(0.3)
    except:
        print(input_data)
        print(obj)
        print('\n')


async def main():
    with open(in_file_name, 'r', encoding='utf8') as openfile:
        json_object = json.load(openfile)

        r = []
        for p in json_object:
            processing = [e for e in p['data'] if e["ambito"] != "Protocolar"]
            processing = [e for e in processing if datetime.strptime(e['dataHora'], '%Y-%m-%dT%H:%M').year == 2021]
            processing = [e for e in processing if e["sequencia"] is not None]
            # processing = [e for e in processing if e["siglaOrgao"] == "MESA"]
            processing = sorted(processing, key=itemgetter('sequencia'))
            p['data'] = processing
            r.append([{
                'd': e['descricaoTramitacao'],
                'c': int(e['codTipoTramitacao']),
                's': e['siglaOrgao'],
                'u': e['uriOrgao']
            } for e in processing])

        with open(out_file_name, "w", encoding='utf8') as outfile:
            json.dump(json_object, outfile, indent=4, ensure_ascii=False)

        r = list(itertools.chain(*r))
        r = [dict(t) for t in {tuple(d.items()) for d in r}]
        r = sorted(r, key=itemgetter('s'))
        t = []
        for i, j in itertools.groupby(r, key=itemgetter('s')):
            z = list(j)
            t.append(
                {'s': i, 'u': z[0]['u'],
                 'v': sorted([{'d': w['d'], 'c': w['c'], 'u': w['u']} for w in z], key=itemgetter('c'))})

        r = t
        urls = [ut['u'] for ut in t]
        # with open(parent_out_file_name, "r", encoding='utf8') as op:
        #     all_s = json.load(op)
        #
        # for item in r:
        #     match = None
        #     for item_s in all_s['c']:
        #         if item['s'] == item_s['s']:
        #             match = item_s
        #             break
        #     if match is not None:
        #         item['p'] = item_s['p']
        #         # with open(steps_out_file_name, "w", encoding='utf8') as outfile:
        # #     json.dump(r, outfile, indent=4, ensure_ascii=False)

        conn = aiohttp.TCPConnector(ttl_dns_cache=300, ssl=False)
        session = aiohttp.ClientSession(connector=conn, headers={"Content-Type": "application/json"})

        results = {
            'c': [],
            'p': []
        }

        conc_req = 2
        now = time.time()
        await gather_with_concurrency(conc_req, *[get_async(i, session, results) for i in urls])
        time_taken = time.time() - now

        print(time_taken)
        await session.close()

        results['p'] = [dict(t) for t in {tuple(d.items()) for d in results['p']}]
        results['c'] = r

        with open(parent_out_file_name3, "w", encoding='utf8') as outfile:
            json.dump(results, outfile, indent=4, ensure_ascii=False)


asyncio.run(main())
