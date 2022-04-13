import asyncio
import json
import time
from typing import Optional

from fastapi import FastAPI, Query
from pydantic import BaseModel

from game import WordleGame
from letter_middle import words_for_brute_force
from solver import Solver

# pylint: disable=invalid-name
app = FastAPI()

class Guesses(BaseModel):
    guesses: list[str]
    next_guess: Optional[str]

@app.post("/wordsleft")
async def root(body: Guesses):
    game = WordleGame()
    for guess in body.guesses:
        game.make_guess(guess)
    solver = Solver(game)
    wordsLeft = solver.answers_that_meet_criteria(game.ResultsFilter)
    bestGuessWords = words_for_brute_force(game)
    return {
        "wordsLeft": wordsLeft,
        "bestGuessWords": bestGuessWords,
    }

@app.get("/nextguesses")
async def get_guess_dict(guesses: str = Query(str), nextguess: str = Query(str)):
    guesses = guesses.split(',')
    game = WordleGame()
    for guess in guesses:
        game.make_guess(guess)
    game.make_guess(nextguess)
    solver = Solver(game)
    wordsLeft = solver.answers_that_meet_criteria(game.ResultsFilter)
    guessDict = solver.narrowing_score_per_guess_async(nextguess, wordsLeft)
    return {
        "data": guessDict
    }

# @app.get("/{item}")
# async def test(item: str):
#     await asyncio.sleep(1)
#     return {
#         "item": item
#     }

@app.post("/game")
async def single_guess_dict(body: Guesses):
    create_game = time.time()
    game = WordleGame()
    end_create_game = time.time()

    make_guess = time.time()
    for guess in body.guesses:
        game.make_guess(guess)
    end_make_guess = time.time()

    create_solver = time.time()
    solver = Solver(game)
    end_create_solver = time.time()

    words_left_time = time.time()
    words_left = solver.answers_that_meet_criteria(game.ResultsFilter)
    end_words_left = time.time()

    narrowing_scores = time.time()
    guess_dict = solver.narrowing_score_per_guess_async(body.next_guess, words_left)
    end_narrowing_scores = time.time()

    # return {"create_game": end_create_game - create_game, "make_guess": end_make_guess - make_guess, "create_solver": end_create_solver - create_solver, "words_left": end_words_left - words_left_time, "narrowing_scores": end_narrowing_scores - narrowing_scores, "guess_dict": guess_dict}
    return guess_dict

@app.get("/jsontime")
async def time_to_load_json():
    start_time = time.time()
    with open('words/targets.json', 'r') as answers_json:
        answers = json.load(answers_json)
    return time.time() - start_time

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

    # uvicorn main:app --reload
