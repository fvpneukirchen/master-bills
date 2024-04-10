import asyncio
import aiohttp
import time
import json

# Load URLs from your JSON file
with open('output/lista_preposicoes_autores_2.json', 'r', encoding='utf-8-sig') as openfile:
    urls = json.load(openfile)


async def gather_with_concurrency(n, *tasks):
    semaphore = asyncio.Semaphore(n)

    async def sem_task(task):
        async with semaphore:
            return await task

    return await asyncio.gather(*(sem_task(task) for task in tasks))


async def get_async(input_data, session, results, max_retries=3, delay=2):
    retries = 0
    while retries <= max_retries:
        try:
            len_r = results["200"].__len__()
            print(f"Results size {len_r}")
            async with session.get(input_data) as response:
                if response.status == 200:
                    obj = await response.text()
                    prep_details = json.loads(obj)
                    del prep_details['links']
                    prep_details_data = prep_details['dados']
                    results["200"].append({
                        "url": input_data,
                        "data": prep_details_data
                    })
                    break  # Break the loop on success
                else:
                    print(f"Retry {retries + 1}/{max_retries} for URL: {input_data} due to status {response.status}")
        except Exception as e:
            print(f"Exception on {input_data}: {str(e)} -- retry {retries + 1}/{max_retries}")
            retries += 1
            await asyncio.sleep(delay)

    if retries > max_retries:
        print(f"Failed to process {input_data} after {max_retries} retries.")
        results["500"].append(input_data)


async def main():
    conn = aiohttp.TCPConnector(limit=1, ttl_dns_cache=300, ssl=False)
    session = aiohttp.ClientSession(connector=conn, headers={"Content-Type": "application/json"})
    results = {
        "200": [],
        "500": []
    }

    conc_req = 50
    now = time.time()
    await gather_with_concurrency(conc_req, *[get_async(i, session, results) for i in urls])
    time_taken = time.time() - now

    print(f"Total time taken: {time_taken} seconds")
    await session.close()

    with open("output/preposicoes_autores_detalhes_2.json", "w", encoding='utf8') as outfile:
        json.dump(results, outfile, indent=4, ensure_ascii=False)


asyncio.run(main())
