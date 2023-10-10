import json

from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable


class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    # def create_friendship(self, person1_name, person2_name):
    #     with self.driver.session(database="neo4j") as session:
    #         # Write transactions allow the driver to handle retries and transient errors
    #         result = session.execute_write(
    #             self._create_and_return_friendship, person1_name, person2_name)
    #         for row in result:
    #             print("Created friendship between: {p1}, {p2}".format(p1=row['p1'], p2=row['p2']))
    #
    # @staticmethod
    # def _create_and_return_friendship(tx, person1_name, person2_name):
    #     # To learn more about the Cypher syntax, see https://neo4j.com/docs/cypher-manual/current/
    #     # The Reference Card is also a good resource for keywords https://neo4j.com/docs/cypher-refcard/current/
    #     query = (
    #         "CREATE (p1:Person { name: $person1_name }) "
    #         "CREATE (p2:Person { name: $person2_name }) "
    #         "CREATE (p1)-[:KNOWS]->(p2) "
    #         "RETURN p1, p2"
    #     )
    #     result = tx.run(query, person1_name=person1_name, person2_name=person2_name)
    #     try:
    #         return [{"p1": row["p1"]["name"], "p2": row["p2"]["name"]}
    #                 for row in result]
    #     # Capture any errors along with the query and data for traceability
    #     except ServiceUnavailable as exception:
    #         logging.error("{query} raised an error: \n {exception}".format(
    #             query=query, exception=exception))
    #         raise

    def create_not_existent_deputies(self):
        with open('not_created_deputies_id.json', 'r', encoding='utf-8-sig') as openfile:
            d_ids = json.load(openfile)

        with open('deputies.json', 'r', encoding='utf-8-sig') as openfile:
            deputies = json.load(openfile)

        for d_id in d_ids:
            d_data = next(d for d in deputies if d_id == d["id"])
            print("Will create deputy: {row}".format(row=d_data))
            with self.driver.session(database="neo4j") as session:
                result = session.execute_read(self._create_and_return_person(), d_data)
                for row in result:
                    print("Created deputy: {row}".format(row=row))


    def check_existent_deputies(self):
        with open('deputies.json', 'r', encoding='utf-8-sig') as openfile:
            deputies = json.load(openfile)
            for d in deputies:
                with self.driver.session(database="neo4j") as session:
                    result = session.execute_read(self._find_and_return_person, str(d["id"]))

                    if len(result) > 0:
                        for row in result:
                            print("Found person: {row}".format(row=row))
                    else:
                        print("Not found person: {row}".format(row=d))

    def find_person(self, person_name):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_read(self._find_and_return_person, person_name)
            for row in result:
                print("Found person: {row}".format(row=row))

    @staticmethod
    def _find_and_return_person(tx, person_name):
        query = (
            "MATCH (p:Deputies) "
            "WHERE p.id = $person_name "
            "RETURN p.nome AS name, p.siglaPartido"
        )
        result = tx.run(query, person_name=person_name)
        # return [row["name"] for row in result]
        return [row for row in result]

    @staticmethod
    def _create_and_return_person(tx, person_name):
        query = (
            "MATCH (p:Deputies) "
            "WHERE p.id = $person_name "
            "RETURN p.nome AS name, p.siglaPartido"
        )
        result = tx.run(query, person_name=person_name)
        # return [row["name"] for row in result]
        return [row for row in result]


if __name__ == "__main__":
    # Aura queries use an encrypted connection using the "neo4j+s" URI scheme
    uri = "neo4j+s://32a0b9ea.databases.neo4j.io"
    user = "neo4j"
    password = "vn1ci786q1eB_ZFdtwgEphSAon8x5G0803oYVnHkHC4"
    app = App(uri, user, password)
    # app.create_friendship("Alice", "David")
    # app.find_person("204397")
    # app.check_existent_deputies()
    create_not_existent_deputies()
    app.close()
