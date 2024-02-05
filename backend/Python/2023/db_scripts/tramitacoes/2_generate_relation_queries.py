import json

# Define the base URL to be removed
base_url = "https://dadosabertos.camara.leg.br/api/v2/orgaos/"

# Initialize counters
file_counter = 1
entry_counter = 0
entry_counter_2 = 0
max_entries_per_file = 10000  # Adjust as needed based on memory constraints

with open('output/results.json', 'r', encoding='utf-16') as file:
    results = json.load(file)

# def generate_data_entry_str(data_entry):
#     # Start the data entry string
#     data_entry_str = "{"
#     # Iterate over the items in the dictionary
#     for key, value in data_entry.items():
#         # For each item, add "key: value" to the string
#         if value is not None:
#             if isinstance(value, str):  # Check if the value is a string
#                 value_str = "'" + value.replace("'", "\\'").replace('"', '\\"') + "'"
#             else:
#                 value_str = str(value)  # Convert non-string values to string without quotes
#             data_entry_str += f"{key}: {value_str}, "
#     # Remove the last comma and space, and close the curly brace
#     data_entry_str = data_entry_str.rstrip(", ") + "}"
#     return data_entry_str
# def generate_query(preposition_id, group_id, data_entry):
#     data_entry_str = generate_data_entry_str(data_entry)
#     return f'MATCH (p:Prepositions {{id: {preposition_id}}}), (g:Groups {{id: {group_id}}}) CREATE (p)-[:HAS_STEP {data_entry_str}]->(g)'

def generate_query(preposition_id, group_id, data_entry):
    # Create the base query
    query = (
        f"MATCH (p:Prepositions {{id: {preposition_id}}}), "
        f" (g:Groups {{id: {group_id}}})"
        f" OPTIONAL MATCH (p)-[h:HAS_STEP {{sequencia: {data_entry.get('sequencia', 'null')}}}]->(g)"
        f" MERGE (p)-[r:HAS_STEP]->(g)"
        f" ON CREATE SET "
    )

    # Generate the 'ON CREATE SET' clauses
    set_clauses = []
    for key, value in data_entry.items():
        # Skip 'sequencia' as it is already used in OPTIONAL MATCH
        if value is not None:
            if isinstance(value, str):
                # Escape single quotes and wrap the value in single quotes
                value_str = "'" + value.replace("'", "\\'").replace('"', '\\"') + "'"
            else:
                value_str = str(value)
            set_clauses.append(f"r.{key} = {value_str}")

    # Join the set clauses and append to the query
    query += ", ".join(set_clauses)
    query += " RETURN p.id, r.sequencia, g.id"

    return query

# output_acumm = []
#
# # Process each element in the JSON array
# for obj in results:
#     # Open a new output file if the entry counter has reached the max entries per file
#     if entry_counter % max_entries_per_file == 0 and entry_counter > 0:
#         entry_counter = 0
#         with open(f'output/relations/output_queries_{file_counter}.json', 'w', encoding='utf8') as outfile:
#             json.dump(output_acumm, outfile, indent=4, ensure_ascii=False)
#         outfile.close()
#         output_acumm = []
#         file_counter += 1
#
#     if obj is not None:
#         # Process the data entries
#         preposition_id = obj["id"]
#         for data_entry in obj["data"]:
#             group_id = data_entry["uriOrgao"].replace(base_url, "")
#             output_acumm.append(generate_query(preposition_id, group_id, data_entry))
#             entry_counter += 1
#             entry_counter_2 += 1
#
# print(f"Processed {entry_counter_2} entries in {file_counter - 1} files.")

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
            output_acumm.append(generate_query(preposition_id, group_id, data_entry))
            entry_counter += 1
            entry_counter_2 += 1

# Write the final batch of data to a file if there's any data left
if output_acumm:
    with open(f'output/relations/output_queries_{file_counter}.json', 'w', encoding='utf8') as outfile:
        json.dump(output_acumm, outfile, indent=4, ensure_ascii=False)

print(f"Processed {entry_counter_2} entries in {file_counter} files.")