import asyncio
import json
import time
from typing import Optional

from fastapi import FastAPI, Query
from pydantic import BaseModel

from game import WordleGame
from letter_middle import words_for_brute_force, letters_sorted_by_middleness
from coroutine_calls import runner
from solver import Solver

# pylint: disable=invalid-name
app = FastAPI()

class Guesses(BaseModel):
    guesses: list[str]
    next_guess: Optional[str]

class AllInOneResponse(BaseModel):
    targets_left_len: int
    best_letters_dict: dict[str, int]
    best_guess_w_score_tup: tuple[str, int]

def targets_left(guesses: list[str]) -> list[str]:
    game = WordleGame()
    for guess in guesses:
        game.make_guess(guess)
    solver = Solver(game)
    return solver.answers_that_meet_criteria(game.ResultsFilter)

@app.post("/onecall", response_model=AllInOneResponse)
async def onecall(body: Guesses):
    return await runner(body.guesses)

@app.post("/bestletters")
async def best_letters(body: Guesses):
    words_left = targets_left(body.guesses)
    return letters_sorted_by_middleness(words_left)

@app.post("/targetsleft")
async def wordsleft(body: Guesses) -> list[str]:
    return targets_left(body.guesses)

@app.post("/bestguesses")
async def best_guesses(body: Guesses) -> list[str]:
    wordsLeft = targets_left(body.guesses)
    return words_for_brute_force(wordsLeft)


@app.post("/game")
async def single_guess_dict(body: Guesses):
    words_left = targets_left(body.guesses)
    return Solver().narrowing_score_per_guess_async(body.next_guess, words_left)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

    # uvicorn main:app --reload

    #region old code
    # synchronous version
    # @app.get("/nextguesses")
    # async def get_guess_dict(guesses: str = Query(str), nextguess: str = Query(str)):
    #     guesses = guesses.split(',')
    #     game = WordleGame()
    #     for guess in guesses:
    #         game.make_guess(guess)
    #     game.make_guess(nextguess)
    #     solver = Solver(game)
    #     wordsLeft = solver.answers_that_meet_criteria(game.ResultsFilter)
    #     guessDict = solver.narrowing_score_per_guess_async(nextguess, wordsLeft)
    #     return {
    #         "data": guessDict
    #     }
    # endregion
