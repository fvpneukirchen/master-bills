import asyncio
import aiohttp
import time
import json
from itertools import islice

with open('pls-2021.json', 'r', encoding="utf8") as data_file:
    json_data = data_file.read()

pls = json.loads(json_data)


def chunks(data, SIZE=10000):
    it = iter(data)
    for i in range(0, len(data), SIZE):
        yield {k: data[k] for k in islice(it, SIZE)}


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
    async with session.get(url[1]) as response:
        obj = await response.text()
        o_json = json.loads(obj)

        new_dict = {url[0]: o_json["dados"]}
        results[str(response.status)].append(new_dict)


async def main():
    f1 = open("pls-and-themes-1.json", "w", encoding='utf8')
    f2 = open("pls-and-themes-2.json", "w", encoding='utf8')
    f3 = open("pls-and-themes-3.json", "w", encoding='utf8')
    f4 = open("pls-and-themes-4.json", "w", encoding='utf8')
    f5 = open("pls-and-themes-5.json", "w", encoding='utf8')

    conn = aiohttp.TCPConnector(limit=None, ttl_dns_cache=300, verify_ssl=False)
    session = aiohttp.ClientSession(connector=conn, headers={"Content-Type": "application/json"})
    results = {'200': []}
    urls = []

    for pl in pls["dados"]:
        id_str = str(pl["id"])
        print("Calling referenceNumber " + id_str)

        url = "https://dadosabertos.camara.leg.br/api/v2//proposicoes/{id_param}/temas"

        url_formatted = url.format(id_param=id_str)
        print("Calling referenceNumber " + url_formatted)

        urls.append([id_str, url_formatted])

    conc_req = 30
    now = time.time()
    await gather_with_concurrency(conc_req, *[get_async(i, session, results) for i in urls])
    time_taken = time.time() - now

    print(time_taken)
    await session.close()

    s = list(split(results['200'], 5))
    # s = split(results.items(), 5)

    json.dump(s[0], f1, ensure_ascii=False, indent=4)
    json.dump(s[1], f2, ensure_ascii=False, indent=4)
    json.dump(s[2], f3, ensure_ascii=False, indent=4)
    json.dump(s[3], f4, ensure_ascii=False, indent=4)
    json.dump(s[4], f5, ensure_ascii=False, indent=4)

    f1.close()
    f2.close()
    f3.close()
    f4.close()
    f5.close()


asyncio.run(main())
