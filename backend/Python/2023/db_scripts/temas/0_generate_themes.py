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
        CREATE (n:Themes)
        SET n = item
        """
        result = tx.run(query, jsonList=json_data)
        return [row for row in result]


    def create_not_existent_deputies(self):
        with open('input/temas.json', 'r', encoding='utf-8-sig') as openfile:
            themes = json.load(openfile)

        for theme in themes['dados']:
            print("Will create theme: {row}".format(row=theme))
            with self.driver.session(database="neo4j") as session:
                result = session.execute_write(self.create_nodes_from_json, theme)
                for row in result:
                    print("Created theme: {row}".format(row=row))

if __name__ == "__main__":
    # Aura queries use an encrypted connection using the "neo4j+s" URI scheme
    uri = "neo4j+ssc://b9d9f1f9.databases.neo4j.io"
    user = "neo4j"
    password = ""
    app = App(uri, user, password)
    # app.
    app.create_not_existent_deputies()
    app.close()
