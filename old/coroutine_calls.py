import asyncio
import time
import aiohttp

async def call_param(session, param):
    url = f"https://1vv6d7.deta.dev/{param}"
    async with session.get(url) as response:
        print(f"Response: {response.content} from {param}")


async def call_all_params(params):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for param in params:
            task = asyncio.ensure_future(call_param(session, param))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)


""" async def main():
    # Schedule three calls *concurrently*:
    L = await asyncio.gather(
        factorial("A", 2),
        factorial("B", 3),
        factorial("C", 4),
    )
    print(L) """

if __name__ == "__main__":
    params = ["hey", "there", "dude"] * 3

    start_time = time.time()
    asyncio.run(call_all_params(params))
    # asyncio.get_event_loop().run_until_complete(call_all_params(params))
    duration = time.time() - start_time
    print(f"Called {len(params)} params in {duration} seconds")