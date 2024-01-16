import json
with open('autores_orgaos_resumo.json', 'r', encoding='utf-8-sig') as openfile:
    original_list = json.load(openfile)

unique_list = list(set(original_list))

# Print the unique list
print(unique_list)
