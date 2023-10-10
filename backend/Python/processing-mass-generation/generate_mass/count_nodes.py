# coding: utf8
import asyncio
import json
from operator import itemgetter
from datetime import datetime
import pandas as pd

import itertools


async def main():
    with open('nodes.json', 'r', encoding='utf8') as openfile:
        nodes = json.load(openfile)

        r = []
        for n in nodes:
            r.append(n)



        with open('out_nodes.json', "w", encoding='utf8') as outfile:
            json.dump(r, outfile, indent=4, ensure_ascii=False)


asyncio.run(main())
