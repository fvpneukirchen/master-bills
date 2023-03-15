import express, { query } from "express";
import fs from "fs";
import neo4j from "neo4j-driver";

const validIds = [204554,
  204521,
  204379,
  204560,
  204528,
  121948,
  74646,
  141372,
  160508,
  136811,
  178835,
  160527,
  204495,
  204549,
  178836,
  160559,
  204413,
  204545,
  204501,
  160511,
  178972,
  204571,
  204544,
  160545,
  204503,
  204516,
  74057,
  178927,
  204353,
  204400,
  178937,
  178881,
  204356,
  178831,
  74471,
  204423,
  133439,
  178882,
  204515,
  73696,
  160553,
  73433,
  141391,
  204414,
  160541,
  160600,
  74090,
  74459,
  160665,
  204509,
  160512,
  69871,
  178975,
  73701,
  109429,
  141335,
  204358,
  178948,
  207176,
  204374,
  204388,
  141513,
  204561,
  160538,
  74052,
  204551,
  204502,
  160589,
  93083,
  204352,
  204572,
  178829,
  178924,
  204487,
  213762,
  204507,
  141401,
  204361,
  178962,
  178993,
  204460,
  74262,
  204426,
  141398,
  164360,
  204369,
  204499,
  204380,
  204370,
  178876,
  204488,
  141405,
  73441,
  204496,
  204504,
  205476,
  204490,
  141439,
  204476,
  204462,
  178928,
  204440,
  178939,
  74537,
  141408,
  204376,
  204378,
  204514,
  178963,
  135054,
  204355,
  141411,
  74467,
  74060,
  178916,
  204367,
  204454,
  204409,
  204459,
  160528,
  62881,
  116379,
  205548,
  204451,
  178908,
  204512,
  204569,
  164359,
  204542,
  160588,
  178929,
  160599,
  143632,
  160758,
  204518,
  204481,
  204439,
  204450,
  204351,
  204412,
  81297,
  204434,
  178994,
  204562,
  141417,
  74655,
  204541,
  92346,
  204500,
  178977,
  141421,
  141422,
  74075,
  204364,
  160532,
  204389,
  178854,
  218086,
  198783,
  161550,
  132504,
  204537,
  160575,
  160640,
  204482,
  178871,
  178953,
  68720,
  178969,
  141427,
  171623,
  204368,
  160587,
  66828,
  204477,
  72442,
  204398,
  204371,
  160666,
  204407,
  141431,
  92699,
  204427,
  204411,
  160598,
  141434,
  191923,
  204392,
  204510,
  204494,
  204393,
  74200,
  115746,
  160669,
  204473,
  204484,
  204527,
  178966,
  204394,
  74383,
  204575,
  204491,
  74270,
  204365,
  160673,
  178996,
  152605,
  204419,
  107283,
  74419,
  198197,
  204513,
  204531,
  160667,
  204442,
  73460,
  204408,
  204456,
  204465,
  204548,
  178964,
  178873,
  204373,
  178909,
  204444,
  73482,
  204539,
  178981,
  73772,
  178884,
  178959,
  141450,
  160674,
  204533,
  204564,
  204508,
  67138,
  204436,
  73531,
  74848,
  108338,
  74273,
  160570,
  178839,
  204435,
  160531,
  74366,
  141458,
  178970,
  141459,
  112437,
  178910,
  204468,
  204546,
  217480,
  205550,
  178857,
  218245,
  141464,
  141470,
  204386,
  204472,
  204391,
  160619,
  74079,
  204555,
  74554,
  209189,
  204563,
  215043,
  204474,
  204420,
  74317,
  204372,
  73586,
  74253,
  204457,
  204520,
  204497,
  204574,
  204550,
  178886,
  204536,
  151208,
  141478,
  98057,
  160534,
  178832,
  204375,
  178825,
  204359,
  204547,
  122195,
  74156,
  74254,
  74299,
  92102,
  139285,
  74585,
  204405,
  204382,
  196358,
  204523,
  204404,
  178879,
  74478,
  178931,
  178954,
  204381,
  160510,
  204410,
  204448,
  204485,
  204455,
  162332,
  204526,
  74784,
  204418,
  178866,
  166402,
  204458,
  204471,
  156190,
  179000,
  146788,
  205863,
  76874,
  133810,
  204558,
  204556,
  118594,
  178983,
  179001,
  204452,
  150418,
  204522,
  160535,
  204431,
  204506,
  178943,
  204430,
  74398,
  178956,
  204428,
  204432,
  74158,
  178858,
  204403,
  204566,
  178843,
  75431,
  204486,
  74749,
  141508,
  188097,
  178984,
  178985,
  92172,
  154178,
  178895,
  178997,
  204453,
  204449,
  204415,
  146307,
  74165,
  178896,
  204479,
  74352,
  178986,
  194260,
  66179,
  74159,
  204498,
  178987,
  204363,
  73463,
  73692,
  204422,
  141515,
  204441,
  204475,
  204573,
  160556,
  160642,
  204570,
  204553,
  74160,
  204377,
  171617,
  141516,
  178860,
  204538,
  193726,
  160558,
  204461,
  204492,
  74574,
  141518,
  74400,
  133968,
  141488,
  216544,
  90201,
  215045,
  178912,
  217330,
  122974,
  204395,
  160604,
  178844,
  204406,
  73943,
  204524,
  204529,
  73486,
  160601,
  204390,
  204383,
  204446,
  204565,
  160639,
  160641,
  204467,
  178951,
  204567,
  141523,
  74161,
  205865,
  178925,
  178989,
  73801,
  73788,
  215042,
  204362,
  160655,
  213274,
  178920,
  204489,
  160653,
  204530,
  204366,
  141531,
  204480,
  160651,
  178930,
  178861,
  204525,
  178945,
  204357,
  178935,
  73466,
  74371,
  178887,
  73604,
  160635,
  204535,
  178990,
  204416,
  204387,
  178921,
  73808,
  178933,
  204438,
  204437,
  178961,
  204557,
  74356,
  204360,
  204425,
  178946,
  178947,
  92776,
  177282,
  204534,
  178922,
  204464,
  206231,
  204466,
  178862,
  143084,
  204519,
  160976,
  197438,
  178934,
  157130,
  178863,
  195866,
  204385,
  160610,
  74376,
  141553,
  204505,
  204396,
  74283,
  137070,
  204483,
  141555,
  204532,
  179587,
  178992,
  215044,
  160569,
  178952,
  160518,
  74043,
  74044,
  74439,
  178889,
  204559,
  160632,
  204517,
  160592];

