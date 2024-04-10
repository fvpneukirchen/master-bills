# coding: utf8

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


async def get_async(input_data, session, results, max_retries=5, retry_delay=2):
    retries = 0
    while retries < max_retries:
        try:
            async with session.get(input_data) as response:
                if response.status == 200:
                    obj = await response.text()
                    party_details = json.loads(obj)
                    del party_details['links']
                    results["200"].append(party_details)
                    break  # Successfully got response, break the retry loop
                else:
                    raise Exception(f"Received {response.status} response")
        except Exception as e:
            print(f"Retry {retries + 1} for URL: {input_data}, Error: {e}")
            retries += 1
            await asyncio.sleep(retry_delay)  # Delay before retrying

    if retries == max_retries:
        print(f"Failed to fetch {input_data} after {max_retries} attempts.")
        results["500"].append(input_data)


async def main():
    conn = aiohttp.TCPConnector(ttl_dns_cache=300, ssl=False)
    session = aiohttp.ClientSession(connector=conn, headers={"Content-Type": "application/json"})
    results = {
        "200": [],
        "500": []
    }

    urls = []

    page_range = range(1, 762)
    for i in page_range:
        url = f"https://dadosabertos.camara.leg.br/api/v2/proposicoes?dataInicio=2023-02-01&dataFim=2023-12-31&ordem=ASC&ordenarPor=id&pagina={i}&itens=100"
        urls.append(url)

    conc_req = 50
    now = time.time()
    await gather_with_concurrency(conc_req, *[get_async(url, session, results) for url in urls])
    time_taken = time.time() - now

    print(f"Time taken: {time_taken} seconds")
    await session.close()

    with open("output/lista_preposicoes_2.json", "w", encoding='utf8') as outfile:
        json.dump(results, outfile, indent=4, ensure_ascii=False)


asyncio.run(main())
