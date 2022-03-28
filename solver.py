from game import WordleGame


class Solver(WordleGame):
    def __init__(self, target: str = None):
        WordleGame.__init__(self, target)

    def matches_exact_letters(self, word: str) -> bool:
        matches_indexed_letters = False
        for index, letter in self.results_filter.indexed_letters.items():
            if (word[index] != letter):
                matches_indexed_letters = False
                break
            else:
                matches_indexed_letters = True
        return matches_indexed_letters

    def includes_included_letters(self, word: str) -> bool:
        all_included_letters_accounted_for = False

        for letter in self.results_filter.included_letters:
            if letter not in word:
                all_included_letters_accounted_for = False
                break
            else:
                word = word.replace(letter, '', 1)
                all_included_letters_accounted_for = True
        return all_included_letters_accounted_for

    def excludes_excluded_letters(self, word: str) -> bool:
        excludes_correct_letters = not any(
            letter in word for letter in self.results_filter.excluded_letters)
        return excludes_correct_letters

    def letters_at_excluded_position(self, word: str) -> bool:
        for index, letters in self.results_filter.index_excludes_letters.items():
            if word[index] in letters:
                return True

    def answers_that_meet_criteria(self, words: list[str]) -> list[str]:
        possible_answers = []
        for word in words:
            if self.results_filter.indexed_letters and not self.matches_exact_letters(word):
                continue

            if self.results_filter.included_letters and not self.includes_included_letters(word):
                continue

            if self.results_filter.excluded_letters and not self.excludes_excluded_letters(word):
                continue

            if self.results_filter.index_excludes_letters and self.letters_at_excluded_position(word):
                continue

            possible_answers.append(word)
        return possible_answers


if __name__ == '__main__':
    solver = Solver('found')
    print(solver.target)
    solver.make_guess('audio')
    print(solver.results_filter.__dict__)
    print(solver.results_filter.answers_that_meet_criteria(solver.all_targets))
