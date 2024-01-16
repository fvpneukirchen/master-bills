import json

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

    @staticmethod
    def create_nodes_from_json(tx, json_data):
        # Define your node creation query with UNWIND and SET
        query = """
        UNWIND $jsonList AS item
        CREATE (n:Groups)
        SET n = item
        """
        result = tx.run(query, jsonList=json_data)
        return [row for row in result]


    def create_not_existent_deputies(self):
        with open('output/detalhes_grupos.json', 'r', encoding='utf-8-sig') as openfile:
            groups = json.load(openfile)

        for group in groups:
            print("Will create theme: {row}".format(row=group['dados']))
            with self.driver.session(database="neo4j") as session:
                result = session.execute_write(self.create_nodes_from_json, group['dados'])
                for row in result:
                    print("Created group: {row}".format(row=row))

if __name__ == "__main__":
    # Aura queries use an encrypted connection using the "neo4j+s" URI scheme
    uri = "neo4j+ssc://b9d9f1f9.databases.neo4j.io"
    user = "neo4j"
    password = "ZNJJl1cee3r3W0txq8NqfQHO5hxrePXvigMDXt9Bzyc"
    app = App(uri, user, password)
    # app.
    app.create_not_existent_deputies()
    app.close()
