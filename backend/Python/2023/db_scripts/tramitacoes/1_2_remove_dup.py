import json

with open('output/results.json', 'r', encoding='utf-16') as file:
    results = json.load(file)

seen_ids = set()
unique_objects = []

for obj in results:
    try:
        if obj is not None and obj["id"] not in seen_ids:
            unique_objects.append(obj)
            seen_ids.add(obj["id"])
    except Exception  as e:
        print(f"Failed to fetch data for obj {obj}: {e}")

# Optionally, you can save this list to a file
with open('output/unique_results.json', 'w', encoding='utf-8') as file:
    json.dump(unique_objects, file, indent=4, ensure_ascii=False)