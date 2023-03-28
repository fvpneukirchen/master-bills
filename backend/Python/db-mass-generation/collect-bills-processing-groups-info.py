# -*- coding: utf-8 -*-


import asyncio
import json
import time

import aiohttp
from itertools import groupby
from operator import itemgetter


pls = ['538737', '180', '5503', '5973', '2012', '538408', '100293', '4', '538344', '2016', '100050', '100303', '2003',
       '100046', '2015', '2008', '538460', '538963', '186', '2010', '6174', '102328', '2007', '6309', '536996', '2018',
       '537480', '538763', '100229', '2004', '6066', '537236', '2002', '2017', '2001', '2006', '537870', '2014',
       '539057', '537871', '100001', '2009']


async def gather_with_concurrency(n, *tasks):
    semaphore = asyncio.Semaphore(n)

    async def sem_task(task):
        async with semaphore:
            return await task

    return await asyncio.gather(*(sem_task(task) for task in tasks))


async def get_async(url, session, results):
    try:
        async with session.get(url) as response:
            obj = await response.text()
            o_json = json.loads(obj)
            # "uriOrgao": "https://dadosabertos.camara.leg.br/api/v2/orgaos/4",
            # results.append(str(dado["uriOrgao"]).replace("https://dadosabertos.camara.leg.br/api/v2/orgaos/", ""))
            results.append(o_json["dados"])
    except Exception:
        print("url  " + url)


async def main():
    conn = aiohttp.TCPConnector(limit=0, ttl_dns_cache=500, verify_ssl=False)
    session = aiohttp.ClientSession(connector=conn, headers={"Content-Type": "application/json"})
    results = []
    urls = []

    for pl in pls:
        id_str = str(pl)

        url = "https://dadosabertos.camara.leg.br/api/v2/orgaos/{pl_id}"

        url_formatted = url.format(pl_id=id_str)
        print("Calling url " + url_formatted)

        urls.append(url_formatted)

    conc_req = 30
    now = time.time()
    await gather_with_concurrency(conc_req, *[get_async(i, session, results) for i in urls])
    time_taken = time.time() - now

    print(time_taken)
    await session.close()

    # results_grouped = dict((k, list(g)) for k, g in groupby(results, key=itemgetter('codTipoOrgao')))
    # for k, v in groupby(results, key=lambda x: x['codTipoOrgao']):
    #     results_grouped.append(
    #         {
    #             'key': k,
    #             'value': list(v)
    #         }
    #     )

    res = {}
    for item in results:
        res.setdefault(item['codTipoOrgao'], []).append(item)

    with open('bills-group-info.json', 'w') as outfile:
        json.dump(res, outfile, indent=4, ensure_ascii=False)


asyncio.run(main())
