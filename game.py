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

    def merge_with_current_game_filter(self, new_filter: WordsFilter) -> WordsFilter:
        return WordsFilter.merge_filters(self.ResultsFilter, new_filter)

    def make_guess(self, guess: str) -> WordsFilter:
        self.Guesses.append(guess)
        if self.solved():
            self.end()
        new_filter = WordsFilter.get_new_filter(guess, self.Target)
        merged_filter = WordsFilter.merge_filters(
            self.ResultsFilter, new_filter)
        return merged_filter

    def end(self):
        pass


if __name__ == '__main__':
    wg = WordleGame('sunny')
    print(wg.Target)
    wg.make_guess('audio')
    wg.make_guess('video')
    print(wg.ResultsFilter.__dict__)
