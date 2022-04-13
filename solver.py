import json
from copy import deepcopy
import time
from game import WordleGame
from words_filter import WordsFilter


with open('words/playable_words.json', 'r') as playable_words:
    guess_words_global = json.load(playable_words)


class Solver():
    def __init__(self, game: WordleGame):
        self.Game = deepcopy(game)

    # region filter criteria sub-functions
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

    def play_fake_guess(self, target: str, guess: str, filtered_answers: list[str]) -> int:
        new_game = WordleGame(target)
        new_game.make_guess(guess)
        new_solver = Solver(new_game)
        words_left = new_solver.answers_that_meet_criteria(
            new_game.ResultsFilter, filtered_answers)
        return len(words_left)

    def narrowing_scores(self, best_words: list[str], targets_left: list[str]) -> list[tuple[str, int]]:
        collect_guess_scores = []
        best_words = [word.lower() for word in best_words]
        for guess in best_words:
            guess_score = self.narrowing_score_per_guess_async(guess, targets_left)
            collect_guess_scores.append(guess_score)
        return collect_guess_scores

    def narrowing_score_per_guess_async(self, guess_word: str, targets_left: list[str]) -> tuple[str, int]:
        guess_word = guess_word.lower()
        score = 0
        start_time = time.time()
        for tgt in targets_left:
            if guess_word == tgt:
                continue
            else:
                score += self.play_fake_guess(tgt, guess_word, targets_left)
        end_time = time.time()
        print(guess_word, end_time - start_time)
        return (guess_word, score/len(targets_left))


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
