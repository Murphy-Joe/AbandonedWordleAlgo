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
            task = asyncio.create_task(call_param(session, param))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)

# game_post method extraction similar to call_param method goes here
# each game_post call will get the session and payload passed to it
# each game_call gets added as a task
# not sure what happens on gather to combine dicts

async def targets_and_guesses(guess_list, session):
    payload = {"guesses": guess_list}
    async with session.post('/wordsleft', json=payload) as words_post:
        return await words_post.json()
        # print(targets_left_and_best_guesses)

async def guess_score(guess_list, session, next_guess):
    payload = {"guesses": guess_list, "next_guess": next_guess}
    async with session.post('/game', json=payload) as game_post:
        return await game_post.json()
        # print(guess_dict)

async def runner(guess_list: list[str]):
    async with aiohttp.ClientSession("https://1vv6d7.deta.dev") as session:
        resp_targets_and_guesses = await targets_and_guesses(guess_list, session)
        print(f'\nnumber of guesses to check: {len(resp_targets_and_guesses["bestGuessWords"])}')
        print(f'number of targets left: {len(resp_targets_and_guesses["wordsLeft"])}')
        if len(resp_targets_and_guesses["wordsLeft"]) == 1 and resp_targets_and_guesses["wordsLeft"][0] == guess_list[-1]:
            print(f'You won in {len(guess_list)} guesses!')
        tasks = []
        for next_guess in resp_targets_and_guesses["bestGuessWords"]:
            task = asyncio.create_task(guess_score(guess_list, session, next_guess))
            tasks.append(task)
        res = await asyncio.gather(*tasks, return_exceptions=True)
        res.sort(key=lambda x: x[1])
        return res[0]



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

    start_time = time.time()
    print(asyncio.run(runner(["czzzz"])))
    duration = time.time() - start_time
    print(f"Called in {duration} seconds")