const driver = neo4j.driver(
  "neo4j+s://32a0b9ea.databases.neo4j.io:7687",
  neo4j.auth.basic("neo4j", "vn1ci786q1eB_ZFdtwgEphSAon8x5G0803oYVnHkHC4")
);

const router = express.Router();

// router.get("/pl", async function (req, res, next) {
//   fs.readFile("out-parallel-4-5.json", async (err, data) => {
//     if (err) throw err;
//     const bills = JSON.parse(data);
//     const session = driver.session();
//     try {
//       const result = await session.run(
//         "WITH $bills AS document UNWIND document.dados AS data CREATE(m:`Bills`) SET m = data",
//         { bills: bills }
//       );

//       console.log(result.records);
//       // on application exit:
//       await driver.close();
//     } catch (e) {
//       console.error(e);
//       next();
//     } finally {
//       await session.close();
//     }

//     return res.status(200).json(bills);
//   });
// });

router.get("/pl-t", async function (req, res, next) {
  
  fs.readFile("pls-and-themes-5.json", async (err, data) => {
    if (err) throw err;
    const plsAndThemes = JSON.parse(data);

    const out = [];


    for (const [key, value] of Object.entries(plsAndThemes)) {
      const entry = Object.entries(value);

      const plId = entry[0][0];

      for(const themeEntry of entry[0][1]) {
        const codTema = themeEntry.codTema;
        out.push(`MATCH (a:Themes), (b:Bills) WHERE a.cod = "${codTema}" AND b.id = ${plId} CREATE ((a)<-[r:THEME]-(b))`);
      }
  }

    const session = driver.session();
    try {

      for (const queryIndex in out) {
        const query = out[Number(queryIndex)];
        console.log(query);
        const result = await session.run(query);
        console.log(result.records);
      }

      // on application exit:
      await driver.close();
    } catch (e) {
      console.error(e);
      next();
    } finally {
      await session.close();
    }

    return res.status(200).json(out);
  });
});

