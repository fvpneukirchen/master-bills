import json

with open('output/lista_preposicoes.json', 'r', encoding='utf-8-sig') as openfile:
    urls = json.load(openfile)

# Função para contar as ocorrências por siglaTipo
def contar_ocorrencias_por_sigla_tipo(lista_de_objetos):
    contagem = {}

    for objeto in lista_de_objetos:
        for item in objeto["dados"]:
            sigla_tipo = item["siglaTipo"]
            contagem[sigla_tipo] = contagem.get(sigla_tipo, 0) + 1

    return contagem

resultado = contar_ocorrencias_por_sigla_tipo(urls)
resultado_ordenado = dict(sorted(resultado.items(), key=lambda item: item[1], reverse=True))


print(resultado_ordenado)
