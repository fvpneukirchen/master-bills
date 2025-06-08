import json
import concurrent.futures
from neo4j import GraphDatabase

class App:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def execute_command(self, command):
        # Use a session to execute a single command
        with self.driver.session(database="neo4j") as session:
            # Here we assume the command is a Cypher query string
            session.run(command)
            print(f"Executed command: {command}")

    def create_not_existent_deputies(self):
        with open('output/relations_deputados_2.json', 'r', encoding='utf-8-sig') as openfile:
            deputies = json.load(openfile)

        # Use ThreadPoolExecutor to execute commands in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            # Submit all commands to the executor
            futures = [executor.submit(self.execute_command, command) for command in deputies]

            # Optional: Process future results as they complete
            for future in concurrent.futures.as_completed(futures):
                try:
                    # There's no result to process here, but you could log or handle errors
                    future.result()
                except Exception as e:
                    print(f"Exception occurred during command execution: {e}")

if __name__ == "__main__":
    uri = "neo4j+ssc://b9d9f1f9.databases.neo4j.io"
    user = "neo4j"
    password = ""
    app = App(uri, user, password)
    app.create_not_existent_deputies()
    app.close()
