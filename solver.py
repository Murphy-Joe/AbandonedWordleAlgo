from game import WordleGame
from copy import deepcopy
from words_filter import WordsFilter
import json


class Solver():
    def __init__(self, game: WordleGame):
        self.Game = deepcopy(game)

    def matches_exact_letters(self, word: str) -> bool:
        matches_indexed_letters = False
        for index, letter in self.Game.ResultsFilter.IndexedLetters.items():
            if (word[index] != letter):
                matches_indexed_letters = False
                break
            else:
                matches_indexed_letters = True
        return matches_indexed_letters

    def includes_included_letters(self, word: str) -> bool:
        all_included_letters_accounted_for = False

        for letter in self.Game.ResultsFilter.IncludedLetters:
            if letter not in word:
                all_included_letters_accounted_for = False
                break
            else:
                word = word.replace(letter, '', 1)
                all_included_letters_accounted_for = True
        return all_included_letters_accounted_for

    def excludes_excluded_letters(self, word: str) -> bool:
        excludes_correct_letters = not any(
            letter in word for letter in self.Game.ResultsFilter.ExcludedLetters)
        return excludes_correct_letters

    def letters_at_excluded_position(self, word: str) -> bool:
        for index, letters in self.Game.ResultsFilter.IndexExcludesLetters.items():
            if word[index] in letters:
                return True

    def answers_that_meet_criteria(self, filtr: WordsFilter,  words: list[str] = None) -> list[str]:
        possible_answers = []
        if words is None:
            words = self.Game.AllTargets
        for word in words:
            if filtr.IndexedLetters and not self.matches_exact_letters(word):
                continue

            if filtr.IncludedLetters and not self.includes_included_letters(word):
                continue

            if filtr.ExcludedLetters and not self.excludes_excluded_letters(word):
                continue

            if filtr.IndexExcludesLetters and self.letters_at_excluded_position(word):
                continue

            possible_answers.append(word)
        return possible_answers

    def letters_left(self, words_left: list[str]) -> set[str]:
        new_words_left = []
        letters_guessed = wg.ResultsFilter.IncludedLetters + \
            list(wg.ResultsFilter.IndexedLetters.values())
        for word in words_left:
            for ltr in letters_guessed:
                if ltr in word:
                    word = word.replace(ltr, '', 1)
            new_words_left.append(word)

        return set(''.join(new_words_left))

    def narrow_guesses_from_words_left(self, words_left):
        ltrs = self.letters_left(words_left)
        playable_guesses = [
            word for word in guess_words if any(ltr in ltrs for ltr in word)]
        return playable_guesses

    def narrowing_score(self, target, guess: str) -> int:
        temp_game = deepcopy(self.Game)
        new_filter = WordsFilter.get_new_filter(guess, target)
        merged_filter = WordsFilter.merge_filters(
            temp_game.ResultsFilter, new_filter)
        words_left = self.answers_that_meet_criteria(merged_filter)
        return len(words_left)

    def narrowing_score_per_word(self, guess_list: list[str]) -> dict[str, int]:
        return_dict = {}
        targets = self.answers_that_meet_criteria(self.Game.ResultsFilter)
        for tgt in targets:
            for guess in guess_list:
                return_dict.setdefault(guess, 0)
                score = self.narrowing_score(tgt, guess) if guess != tgt else 0
                return_dict[guess] += score
        return return_dict


if __name__ == '__main__':
    with open('words/playable_words.json', 'r') as playable_words:
        guess_words = json.load(playable_words)

    wg = WordleGame('sunny')
    print(wg.Target)
    wg.make_guess('audio')
    print(wg.ResultsFilter.__dict__)
    wg.make_guess('noork')
    print(wg.ResultsFilter.__dict__)

    solver = Solver(wg)
    words_left = solver.answers_that_meet_criteria(wg.ResultsFilter)
    print(words_left)
    print(solver.letters_left(words_left))
    print(len(solver.narrow_guesses_from_words_left(words_left)))
    # print(solver.narrowing_score_per_word(guess_words[2000:2050]))
