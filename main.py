import asyncio
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

@app.get("/{item}")
async def test(item: str):
    await asyncio.sleep(1)
    return {
        "item": item
    }

@app.post("/game")
async def single_guess_dict(body: Guesses):
    game = WordleGame()
    for guess in body.guesses:
        game.make_guess(guess)
    solver = Solver(game)
    words_left = solver.answers_that_meet_criteria(game.ResultsFilter)
    guess_dict = solver.narrowing_score_per_guess_async(body.next_guess, words_left)
    return guess_dict

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

    # uvicorn main:app --reload
