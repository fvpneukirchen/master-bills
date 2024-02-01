import json

with open('output/results.json', 'r', encoding='utf-16') as file:
    results = json.load(file)

# Initialize a set to hold the extracted IDs (set ensures uniqueness)
orgao_ids_set = set()

# Define the substring to remove from the uriOrgao
substring_to_remove = "https://dadosabertos.camara.leg.br/api/v2/orgaos/"

# Iterate over the results and extract the orgao IDs
for result in results:
    if result is not None:
        if result['data'] is not None:
            for data_entry in result['data']:
                uri_orgao = data_entry.get('uriOrgao')
                if uri_orgao and uri_orgao.startswith(substring_to_remove):
                    orgao_id = uri_orgao.replace(substring_to_remove, '')
                    orgao_ids_set.add(orgao_id)

# Convert the set back to a list if needed (optional)
orgao_ids = list(orgao_ids_set)

# Optionally, you can save this list to a file
with open('output/orgao_ids.json', 'w', encoding='utf8') as file:
    json.dump(orgao_ids, file)