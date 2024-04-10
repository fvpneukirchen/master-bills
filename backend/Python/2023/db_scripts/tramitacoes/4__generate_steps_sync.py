import json
import time

from neo4j import GraphDatabase

class App:

    def __init__(self, uri, user, password):
        URI = uri
        AUTH = (user, password)
        with GraphDatabase.driver(URI, auth=AUTH) as driver:
            self.driver = driver
            # self.driver = GraphDatabase.driver(uri, auth=(user, password))
            self.driver.verify_connectivity()

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
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
                #print(f"Created relation: {create_query}")
            #else:
                #print(f"Relation already exists, skipped creation: {check_query}")

    def create_relations(self):
        # 1 2
        # Exception occurred: Failed to read from defunct connection IPv4Address(('b9d9f1f9.databases.neo4j.io', 7687)) (ResolvedIPv4Address(('34.69.128.95', 7687))) - MATCH (p:Prepositions {id: 2406583}), (g:Groups {id: 186}) OPTIONAL MATCH (p)-[r:HAS_STEP3 {sequencia: 13}]->(g) RETURN r IS NOT NULL AS relationshipExists
        with open('output/relations/output_queries_2_3.json', 'r', encoding='utf-8-sig') as openfile:
            query_pairs = json.load(openfile)

        now = time.time()

        for check_query, create_query in query_pairs:
            try:
                self.create_relation(check_query, create_query)
            except Exception as e:
                print(f"Exception occurred: {e} - {check_query}")

        time_taken = time.time() - now
        print(f"Time taken: {time_taken}")


if __name__ == "__main__":
    # Aura queries use an encrypted connection using the "neo4j+s" URI scheme
    uri = "neo4j+ssc://b9d9f1f9.databases.neo4j.io"
    user = "neo4j"
    password = "ZNJJl1cee3r3W0txq8NqfQHO5hxrePXvigMDXt9Bzyc"
    app = App(uri, user, password)
    # app.
    app.create_relations()
    app.close()
