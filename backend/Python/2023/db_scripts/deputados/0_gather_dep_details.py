# coding: utf8

import asyncio
import aiohttp
import time
import json

with open('input/deputados_legis_57.json', 'r', encoding='utf-8-sig') as openfile:
    deputies = json.load(openfile)


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
            deputy_detail = json.loads(obj)

            if response.status == 200:
                results.append(deputy_detail)

    except Exception:
        print("url  " + input_data)


async def main():
    conn = aiohttp.TCPConnector(limit=1, ttl_dns_cache=300, ssl=False)
    session = aiohttp.ClientSession(connector=conn, headers={"Content-Type": "application/json"})
    results = []

    urls = []

    for d in deputies:
        urls.append(d["uri"])

    conc_req = 50
    now = time.time()
    await gather_with_concurrency(conc_req, *[get_async(i, session, results) for i in urls])
    time_taken = time.time() - now

    print(time_taken)
    await session.close()

    with open("output/deputados_detalhes.json", "w", encoding='utf8') as outfile:
        json.dump(results, outfile, indent=4, ensure_ascii=False)


asyncio.run(main())
