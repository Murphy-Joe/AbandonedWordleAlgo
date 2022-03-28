from __future__ import annotations


class WordsFilter:
    def __init__(self,
                 excluded_letters: list[str] = [],
                 included_letters: list[str] = [],
                 index_excludes_letters: dict[int, list[str]] = {},
                 indexed_letters: dict[int, str] = {}):
        self.ExcludedLetters = excluded_letters
        self.IncludedLetters = included_letters
        self.IndexExcludesLetters = index_excludes_letters
        self.IndexedLetters = indexed_letters

    def get_new_filter(self, guess: str, target: str) -> WordsFilter:
        excluded_letters, included_letters = [], []
        index_excludes_letters, indexed_letters = {}, {}

        for i, letter in enumerate(guess):
            if target == letter:
                indexed_letters[i] = letter
            elif letter in target:
                target = target.replace(letter, '', 1)
                index_excludes_letters[i] = [letter]
                included_letters.append(letter)
            elif letter not in included_letters and letter not in indexed_letters.values():
                excluded_letters.append(letter)
        turn_filter = WordsFilter(
            excluded_letters, included_letters, index_excludes_letters, indexed_letters)
        return turn_filter

    def update_filter(self, new_filter: WordsFilter) -> WordsFilter:

        # exluded letters
        self.ExcludedLetters.extend(new_filter.ExcludedLetters)

        # indexed letters
        for k, v in new_filter.IndexedLetters.items():
            self.IndexedLetters.setdefault(k, v)

        # index excludes letters
        for idx, letter_list in new_filter.IndexExcludesLetters.items():
            if idx in self.IndexExcludesLetters.keys() \
                    and letter_list[0] not in self.IndexExcludesLetters[idx]:
                self.IndexExcludesLetters[idx].extend(letter_list)
            else:
                self.IndexExcludesLetters[idx] = letter_list

        # included letters
        for letter in new_filter.IncludedLetters:
            if letter in self.IncludedLetters:
                self.IncludedLetters.remove(letter)
        self.IncludedLetters.extend(new_filter.IncludedLetters)

        return self


if __name__ == '__main__':
    wf1 = WordsFilter()
    wf2 = WordsFilter()
    guess_filter1 = wf1.get_new_filter('coast', 'sunny')
    print(guess_filter1.__dict__)
    guess_filter2 = wf1.get_new_filter('nanns', 'sunny')
    guess_filter1.update_filter(guess_filter2)
    print(guess_filter1.__dict__)
