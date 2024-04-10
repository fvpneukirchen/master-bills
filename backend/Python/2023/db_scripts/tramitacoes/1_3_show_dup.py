import json

with open('output/results4_1.json', 'r', encoding='utf-16') as file:
    results = json.load(file)

seen_ids = set()
unique_objects = []
none_list = []

for obj in results:
    try:
        if obj is not None:
            if obj["id"] not in seen_ids:
                seen_ids.add(obj["id"])
            else:
                unique_objects.append(obj)
        else:
            none_list.append(obj)
    except Exception  as e:
        print(f"Failed to fetch data for obj {obj}: {e}")

# Optionally, you can save this list to a file
with open('output/show_dups4_1.json', 'w', encoding='utf-8') as file:
    json.dump(unique_objects, file, indent=4, ensure_ascii=False)

with open('output/none_list4_1.json', 'w', encoding='utf-8') as file:
    json.dump(none_list, file, indent=4, ensure_ascii=False)