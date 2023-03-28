import asyncio
import aiohttp
import time
import json

with open('pl-specific-4.json', 'r', encoding="utf8") as data_file:
    json_data = data_file.read()

pls = json.loads(json_data)


def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))


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
        results[str(response.status)].append(o_json)


async def main():
    f1 = open("pl-specific-authors-4.json", "w", encoding='utf8')

    conn = aiohttp.TCPConnector(limit=None, ttl_dns_cache=300, verify_ssl=False)
    session = aiohttp.ClientSession(connector=conn, headers={"Content-Type": "application/json"})
    results = {
        "200": [],
        "500": []
    }

    base_url = 'https://dadosabertos.camara.leg.br/api/v2/proposicoes/{pl_id}/autores'

    urls = []

    for pl in pls:
        print("Calling referenceNumber " + str(pl["id"]))

        urls.append(base_url.format(pl_id=str(pl["id"])))

    conc_req = 30
    now = time.time()
    await gather_with_concurrency(conc_req, *[get_async(i, session, results) for i in urls])
    time_taken = time.time() - now

    print(time_taken)
    await session.close()

    json.dump(results["200"], f1, ensure_ascii=False, indent=4)

    f1.close()


asyncio.run(main())
