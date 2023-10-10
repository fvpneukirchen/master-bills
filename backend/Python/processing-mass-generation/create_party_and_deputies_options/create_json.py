# coding: utf8
import asyncio
import json


async def main():
    # with open('../../nodes_creation/deputies.json', 'r', encoding='utf8') as openfile:
    with open('output.json', 'r', encoding='utf8') as openfile:
        deputies = json.load(openfile)

        # # Cria um dicionário para agrupar os deputados por partido
        # partidos = {}
        # for deputado in deputies:
        #     sigla_partido = deputado['siglaPartido']
        #     if sigla_partido not in partidos:
        #         partidos[sigla_partido] = {
        #             'label': sigla_partido,
        #             'options': []
        #         }
        #     partidos[sigla_partido]['options'].append({
        #         'label': deputado['nome'],
        #         'value': str(deputado['id'])
        #     })

        # out = []
        # for d in deputies:
        #     out.append({"label": d['label'], "value": d['label']})

        for element in deputies:
            for option in element["options"]:
                option["party"] = element["label"]

        # with open('output.json', "w", encoding='utf8') as outfile:
        with open('output4.json', "w", encoding='utf8') as outfile:
            json.dump(deputies, outfile, indent=4, ensure_ascii=False)
            # json.dump(partidos, outfile, indent=4, ensure_ascii=False)


asyncio.run(main())