// router.get("/pl-a", async function (req, res, next) {
  
//   fs.readFile("out-parallel-4-4-authors.json", async (err, data) => {
//     if (err) throw err;
//     const plsAndAuthors = JSON.parse(data);

//     const out = [];

//     for (const entryIndex in plsAndAuthors) {
//       const plAuthors = plsAndAuthors[Number(entryIndex)];
//       const plId = plAuthors.links[0].id;
      
//       for(const authorIndex in plAuthors.dados) {
//         const author = plAuthors.dados[Number(authorIndex)];
//         const split = author.uri.split('/');
//         const authorId = split[split.length - 1];

//         if (!validIds.includes(Number(authorId))) continue;

//         out.push(`MATCH (a:Deputies), (b:Bills) WHERE a.id = ${authorId} AND b.id = ${plId} CREATE ((a)-[r:AUTHORED {codTipo: ${author.codTipo}, tipo: "${author.tipo}", ordemAssinatura: ${author.ordemAssinatura}, proponente: ${author.proponente} }]->(b))`);
//       }
//     }
    

//     const session = driver.session();
//     try {

//       for (const queryIndex in out) {
//         const query = out[Number(queryIndex)];
//         console.log(query);
//         const result = await session.run(query);
//         console.log(result.records);
//       }

//       // on application exit:
//       await driver.close();
//     } catch (e) {
//       console.error(e);
//       next();
//     } finally {
//       await session.close();
//     }

//     return res.status(200).json(out);
//   });
// });


// router.get("/t", async function (req, res, next) {
//   fs.readFile("temas.json", async (err, data) => {
//     if (err) throw err;
//     const t = JSON.parse(data);
//     const session = driver.session();
//     try {
//       const result = await session.run(
//         "WITH $t AS document UNWIND document.dados AS data CREATE(m:`Themes`) SET m = data",
//         { t: t }
//       );

//       console.log(result.records);
//       // on application exit:
//       await driver.close();
//     } catch (e) {
//       console.error(e);
//       next();
//     } finally {
//       await session.close();
//     }

//     return res.status(200).json(t);
//   });
// });


// router.get("/d", async function (req, res, next) {
//   fs.readFile("deputies.json", async (err, data) => {
//     if (err) throw err;
//     const deputies = JSON.parse(data);
//     // const session = driver.session();
//     // try {
//     //   const result = await session.run(
//     //     "WITH $deputies AS document UNWIND document.dados AS data CREATE(m:`Deputies`) SET m = data",
//     //     { deputies: deputies }
//     //   );

//     //   console.log(result.records);
//     //   // on application exit:
//     //   await driver.close();
//     // } catch (e) {
//     //   console.error(e);
//     //   next();
//     // } finally {
//     //   await session.close();
//     // }

//     return res.status(200).json(deputies);
//   });
// });

// router.get("/p", async function (req, res, next) {
//   fs.readFile("parties-2.json", async (err, data) => {
//     if (err) throw err;
//     const parties = JSON.parse(data);
//     const session = driver.session();
//     try {
//       const result = await session.run(
//         "WITH $parties AS document UNWIND document.dados AS data CREATE(m:`Parties`) SET m = data",
//         { parties: parties }
//       );

//       console.log(result.records);
//       // on application exit:
//       await driver.close();
//     } catch (e) {
//       console.error(e);
//       next();
//     } finally {
//       await session.close();
//     }

//     return res.status(200).json(parties);
//   });
// });

export default router;
