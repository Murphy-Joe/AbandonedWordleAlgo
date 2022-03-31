import json
from copy import deepcopy
from game import WordleGame
from words_filter import WordsFilter


with open('words/playable_words.json', 'r') as playable_words:
    guess_words_global = json.load(playable_words)


class Solver():
    def __init__(self, game: WordleGame):
        self.Game = deepcopy(game)

    # region sub-functions
    def matches_exact_letters(self, word: str) -> bool:
        matches_indexed_letters = False
        for index, letter in self.Game.ResultsFilter.IndexedLetters.items():
            if word[index] != letter:
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

    def narrowing_score(self, target, guess: str) -> int:
        temp_game = deepcopy(self.Game)
        new_filter = WordsFilter.get_new_filter(guess, target)
        merged_filter = WordsFilter.merge_filters(
            temp_game.ResultsFilter, new_filter)
        words_left = self.answers_that_meet_criteria(merged_filter)
        return len(words_left)
    # endregion

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

    def narrowing_scores(self, best_words: dict[str, int]) -> dict[str, int]:
        return_dict = {}
        targets = self.answers_that_meet_criteria(self.Game.ResultsFilter)
        best_words = [word.lower() for word in best_words]
        for tgt in targets:
            for guess in best_words:
                return_dict.setdefault(guess, 0)
                score = self.narrowing_score(tgt, guess) if guess != tgt else 0
                return_dict[guess] += score
        return return_dict


if __name__ == '__main__':
    with open('words/playable_words.json', 'r') as playable_words:
        guess_words = json.load(playable_words)

    wg = WordleGame()
    solver = Solver(wg)

    print(wg.Target)
    wg.make_guess('roate')
    print(f'\nfilter \n{wg.ResultsFilter.__dict__}')
    solver = Solver(wg)
    print(
        f'\nanswers left \n{solver.answers_that_meet_criteria(wg.ResultsFilter)}')

    wg.make_guess('noork')
    print(wg.ResultsFilter.__dict__)
    solver = Solver(wg)
    words_remaining = solver.answers_that_meet_criteria(wg.ResultsFilter)
    print(words_remaining)
