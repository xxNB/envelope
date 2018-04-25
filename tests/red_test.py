# -*- coding: utf-8 -*-

import random
import aiohttp
import asyncio

all_chr = [chr(i) for i in range(97, 123)]
print(all_chr)


# 抢红包人的名字
def user_name():
    name = "".join(random.sample(all_chr, 4))
    # 每个人抢红包的次数
    times = random.randint(0, 3)
    return {"name": name, "times": times}


async def post(url):
    with aiohttp.ClientSession() as session:
        html = await session.get(url)
        print("html", html)
        html = await html.text
        print(html)
        return html


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    urls = []
    for i in range(103):
        name = user_name()
        url = "http://127.0.0.1:8010/api/redpost?name={}".format(name["name"])
        for time in range(name["times"]):
            urls.append(url)
    tasks = [post(url) for url in urls]
    loop.run_until_complete(asyncio.wait(tasks))