# coding: utf8

import asyncio
import aiohttp
import time
import json

# with open('input/lista_com_permanentes.json', 'r', encoding='utf-8-sig') as openfile:
with open('input/lista_dos_grupos_sem_membros.json', 'r', encoding='utf-8-sig') as openfile:
    grupos = json.load(openfile)


async def gather_with_concurrency(n, *tasks):
    semaphore = asyncio.Semaphore(n)

    async def sem_task(task):
        async with semaphore:
            return await task

    return await asyncio.gather(*(sem_task(task) for task in tasks))


async def get_async(input_data, session, results):
    base_url = f"https://dadosabertos.camara.leg.br/api/v2/orgaos/{input_data}/membros?dataInicio=2023-01-01&itens=1000"
    try:
        async with session.get(base_url) as response:
            if response.status == 200:
                deputy_detail = json.loads(await response.text())
                deputy_data = deputy_detail['dados']

                if len(deputy_detail['links']) == 4:
                    second_url = deputy_detail['links'][1]['href']
                    async with session.get(second_url) as response2:
                        if response2.status == 200:
                            deputy_data.extend(json.loads(await response2.text())['dados'])

                deputies_info = [
                    {
                        "id": d['id'],
                        "idLegislatura": d['idLegislatura'],
                        "dataFim": d['dataFim'],
                        "dataInicio": d['dataInicio'],
                        "codTitulo": d['codTitulo'],
                        "titulo": d['titulo']
                    }
                    for d in deputy_data if d['idLegislatura'] == 57
                ]

                results.append({
                    "groupId": input_data,
                    "deputies": deputies_info
                })

    except Exception as e:
        print(f"Error with {input_data}: {e}")

async def main():
    conn = aiohttp.TCPConnector(limit=1, ttl_dns_cache=300, ssl=False)
    session = aiohttp.ClientSession(connector=conn, headers={"Content-Type": "application/json"})
    results = []

    conc_req = 50
    now = time.time()
    await gather_with_concurrency(conc_req, *[get_async(i, session, results) for i in grupos])
    time_taken = time.time() - now

    print(time_taken)
    await session.close()

    # with open("output/detalhes_membros_grupos_com_perm.json", "w", encoding='utf8') as outfile:
    with open("output/grupos_restantes.json", "w", encoding='utf8') as outfile:
        json.dump(results, outfile, indent=4, ensure_ascii=False)


asyncio.run(main())
