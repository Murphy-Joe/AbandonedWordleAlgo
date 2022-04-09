import asyncio
import json
import time
import aiohttp

async def call_param(session, param):
    url = f"https://1vv6d7.deta.dev/{param}"
    async with session.get(url) as response:
        print(f"Response: {response.json()} from {param}")


async def call_all_params(params):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for param in params:
            task = asyncio.ensure_future(call_param(session, param))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)

# game_post method extraction similar to call_param method goes here
# each game_post call will get the session and payload passed to it
# each game_call gets added as a task
# not sure what happens on gather to combine dicts

async def words_left_and_guess_words(guess_list: list[str]):
    async with aiohttp.ClientSession("https://1vv6d7.deta.dev") as session:
        async with session.post('/wordsleft', json={"guesses": guess_list}) as words_post:
            targets_left_and_best_guesses = await words_post.json()
            print(targets_left_and_best_guesses)
        async with session.post('/game', json={"guesses": guess_list, "next_guess": "whope"}) as game_post:
            guess_dict = await game_post.json()
            print(guess_dict)






""" async def main():
    # Schedule three calls *concurrently*:
    L = await asyncio.gather(
        factorial("A", 2),
        factorial("B", 3),
        factorial("C", 4),
    )
    print(L) """

if __name__ == "__main__":
    # params = ["hey", "there", "dude"] * 3

    """ start_time = time.time()
    asyncio.run(call_all_params(params))
    # asyncio.get_event_loop().run_until_complete(call_all_params(params))
    duration = time.time() - start_time
    print(f"Called {len(params)} params in {duration} seconds") """

    asyncio.run(words_left_and_guess_words(["scare"]))