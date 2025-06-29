# coding: utf8

import asyncio
import aiohttp
import time
import json

# with open('input/lista_unica_grupos.json', 'r', encoding='utf-8-sig') as openfile:
# with open('input/lista_com_permanentes.json', 'r', encoding='utf-8-sig') as openfile:
with open('input/grupos_que_faltaram.json', 'r', encoding='utf-8-sig') as openfile:
    grupos = json.load(openfile)


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

    for d in grupos:
        urls.append("https://dadosabertos.camara.leg.br/api/v2/orgaos/" + str(d))

    conc_req = 50
    now = time.time()
    await gather_with_concurrency(conc_req, *[get_async(i, session, results) for i in urls])
    time_taken = time.time() - now

    print(time_taken)
    await session.close()

    # with open("output/detalhes_grupos_com_perm.json", "w", encoding='utf8') as outfile:
    with open("output/detalhes_grupos_que_faltaram.json", "w", encoding='utf8') as outfile:
        json.dump(results, outfile, indent=4, ensure_ascii=False)


asyncio.run(main())
