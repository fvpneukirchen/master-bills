import json
import os

# Define the input data
with open('output/detalhes_membros_grupos_com_perm.json', 'r', encoding='utf-8-sig') as openfile:
    input_data = json.load(openfile)

# Generate the queries
queries = []
for group in input_data:
    groupId = group["groupId"]
    for deputy in group["deputies"]:
        deputyId = deputy["id"]
        idLegislatura = deputy["idLegislatura"]
        dataFim = f"'{deputy['dataFim']}'" if deputy["dataFim"] else "null"
        dataInicio = f"'{deputy['dataInicio']}'" if deputy["dataInicio"] else "null"
        codTitulo = deputy["codTitulo"]
        titulo = deputy["titulo"].replace("'", "\\'")

        query = (
            f"MATCH (d:Deputies {{id: {deputyId}}}), (g:Groups {{id: {groupId}}}) "
            f"CREATE (d)-[:IS_MEMBER {{"
            f"idLegislatura: {idLegislatura}, "
            f"dataFim: {dataFim}, "
            f"dataInicio: {dataInicio}, "
            f"codTitulo: {codTitulo}, "
            f"titulo: '{titulo}'"
            f"}}]->(g)"
        )
        queries.append(query)

with open("output/relations_membros_grupos_com_perm.json", "w", encoding='utf8') as outfile:
    json.dump(queries, outfile, indent=4, ensure_ascii=False)
