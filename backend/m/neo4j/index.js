const neo4j = require("neo4j-driver");
const fetch = require('cross-fetch');


const driver = neo4j.driver(
  "neo4j+s://32a0b9ea.databases.neo4j.io:7687",
  neo4j.auth.basic("neo4j", "vn1ci786q1eB_ZFdtwgEphSAon8x5G0803oYVnHkHC4")
);

// const session = driver.session();
// const personName = "Alice";
// const loader = async () => {
//   try {
//     const result = await session.run(
//       "CREATE (a:Person {name: $name}) RETURN a",
//       {
//         name: personName,
//       }
//     );

//     const singleRecord = result.records[0];
//     const node = singleRecord.get(0);

//     console.log(node.properties.name);
//   } finally {
//     await session.close();
//   }

//   // on application exit:
//   await driver.close();
// };

// loader();

fetch("./deputies.json")
  .then((response) => response.json())
  .then((json) => console.log(json));
