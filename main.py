from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from game import WordleGame
from letter_middle import words_for_brute_force, letters_sorted_by_middleness
from coroutine_calls import runner
from solver import Solver

# pylint: disable=invalid-name
app = FastAPI()
origins = [
    "https://www.nytimes.com",
    "chrome-extension://*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

class Guesses(BaseModel):
    guesses: list[str]
    next_guess: Optional[str]

class TargetsLeftResponse(BaseModel):
    count: int
    targets: list[str]

def targets_left(guesses: list[str]) -> list[str]:
    guesses = [word for word in guesses if word]
    game = WordleGame()
    for guess in guesses:
        game.make_guess(guess)
    solver = Solver(game)
    return solver.answers_that_meet_criteria(game.ResultsFilter)

@app.post("/onecall")
async def onecall(body: Guesses):
    words_left = targets_left(body.guesses)
    return await runner(body.guesses, words_left)

@app.post("/bestletters")
async def best_letters(body: Guesses):
    words_left = targets_left(body.guesses)
    return letters_sorted_by_middleness(words_left)

@app.post("/targetsleft", response_model=TargetsLeftResponse)
async def wordsleft(body: Guesses) -> list[str]:
    targets = targets_left(body.guesses)
    return TargetsLeftResponse(count=len(targets), targets=targets[:30])

@app.post("/guessestorun")
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
