# coding: utf8

import asyncio
import aiohttp
import time
import json


with open('output/lista_preposicoes_3.json', 'r', encoding='utf-8-sig') as openfile:
    prepositions = json.load(openfile)

async def gather_with_concurrency(n, *tasks):
    semaphore = asyncio.Semaphore(n)

    async def sem_task(task):
        async with semaphore:
            return await task

    return await asyncio.gather(*(sem_task(task) for task in tasks))


async def get_async(input_data, session, results):
    try:
        async with session.get(input_data) as response:
            obj = await response.text()
            party_details = json.loads(obj)
            del party_details['links']
            if response.status == 200:
                results["200"].append(party_details)

    except Exception:
        results["500"].append(input_data)
        print("url  " + input_data)


async def main():
    conn = aiohttp.TCPConnector(ttl_dns_cache=300, ssl=False)
    session = aiohttp.ClientSession(connector=conn, headers={"Content-Type": "application/json"})
    results = {
        "200": [],
        "500": []
    }

    conc_req = 5
    now = time.time()
    await gather_with_concurrency(conc_req, *[get_async(i, session, results) for i in prepositions["500"]])
    time_taken = time.time() - now

    print(time_taken)
    await session.close()

    with open("output/lista_preposicoes_4.json", "w", encoding='utf8') as outfile:
        json.dump(results, outfile, indent=4, ensure_ascii=False)


asyncio.run(main())
