import asyncio
from neo4j import GraphDatabase, async_session
import json

class AsyncApp:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    async def close(self):
        # Close the driver connection when you are finished with it
        await self.driver.close()

    async def create_nodes_from_json(self, async_session, json_data):
        query = """
        UNWIND $jsonList AS item
        CREATE (n:Prepositions)
        SET n = item
        """
        result = await async_session.run(query, jsonList=json_data)
        return [row async for row in result]

    async def create_not_existent_prepositions(self):
        with open('output/preposicoes_detalhes_limpos_2.json', 'r', encoding='utf-8-sig') as openfile:
            prepositions = json.load(openfile)

        tasks = []
        async with self.driver.session(database="neo4j") as session:
            for preposition in prepositions:
                print(f"Will create preposicoes: {preposition}")
                # Schedule the coroutine for execution
                task = asyncio.create_task(self.create_nodes_from_json(session, preposition))
                tasks.append(task)

            results = await asyncio.gather(*tasks)
            for result in results:
                for row in result:
                    print(f"Created preposicoes: {row}")

if __name__ == "__main__":
    uri = "neo4j+ssc://b9d9f1f9.databases.neo4j.io"
    user = "neo4j"
    password = "ZNJJl1cee3r3W0txq8NqfQHO5hxrePXvigMDXt9Bzyc"
    app = AsyncApp(uri, user, password)
    asyncio.run(app.create_not_existent_prepositions())
    asyncio.run(app.close())
