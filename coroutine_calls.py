import asyncio
import time
import aiohttp

from letter_middle import choose_best_guess

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

async def runner1(guess_list: list[str]):
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
        # want
        # targets left (and len)
        # best overall guess (and score)
        # best guess from targets (and score)
        # maybe best letters
        res.sort(key=lambda tup: tup[1])
        return res

async def targets_left(guess_list, session) -> list[str]:
    payload = {"guesses": guess_list}
    async with session.post('/targetsleft', json=payload) as targets_left_post:
        return await targets_left_post.json()

async def best_guesses(guess_list: list[str], session) -> list[str]:
    payload = {"guesses": guess_list}
    async with session.post('/bestguesses', json=payload) as best_guesses_post:
        return await best_guesses_post.json()

async def best_letters(guess_list: list[str], session) -> dict[str, int]:
    payload = {"guesses": guess_list}
    async with session.post('/bestletters', json=payload) as best_letters_post:
        return await best_letters_post.json()

async def runner(guess_list: list[str], words_left: list[str]) -> list[tuple[str, int]]:
    async with aiohttp.ClientSession("https://1vv6d7.deta.dev") as session:
        resp_best_guesses = await best_guesses(guess_list, session)
        
        tasks = []
        for next_guess in resp_best_guesses:
            task = asyncio.create_task(guess_score(guess_list, session, next_guess))
            tasks.append(task)
        res = await asyncio.gather(*tasks, return_exceptions=True)

        res.sort(key=lambda tup: tup[1])
        best_guess = choose_best_guess(res, words_left)
        res.remove(best_guess)
        res.insert(0, best_guess)

        return res

if __name__ == "__main__":
    from game import WordleGame
    from solver import Solver

    guesses = ["basks", "tench"]

    game = WordleGame()
    for guess in guesses:
        game.make_guess(guess)
    solver = Solver(game)
    word_left_param = solver.answers_that_meet_criteria(game.ResultsFilter)

    start_time = time.time()
    results = asyncio.run(runner(guesses, word_left_param))
    duration = time.time() - start_time
    # avgNarrowingScore = sum([r["narrowing_scores"] for r in results]) / len(results)
    # print(f"\nheavy narrowing score loop took {avgNarrowingScore} seconds")
    print(results)

    print(f"\nCalled in {duration} seconds")
