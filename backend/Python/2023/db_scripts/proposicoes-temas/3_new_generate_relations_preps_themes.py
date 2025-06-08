import json
import concurrent.futures
from neo4j import GraphDatabase

class App:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        # Verifying connectivity is essential but ensure that the driver instance is preserved.
        with self.driver.session() as session:
            session.run("RETURN 1")

    def close(self):
        # Ensures the driver connection is properly closed when done.
        self.driver.close()

    def execute_command(self, command):
        # This function is intended to be executed within a separate thread.
        # Each thread will use its own session.
        with self.driver.session(database="neo4j") as session:
            session.run(command)
            print(f"Executed command: {command}")

    def create_not_existent_deputies(self):
        with open('output/relations_preps_themes_2.json', 'r', encoding='utf-8-sig') as openfile:
            commands = json.load(openfile)

        # Execute the commands in parallel using ThreadPoolExecutor.
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(self.execute_command, command) for command in commands]

            # If needed, handle futures to process results or catch exceptions.
            for future in concurrent.futures.as_completed(futures):
                try:
                    # There's no return value expected here, but it's useful for catching exceptions.
                    future.result()
                except Exception as e:
                    print(f"An exception occurred: {e}")

if __name__ == "__main__":
    uri = "neo4j+ssc://b9d9f1f9.databases.neo4j.io"
    user = "neo4j"
    password = ""
    app = App(uri, user, password)
    app.create_not_existent_deputies()
    app.close()
