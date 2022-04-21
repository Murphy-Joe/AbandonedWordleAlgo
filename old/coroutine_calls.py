import asyncio
import time
import aiohttp


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
        if (len(resp_targets_and_guesses["wordsLeft"]) == 1
        and resp_targets_and_guesses["wordsLeft"][0] == guess_list[-1]):
            print(f'You won in {len(guess_list)} guesses!')
        tasks = []
        for next_guess in resp_targets_and_guesses["bestGuessWords"]:
            task = asyncio.create_task(guess_score(guess_list, session, next_guess))
            tasks.append(task)
        res = await asyncio.gather(*tasks, return_exceptions=True)
        # res.sort(key=lambda tup: tup[1])
        return res

if __name__ == "__main__":

    start_time = time.time()
    results = asyncio.run(runner(["crane"]))
    duration = time.time() - start_time
    avgNarrowingScore = sum([r["narrowing_scores"] for r in results]) / len(results)
    print(f"\nheavy narrowing score loop took {avgNarrowingScore} seconds")

    print(f"\nCalled in {duration} seconds")
