import json
import concurrent.futures
from neo4j import GraphDatabase

class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        # Check connectivity at the start
        with self.driver.session() as session:
            session.run("RETURN 1")

    def close(self):
        self.driver.close()

    def create_nodes_from_json(self, preposition):
        del preposition['statusProposicao']
        # Define your node creation query with UNWIND and SET
        query = """
        UNWIND $jsonList AS item
        CREATE (n:Prepositions)
        SET n = item
        """
        with self.driver.session(database="neo4j") as session:
            # Since this is just an example, ensure your query and parameters match your needs
            result = session.execute_write(lambda tx: tx.run(query, jsonList=[preposition]))
            return [row for row in result]

    def create_not_existent_deputies(self, prepositions, max_workers=50):
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self.create_nodes_from_json, preposition) for preposition in prepositions["200"]]
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    # Assuming the result contains something useful for logging
                    print("Created preposicoes: {}".format(result))
                except Exception as e:
                    print(f"Exception occurred: {e}")

if __name__ == "__main__":
    uri = "neo4j+ssc://b9d9f1f9.databases.neo4j.io"
    user = "neo4j"
    password = ""
    app = App(uri, user, password)

    # Load your JSON data
    with open('output/preposicoes_detalhes_limpos_2.json', 'r', encoding='utf-8-sig') as openfile:
        prepositions = json.load(openfile)

    # Call the concurrent execution function
    app.create_not_existent_deputies(prepositions)
    app.close()
