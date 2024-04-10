import requests
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Read the id_list from a JSON file
with open('input/prep_list_2.json', 'r', encoding='utf-8-sig') as file:
#with open('output/fails4_1.json', 'r', encoding='utf-8-sig') as file:
    preps = json.load(file)

# Define the base URL
base_url = "https://dadosabertos.camara.leg.br/api/v2/proposicoes/{}/tramitacoes"


def fetch_data(id):
    try:
        response = requests.get(base_url.format(id))
        response.raise_for_status()  # Raises an HTTPError if the status is 4xx, 5xx
        data = response.json().get('dados', [])
        return {'id': id, 'data': data}
    except Exception as e:
        fails.append(id)
        print(f"Failed to fetch data for ID {id}: {e}")


# Define the number of workers for ThreadPoolExecutor
number_of_workers = 50  # Adjust this number based on your machine's capabilities

results = []
fails = []

with ThreadPoolExecutor(max_workers=number_of_workers) as executor:
    # Initiate all the tasks and mark them for execution
    now = time.time()
    future_to_id = {executor.submit(fetch_data, p): p for p in preps}

    # As the tasks complete, process the results
    for future in as_completed(future_to_id):
        id = future_to_id[future]
        try:
            data = future.result()
            results.append(data)
            print(f" results {len( results)}")
        except Exception as e:
            print(f"ID {id} generated an exception: {e}")
            fails.append(id)

    time_taken = time.time() - now
    print(time_taken)

# Optionally, save the results to a file
with open('output/results_2.json', 'w', encoding='utf8') as f:
    json.dump(results, f, indent=4, ensure_ascii=False)

with open('output/fails_2.json', 'w', encoding='utf8') as f:
    json.dump(fails, f, indent=4, ensure_ascii=False)
