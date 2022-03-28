from __future__ import annotations
from copy import copy


class WordsFilter:
    def __init__(self,
                 excluded_letters: set[str] = set(),
                 included_letters: list[str] = [],
                 index_excludes_letters: dict[int, list[str]] = {},
                 indexed_letters: dict[int, str] = {}):
        self.ExcludedLetters = excluded_letters
        self.IncludedLetters = included_letters
        self.IndexExcludesLetters = index_excludes_letters
        self.IndexedLetters = indexed_letters

    @staticmethod
    def get_new_filter(guess: str, target: str) -> WordsFilter:
        target_copy = copy(target)
        excluded_letters = set()
        included_letters = []
        index_excludes_letters, indexed_letters = {}, {}

        for i, letter in enumerate(guess):
            if target_copy[i] == letter:
                indexed_letters[i] = letter
            elif letter in target:
                target = target.replace(letter, '', 1)
                index_excludes_letters[i] = [letter]
                included_letters.append(letter)
            elif letter not in included_letters and letter not in indexed_letters.values():
                excluded_letters.add(letter)
        turn_filter = WordsFilter(
            excluded_letters, included_letters, index_excludes_letters, indexed_letters)
        return turn_filter

    @staticmethod
    def merge_filters(existing_filter: WordsFilter, new_filter: WordsFilter) -> WordsFilter:
        merged_filter = WordsFilter()
        # exluded letters
        merged_filter.ExcludedLetters = existing_filter.ExcludedLetters.union(
            new_filter.ExcludedLetters)

        # indexed letters
        merged_filter.IndexedLetters = existing_filter.IndexedLetters.copy()
        for k, v in new_filter.IndexedLetters.items():
            merged_filter.IndexedLetters.setdefault(k, v)

        # index excludes letters
        merged_filter.IndexExcludesLetters = existing_filter.IndexExcludesLetters.copy()
        for idx, letter_list in new_filter.IndexExcludesLetters.items():
            if idx in merged_filter.IndexExcludesLetters.keys() \
                    and letter_list[0] not in merged_filter.IndexExcludesLetters[idx]:
                merged_filter.IndexExcludesLetters[idx].extend(letter_list)
            else:
                merged_filter.IndexExcludesLetters[idx] = letter_list

        # included letters
        merged_filter.IncludedLetters = existing_filter.IncludedLetters.copy()
        for letter in new_filter.IncludedLetters:
            if letter in merged_filter.IncludedLetters:
                merged_filter.IncludedLetters.remove(letter)
        merged_filter.IncludedLetters.extend(new_filter.IncludedLetters)

        return merged_filter


if __name__ == '__main__':
    guess_filter1 = WordsFilter.get_new_filter('coast', 'sunny')
    print('\n1st guess \n', guess_filter1.__dict__)
    guess_filter2 = WordsFilter.get_new_filter('nanns', 'sunny')
    print('\n2nd guess \n', guess_filter2.__dict__)
    guess_filter_merged = WordsFilter.merge_filters(
        guess_filter1, guess_filter2)
    print('\nmerged filter \n', guess_filter_merged.__dict__)
