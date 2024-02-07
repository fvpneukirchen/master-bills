import json

# Define the base URL to be removed
base_url = "https://dadosabertos.camara.leg.br/api/v2/orgaos/"

# Initialize counters
file_counter = 1
entry_counter = 0
entry_counter_2 = 0
max_entries_per_file = 50000  # Adjust as needed based on memory constraints

with open('output/unique_results.json', 'r', encoding='utf-8') as file:
    results = json.load(file)

def generate_data_entry_str(data_entry):
    # Start the data entry string
    data_entry_str = "{"
    # Iterate over the items in the dictionary
    for key, value in data_entry.items():
        # For each item, add "key: value" to the string
        if value is not None:
            if isinstance(value, str):  # Check if the value is a string
                value_str = "'" + value.replace("'", "\\'").replace('"', '\\"') + "'"
            else:
                value_str = str(value)  # Convert non-string values to string without quotes
            data_entry_str += f"{key}: {value_str}, "
    # Remove the last comma and space, and close the curly brace
    data_entry_str = data_entry_str.rstrip(", ") + "}"
    return data_entry_str

#def generate_query(preposition_id, group_id, data_entry):
#    data_entry_str = generate_data_entry_str(data_entry)
#    return f'MATCH (p:Prepositions {{id: {preposition_id}}}), (g:Groups {{id: {group_id}}}) CREATE (p)-[:HAS_STEP{file_counter} {data_entry_str}]->(g)'

def generate_queries(preposition_id, group_id, data_entry):
    data_entry_str = generate_data_entry_str(data_entry)
    check_query = (
        f"MATCH (p:Prepositions {{id: {preposition_id}}}), (g:Groups {{id: {group_id}}}) "
        f"OPTIONAL MATCH (p)-[r:HAS_STEP{file_counter} {{sequencia: {data_entry['sequencia']}}}]->(g) "
        f"RETURN r IS NOT NULL AS relationshipExists"
    )
    create_query = (
        f"MATCH (p:Prepositions {{id: {preposition_id}}}), (g:Groups {{id: {group_id}}}) "
        f"CREATE (p)-[:HAS_STEP{file_counter} {data_entry_str}]->(g)"
    )
    return check_query, create_query

output_acumm = []

# Process each element in the JSON array
for obj in results:
    if obj is not None:
        # Process the data entries
        preposition_id = obj["id"]
        for data_entry in obj["data"]:
            # Check if we need to write the current batch to a file and start a new batch
            if entry_counter >= max_entries_per_file:
                with open(f'output/relations/output_queries_{file_counter}.json', 'w', encoding='utf8') as outfile:
                    json.dump(output_acumm, outfile, indent=4, ensure_ascii=False)
                entry_counter = 0  # Reset entry_counter for the new file
                output_acumm = []  # Reset output_acumm for the new file
                file_counter += 1  # Increment file_counter to create a new file

            group_id = data_entry["uriOrgao"].replace(base_url, "")
            output_acumm.append(generate_queries(preposition_id, group_id, data_entry))
            entry_counter += 1
            entry_counter_2 += 1

# Write the final batch of data to a file if there's any data left
if output_acumm:
    with open(f'output/relations/output_queries_{file_counter}.json', 'w', encoding='utf8') as outfile:
        json.dump(output_acumm, outfile, indent=4, ensure_ascii=False)

print(f"Processed {entry_counter_2} entries in {file_counter} files.")