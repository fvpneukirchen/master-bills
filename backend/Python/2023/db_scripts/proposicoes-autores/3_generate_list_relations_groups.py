# coding: utf8

import asyncio
import aiohttp
import time
import json

with open('output/split_preposicoes_autores_grupos_2.json', 'r', encoding='utf-8-sig') as openfile:
    autores = json.load(openfile)


async def main():
    deps = []
    for a in autores:
        if a['autor']['uri'] != None and a['autor']['uri'] != '':
            prep = (a['prep']
                    .replace("https://dadosabertos.camara.leg.br/api/v2/proposicoes/", "")
                    .replace("/autores", ""))
            author = a['autor']['uri'].replace("https://dadosabertos.camara.leg.br/api/v2/orgaos/", "")
            uri = a['autor']['uri']
            nome = a['autor']['nome']
            codTipo = a['autor']['codTipo']
            tipo = a['autor']['tipo']
            ordemAssinatura = a['autor']['ordemAssinatura']
            proponente = a['autor']['proponente']
            print(prep, author, uri, nome, codTipo, tipo, ordemAssinatura, proponente)
            match = ('MATCH (d:Groups {0}{1}{2}), (p:Prepositions {3}{4}{5}) '
                     'MERGE (d)'
                     '-[:AUTHORED '
                     '{6}uri: \'{7}\', '
                     'nome:  \"{8}\", '
                     'codTipo:  \'{9}\', '
                     'tipo:  \'{10}\', '
                     'ordemAssinatura:  \'{11}\', '
                     'proponente:  \'{12}\', '
                     'prepId:  \'{13}\', '
                     'autorId:  \'{14}\''
                     '{15}'
                     ']'
                     '->(p)').format("{","id: " + author,"}", "{", "id: " + prep,"}", "{", uri, nome,
                                     codTipo, tipo, ordemAssinatura,
                                     proponente, prep, author,"}")
            deps.append(match)

    with open("output/relations_groups_2.json", "w", encoding='utf8') as outfile:
        json.dump(deps, outfile, indent=4, ensure_ascii=False)


asyncio.run(main())
