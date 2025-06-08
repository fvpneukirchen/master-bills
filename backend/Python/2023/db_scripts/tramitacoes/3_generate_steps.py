import concurrent
import json
import time

from neo4j import GraphDatabase

max_workers = 30

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

    def create_relation(self, command):
        with self.driver.session(database="neo4j") as session:
            result = session.run(command)
            for row in result:
                print("Created relation for: {row}".format(row=row))


    def create_relations(self):
        with open('output/relations/output_queries_1.json', 'r', encoding='utf-8-sig') as openfile:
            deputies = json.load(openfile)
        #
        # for command in deputies:
        #     print("Will create command: {row}".format(row=command))
        #     with self.driver.session(database="neo4j") as session:
        #         result = session.run(command)
        #         print("Created relation: " + command)

        now = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self.create_relation, command) for command in deputies]
            for future in concurrent.futures.as_completed(futures):
                try:
                    # You can add error handling or additional processing here if needed
                    future.result()
                except Exception as e:
                    print(f"{time.time()} Exception occurred: {e}")

        time_taken = time.time() - now
        print(time_taken)


if __name__ == "__main__":
    # Aura queries use an encrypted connection using the "neo4j+s" URI scheme
    uri = "neo4j+ssc://b9d9f1f9.databases.neo4j.io"
    user = "neo4j"
    password = ""
    app = App(uri, user, password)
    app.create_relations()
    app.close()
