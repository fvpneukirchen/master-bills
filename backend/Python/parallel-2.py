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
        oJson = json.loads(obj)
        del oJson["dados"]["status"]
        results[str(response.status)].append(oJson["dados"])


async def main():
    f = open("out-deput-3.txt", "a")

    conn = aiohttp.TCPConnector(limit=None, ttl_dns_cache=300, verify_ssl=False)
    session = aiohttp.ClientSession(connector=conn, headers={"Content-Type": "application/json"})
    results = {
        "200": [],
        "500": []
    }

    urls = [
        "https://dadosabertos.camara.leg.br/api/v2/partidos/37906",
        "https://dadosabertos.camara.leg.br/api/v2/partidos/36837",
        "https://dadosabertos.camara.leg.br/api/v2/partidos/36763",
        "https://dadosabertos.camara.leg.br/api/v2/partidos/36835",
        "https://dadosabertos.camara.leg.br/api/v2/partidos/37901",
        "https://dadosabertos.camara.leg.br/api/v2/partidos/37903",
        "https://dadosabertos.camara.leg.br/api/v2/partidos/36844",
        "https://dadosabertos.camara.leg.br/api/v2/partidos/36769",
        "https://dadosabertos.camara.leg.br/api/v2/partidos/37907",
        "https://dadosabertos.camara.leg.br/api/v2/partidos/36832",
        "https://dadosabertos.camara.leg.br/api/v2/partidos/37905",
        "https://dadosabertos.camara.leg.br/api/v2/partidos/36779",
        "https://dadosabertos.camara.leg.br/api/v2/partidos/37908",
        "https://dadosabertos.camara.leg.br/api/v2/partidos/36833",
        "https://dadosabertos.camara.leg.br/api/v2/partidos/36898",
        "https://dadosabertos.camara.leg.br/api/v2/partidos/37904",
        "https://dadosabertos.camara.leg.br/api/v2/partidos/36839",
        "https://dadosabertos.camara.leg.br/api/v2/partidos/36896",
        "https://dadosabertos.camara.leg.br/api/v2/partidos/36851",
        "https://dadosabertos.camara.leg.br/api/v2/partidos/36845",
        "https://dadosabertos.camara.leg.br/api/v2/partidos/36886"
    ]

    conc_req = 5
    now = time.time()
    await gather_with_concurrency(conc_req, *[get_async(i, session, results) for i in urls])
    time_taken = time.time() - now

    print(time_taken)
    await session.close()

    r = str(results).replace("\\\\", "\\").replace("'{", "{").replace("}'", "}\n")

    f.write(r)
    f.close()


asyncio.run(main())
