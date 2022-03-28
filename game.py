import json
from datetime import date
import random
from words_filter import WordsFilter
from copy import copy


class WordleGame:
    def __init__(self, target: str = None, results_filter: WordsFilter = None):
        self.AllTargets: list[str] = self.get_targets()
        self.Target: str = target if target else self.AllTargets[self.get_todays_target(
        )]
        self.ResultsFilter: WordsFilter = results_filter if results_filter else WordsFilter()
        self.Guesses: list[str] = []

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
        return random.choice(self.AllTargets)

    def set_random_target(self) -> str:
        self.Target = self.get_random_target()
        return self.Target

    def solved(self) -> bool:
        return self.Guesses[-1] == self.Target

    def get_new_filter(self, guess: str) -> WordsFilter:
        excluded_letters, included_letters = [], []
        index_excludes_letters, indexed_letters = {}, {}
        temp_target = copy(self.Target)

        for i, letter in enumerate(guess):
            if self.Target == letter:
                indexed_letters[i] = letter
            elif letter in temp_target:
                temp_target = temp_target.replace(letter, '', 1)
                index_excludes_letters[i] = [letter]
                included_letters.append(letter)
            elif letter not in included_letters and letter not in indexed_letters.values():
                excluded_letters.append(letter)
        turn_filter = WordsFilter(
            excluded_letters, included_letters, index_excludes_letters, indexed_letters)
        return turn_filter

    def update_results_filter(self, new_filter: WordsFilter) -> WordsFilter:
        self.ResultsFilter.update_filter(new_filter)
        return self.ResultsFilter

    def make_guess(self, guess: str) -> WordsFilter:
        self.Guesses.append(guess)
        if self.solved():
            self.end()
        new_filter = self.get_new_filter(guess)
        updated_filter = self.update_results_filter(new_filter)
        return updated_filter

    def end(self):
        pass


if __name__ == '__main__':
    wg = WordleGame('sunny')
    print(wg.Target)
    wg.make_guess('audio')
    print(wg.ResultsFilter.__dict__)
    # print(wg.results_filter.answers_that_meet_criteria(wg.all_targets))
