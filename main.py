from time import sleep
from game import WordleGame
from solver import Solver
from letter_middle import best_guess, words_for_brute_force
from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/wordsleft")
async def root(guesses: str = Query(str)):
    guesses = guesses.split(',')
    game = WordleGame()
    for guess in guesses:
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
    sleep(1)
    return {
        "item": item
    }


app.get("bestguess/{params}")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

    # uvicorn main:app --reload
