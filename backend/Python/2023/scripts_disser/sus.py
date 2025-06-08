import json


def processar_respostas(arquivo_txt):
    # Lê todas as linhas do arquivo
    with open(arquivo_txt, 'r', encoding='utf-8') as file:
        linhas = file.readlines()

    # Remove espaços em branco e quebras de linha
    linhas = [linha.strip() for linha in linhas if linha.strip()]

    # Divide cada linha pelos tabs
    respostas_por_participante = [linha.split('\t') for linha in linhas]

    # Verifica se todas as linhas têm o mesmo número de respostas
    num_respostas = len(respostas_por_participante[0])
    for i, respostas in enumerate(respostas_por_participante):
        if len(respostas) != num_respostas:
            print(f"Aviso: A linha {i + 1} tem {len(respostas)} respostas, esperava {num_respostas}")

    # Transpõe a matriz para agrupar respostas do mesmo tipo
    resposta_final = list(zip(*respostas_por_participante))

    # Converte tuplas para listas
    resposta_final = [list(grupo) for grupo in resposta_final]

    return resposta_final


# Exemplo de uso:
if __name__ == "__main__":
    # Substitua pelo caminho do seu arquivo
    arquivo = 'respostas.txt'

    try:
        resultado = processar_respostas(arquivo)

        # Converte para formato JSON
        json_output = json.dumps(resultado, indent=2, ensure_ascii=False)

        print("Respostas agrupadas em formato JSON:")
        print(json_output)

        # Se quiser salvar em um arquivo JSON
        with open('respostas.json', 'w', encoding='utf-8') as f:
            json.dump(resultado, f, indent=2, ensure_ascii=False)
        print("\nArquivo 'respostas.json' salvo com sucesso!")

    except FileNotFoundError:
        print(f"Erro: Arquivo '{arquivo}' não encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")