import concurrent
import json
import time

from neo4j import GraphDatabase

max_workers = 5


class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.driver.verify_connectivity()

    def close(self):
        self.driver.close()

    def create_relation(self, check_query, create_query):
        with self.driver.session(database="neo4j") as session:
            # Step 1: Check if the relationship exists
            result = session.run(check_query)
            record = result.single()
            relationship_exists = record["relationshipExists"] if record else False

            # Step 2: Create the relationship if it does not exist
            if not relationship_exists:
                session.run(create_query)
                print(f"Created relation: {create_query}")
            else:
                print(f"Relation already exists, skipped creation: {check_query}")

    def create_relations(self):
        with open('output/relations/output_queries_1.json', 'r', encoding='utf-8-sig') as openfile:
            query_pairs = json.load(openfile)

        now = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self.create_relation, check_query, create_query)
                       for check_query, create_query in query_pairs]
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Exception occurred: {e}")

        time_taken = time.time() - now
        print(f"Time taken: {time_taken}")


if __name__ == "__main__":
    # Aura queries use an encrypted connection using the "neo4j+s" URI scheme
    uri = "neo4j+ssc://b9d9f1f9.databases.neo4j.io"
    user = "neo4j"
    password = "ZNJJl1cee3r3W0txq8NqfQHO5hxrePXvigMDXt9Bzyc"
    app = App(uri, user, password)
    app.create_relations()
    app.close()
