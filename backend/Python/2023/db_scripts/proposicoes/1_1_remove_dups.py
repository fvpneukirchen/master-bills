import json


def load_json_file(file_path):
    """Load a JSON file and return its contents."""
    with open(file_path, 'r') as file:
        return json.load(file)


def find_unique_elements(input1, input2):
    """Find elements that are unique to either of the input lists."""
    set1 = set(input1)
    set2 = set(input2)
    return list((set1 - set2) | (set2 - set1))


def main():
    # Load the contents of both JSON files
    input1 = load_json_file('output/lista_preposicoes_detalhes_urls.json')
    input2 = load_json_file('output/lista_preposicoes_detalhes_urls_2_1.json')

    # Find unique elements
    final_result = find_unique_elements(input1, input2)

    with open("output/lista_preposicoes_detalhes_urls_sem_dups_PLS.json", "w", encoding='utf8') as outfile:
        json.dump(final_result, outfile, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
