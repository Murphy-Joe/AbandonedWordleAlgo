# pylint: disable=wrong-import-position
# pylint: disable=import-error
import json
import os
import random
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from solver import Solver
from letter_middle import best_guess
from game import WordleGame


# sys.path.insert(0, '..')

with open('words/targets.json', 'r') as answers_json:
    answers = json.load(answers_json)

starting_word = 'roate'

cnt = 0
while cnt < 2:
    cnt += 1
    random_target = random.choice(answers)
    game = WordleGame(answers[cnt])
    game.make_guess(starting_word)

    while game.Target != game.Guesses[-1]:
        remaining_answers = Solver(
            game).answers_that_meet_criteria(game.ResultsFilter)
        next_guess = best_guess(game)
        game.make_guess(next_guess)

    with open(f'outcomes/{starting_word}3.json', 'r') as file_read:
        file_obj = json.load(file_read)
        file_obj.update({game.Target: len(game.Guesses)})

    with open(f'outcomes/{starting_word}3.json', 'w') as file_write:
        json.dump(file_obj, file_write)
