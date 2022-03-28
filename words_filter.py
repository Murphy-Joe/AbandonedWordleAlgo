from __future__ import annotations


class WordsFilter:
    def __init__(self, excluded_letters=[], included_letters=[], index_excludes_letters={}, indexed_letters={}):
        self.excluded_letters = excluded_letters
        self.included_letters = included_letters
        self.index_excludes_letters = index_excludes_letters
        self.indexed_letters = indexed_letters

    def matches_exact_letters(self, word: str) -> bool:
        matches_indexed_letters = False
        for index, letter in self.indexed_letters.items():
            if (word[index] != letter):
                matches_indexed_letters = False
                break
            else:
                matches_indexed_letters = True
        return matches_indexed_letters

    def includes_included_letters(self, word: str) -> bool:
        all_included_letters_accounted_for = False

        for letter in self.included_letters:
            if letter not in word:
                all_included_letters_accounted_for = False
                break
            else:
                word = word.replace(letter, '', 1)
                all_included_letters_accounted_for = True
        return all_included_letters_accounted_for

    def excludes_excluded_letters(self, word: str) -> bool:
        excludes_correct_letters = not any(
            letter in word for letter in self.excluded_letters)
        return excludes_correct_letters

    def letters_at_excluded_position(self, word: str) -> bool:
        for index, letters in self.index_excludes_letters.items():
            if word[index] in letters:
                return True

    def answers_that_meet_criteria(self, words: list[str]) -> list[str]:
        possible_answers = []
        for word in words:
            if self.indexed_letters and not self.matches_exact_letters(word):
                continue

            if self.included_letters and not self.includes_included_letters(word):
                continue

            if self.excluded_letters and not self.excludes_excluded_letters(word):
                continue

            if self.index_excludes_letters and self.letters_at_excluded_position(word):
                continue

            possible_answers.append(word)
        return possible_answers

    def update_filter(self, new_filter: WordsFilter) -> WordsFilter:

        # exluded letters
        self.excluded_letters.extend(new_filter.excluded_letters)

        # indexed letters
        for k, v in new_filter.indexed_letters.items():
            self.indexed_letters.setdefault(k, v)

        # index excludes letters
        for idx, letter_list in new_filter.index_excludes_letters.items():
            if idx in self.index_excludes_letters.keys() \
                    and letter_list[0] not in self.index_excludes_letters[idx]:
                self.index_excludes_letters[idx].extend(letter_list)
            else:
                self.index_excludes_letters[idx] = letter_list

        # included letters
        for letter in new_filter.included_letters:
            if letter in self.included_letters:
                self.included_letters.remove(letter)
        self.included_letters.extend(new_filter.included_letters)

        return self


if __name__ == '__main__':
    import json

    with open('words/playable_words.json', 'r') as five_letter_words_json:
        playable_words = json.load(five_letter_words_json)

    with open('words/targets.json', 'r') as answers_json:
        answers = json.load(answers_json)

    wf = WordsFilter('coastlier', 'n', {2: 'n'})
    words_to_guess = wf.answers_that_meet_criteria(answers)
    print(words_to_guess)
