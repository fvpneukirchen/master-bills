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

    def create_not_existent_deputies(self):
        # with open('output/relations_membros_grupos_com_perm.json', 'r', encoding='utf-8-sig') as openfile:
        with open('output/relations_groups_restantes.json', 'r', encoding='utf-8-sig') as openfile:
            deputies = json.load(openfile)

        for command in deputies:
            print("Will create command: {row}".format(row=command))
            with self.driver.session(database="neo4j") as session:
                result = session.run(command)
                print("Created relation: " + command)


if __name__ == "__main__":
    # Aura queries use an encrypted connection using the "neo4j+s" URI scheme
    uri = "neo4j+ssc://b9d9f1f9.databases.neo4j.io"
    user = "neo4j"
    password = "ZNJJl1cee3r3W0txq8NqfQHO5hxrePXvigMDXt9Bzyc"
    app = App(uri, user, password)
    # app.
    app.create_not_existent_deputies()
    app.close()
