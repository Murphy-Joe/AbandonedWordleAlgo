from game import WordleGame
from words_filter import WordsFilter
import json


class Solver(WordleGame):
    def __init__(self, target: str = None, results_filter: WordsFilter = None):
        WordleGame.__init__(self, target, results_filter)

    def matches_exact_letters(self, word: str) -> bool:
        matches_indexed_letters = False
        for index, letter in self.ResultsFilter.IndexedLetters.items():
            if (word[index] != letter):
                matches_indexed_letters = False
                break
            else:
                matches_indexed_letters = True
        return matches_indexed_letters

    def includes_included_letters(self, word: str) -> bool:
        all_included_letters_accounted_for = False

        for letter in self.ResultsFilter.IncludedLetters:
            if letter not in word:
                all_included_letters_accounted_for = False
                break
            else:
                word = word.replace(letter, '', 1)
                all_included_letters_accounted_for = True
        return all_included_letters_accounted_for

    def excludes_excluded_letters(self, word: str) -> bool:
        excludes_correct_letters = not any(
            letter in word for letter in self.ResultsFilter.ExcludedLetters)
        return excludes_correct_letters

    def letters_at_excluded_position(self, word: str) -> bool:
        for index, letters in self.ResultsFilter.IndexExcludesLetters.items():
            if word[index] in letters:
                return True

    def answers_that_meet_criteria(self, words: list[str] = None) -> list[str]:
        possible_answers = []
        if words is None:
            words = self.AllTargets
        for word in words:
            if self.ResultsFilter.IndexedLetters and not self.matches_exact_letters(word):
                continue

            if self.ResultsFilter.IncludedLetters and not self.includes_included_letters(word):
                continue

            if self.ResultsFilter.ExcludedLetters and not self.excludes_excluded_letters(word):
                continue

            if self.ResultsFilter.IndexExcludesLetters and self.letters_at_excluded_position(word):
                continue

            possible_answers.append(word)
        return possible_answers

    def narrowing_score(self, target, guess: str) -> int:
        temp_game = WordleGame(target, self.ResultsFilter)
        temp_game.make_guess(guess)
        words_left = self.answers_that_meet_criteria()
        return len(words_left)

    def narrowing_score_per_word(self, guess_list: list[str]) -> dict[str, int]:
        return_dict = {}
        for tgt in self.answers_that_meet_criteria():
            for guess in guess_list:
                return_dict.setdefault(guess, 0)
                score = self.narrowing_score(tgt, guess)
                return_dict[guess] += score
        return return_dict


if __name__ == '__main__':
    with open('words/playable_words.json', 'r') as playable_words:
        guess_words = json.load(playable_words)

    solver = Solver('found')
    print(solver.Target)
    solver.make_guess('audio')
    print(solver.ResultsFilter.__dict__)
    print(solver.answers_that_meet_criteria())
    print(solver.narrowing_score_per_word(guess_words))
