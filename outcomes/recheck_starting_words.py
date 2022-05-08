import json
import os
import random
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from solver import Solver
from letter_middle import words_sorted_by_middleness_w_upper
from game import WordleGame

with open('words/targets.json', 'r') as answers_json:
    answers = json.load(answers_json)

with open('words/playable_words.json', 'r') as playable_json:
    playable_words = json.load(playable_json)

starting_word = 'soare'

def targets_left(ans: str, guesses: list[str]) -> list[str]:
    guesses = [word for word in guesses if word]
    game = WordleGame(ans)
    for guess in guesses:
        game.make_guess(guess)
    solver = Solver(game)
    return solver.answers_that_meet_criteria(game.ResultsFilter)

# targets_left_list = []
# for answer in answers:
#     targets_left_list.append(len(targets_left(answer, starting_word)))
# print(f'\n{starting_word} avg words left: {(sum(targets_left_list))/len(targets_left_list)}')

starting_words_tups = []
word_scores = words_sorted_by_middleness_w_upper(answers,playable_words)
best_words = [word[0] for word in word_scores]
for word in best_words[:50]:
    targets_left_list = []
    for answer in answers:
        targets_left_list.append(len(targets_left(answer, [word])))
    starting_words_tups.append((word, (sum(targets_left_list))/len(targets_left_list)))
    # print(f'{word} avg words left: {(sum(targets_left_list))/len(targets_left_list)}')
starting_words_tups.sort(key=lambda x: x[1])
for x in starting_words_tups:
    print(x)