import asyncio
import aiohttp
import time
import json


async def gather_with_concurrency(n, *tasks):
    semaphore = asyncio.Semaphore(n)

    async def sem_task(task):
        async with semaphore:
            return await task

    return await asyncio.gather(*(sem_task(task) for task in tasks))


async def get_async(url, session, results):
    async with session.get(url) as response:
        obj = await response.text()
        o_json = json.loads(obj)

        if response.status == 200:
            for pl_json in o_json["dados"]:
                results[str(response.status)].append(pl_json)


async def main():
    f = open("out-parallel-3.txt", "a")

    conn = aiohttp.TCPConnector(limit=None, ttl_dns_cache=300, verify_ssl=False)
    session = aiohttp.ClientSession(connector=conn, headers={"Content-Type": "application/json"})
    results = {
        "200": [],
        "400": [],
        "500": []
    }

    urls = []

    for page in range(41):
        url = "https://dadosabertos.camara.leg.br/api/v2/proposicoes?" \
              "siglaTipo=PL&ano=2021&pagina={page}&itens=100&ordem=ASC&ordenarPor=id"

        print("Calling page " + str(page))

        urls.append(url.format(page=page))

    conc_req = 10
    now = time.time()
    await gather_with_concurrency(conc_req, *[get_async(i, session, results) for i in urls])
    time_taken = time.time() - now

    print(time_taken)
    await session.close()

    r = str(results).replace("\\\\", "\\").replace("'{", "{").replace("}'", "}\n")

    f.write(r)
    f.close()


asyncio.run(main())
