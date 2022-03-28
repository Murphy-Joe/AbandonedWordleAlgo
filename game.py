from copy import copy
import json
from datetime import date
import random
from words_filter import WordsFilter


class WordleGame:
    def __init__(self, target: str = None):
        self.all_targets = self.get_targets()
        self.target = target if target else self.all_targets[self.get_todays_target(
        )]
        self.results_filter = WordsFilter()
        self.guess_idx = 0
        self.solved = self.solved_check()

    def get_targets(self) -> list[str]:
        with open('words/targets.json', 'r') as targets_json:
            targets_list = json.load(targets_json)
        return targets_list

    def get_todays_target(self) -> str:
        beginning = date(year=2021, month=6, day=19)
        today = date.today()
        time_delta = today - beginning
        answers_idx = time_delta.days
        return answers_idx

    def get_random_target(self) -> str:
        return random.choice(self.all_targets)

    def set_random_target(self) -> str:
        self.target = self.get_random_target()
        return self.target

    def solved_check(self) -> bool:
        return len(self.results_filter.indexed_letters) >= 5 or self.guess_idx >= 6

    def update_results_filter(self, new_filter: WordsFilter) -> WordsFilter:
        self.results_filter.update_filter(new_filter)
        return self.results_filter

    def make_guess(self, guess: str) -> WordsFilter:
        excluded_letters, included_letters = [], []
        index_excludes_letters, indexed_letters = {}, {}

        temp_target = copy(self.target)

        for i, letter in enumerate(guess):
            if self.target == letter:
                indexed_letters[i] = letter
            elif letter in temp_target:
                temp_target = temp_target.replace(letter, '', 1)
                index_excludes_letters[i] = [letter]
                included_letters.append(letter)
            elif letter not in included_letters and letter not in indexed_letters.values():
                excluded_letters.append(letter)
        turn_filter = WordsFilter(
            excluded_letters, included_letters, index_excludes_letters, indexed_letters)
        self.update_results_filter(turn_filter)
        return turn_filter

    def end(self):
        pass


if __name__ == '__main__':
    wg = WordleGame('sunny')
    print(wg.target)
    wg.make_guess('audio')
    print(wg.results_filter.__dict__)
    # print(wg.results_filter.answers_that_meet_criteria(wg.all_targets))
