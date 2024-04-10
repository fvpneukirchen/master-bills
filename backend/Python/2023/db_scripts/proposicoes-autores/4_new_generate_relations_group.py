import json
import concurrent.futures
from neo4j import GraphDatabase

class App:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        # It's important to verify connectivity without closing the driver prematurely.
        with self.driver.session() as session:
            session.run("RETURN 1")

    def close(self):
        # Ensures the driver connection is properly closed when done.
        self.driver.close()

    def execute_command(self, command):
        # This method executes a single Neo4j command.
        # Each thread will have its own session to ensure thread safety.
        with self.driver.session(database="neo4j") as session:
            session.run(command)
            print(f"Executed command: {command}")

    def create_not_existent_deputies(self):
        with open('output/relations_groups_2.json', 'r', encoding='utf-8-sig') as openfile:
            commands = json.load(openfile)

        # Use ThreadPoolExecutor to execute commands concurrently.
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self.execute_command, command) for command in commands]

            # Optional: Handle future results as they complete.
            for future in concurrent.futures.as_completed(futures):
                try:
                    # No return value is expected, but it's useful for catching exceptions.
                    future.result()
                except Exception as e:
                    print(f"An exception occurred during command execution: {e}")

if __name__ == "__main__":
    uri = "neo4j+ssc://b9d9f1f9.databases.neo4j.io"
    user = "neo4j"
    password = "ZNJJl1cee3r3W0txq8NqfQHO5hxrePXvigMDXt9Bzyc"
    app = App(uri, user, password)
    app.create_not_existent_deputies()
    app.close()
