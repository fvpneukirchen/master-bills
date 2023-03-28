# coding: utf8

import asyncio
import aiohttp
import time
import json

with open('preps.json', 'r', encoding='utf-8-sig') as openfile:
    json_object = json.load(openfile)


async def gather_with_concurrency(n, *tasks):
    semaphore = asyncio.Semaphore(n)

    async def sem_task(task):
        async with semaphore:
            return await task

    return await asyncio.gather(*(sem_task(task) for task in tasks))


async def get_async(input_data, session, results):
    p_id = str(input_data[1])

    url = input_data[0].format(tramit_id=p_id)

    print("Calling page " + str(url))

    async with session.get(url) as response:
        obj = await response.text()
        o_json = json.loads(obj)

        if response.status == 200:
            results.append({
                'processing': p_id,
                'data': o_json["dados"]
            })


async def main():
    conn = aiohttp.TCPConnector(ttl_dns_cache=300, ssl=False)
    session = aiohttp.ClientSession(connector=conn, headers={"Content-Type": "application/json"})
    results = []

    urls = []

    for processing in json_object:
        urls.append(["https://dadosabertos.camara.leg.br/api/v2/proposicoes/{tramit_id}/tramitacoes", processing])

    conc_req = 5
    now = time.time()
    await gather_with_concurrency(conc_req, *[get_async(i, session, results) for i in urls])
    time_taken = time.time() - now

    print(time_taken)
    await session.close()

    with open("../generate_mass/tramit_all.json", "w", encoding='utf8') as outfile:
        json.dump(results, outfile, indent=4, ensure_ascii=False)


asyncio.run(main())
