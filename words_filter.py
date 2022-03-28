from __future__ import annotations


class WordsFilter:
    def __init__(self,
                 excluded_letters: list[str] = [],
                 included_letters: list[str] = [],
                 index_excludes_letters: dict[int, list[str]] = {},
                 indexed_letters: dict[int, str] = {}):
        self.excluded_letters = excluded_letters
        self.included_letters = included_letters
        self.index_excludes_letters = index_excludes_letters
        self.indexed_letters = indexed_letters

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
    wf = WordsFilter('coastlier', 'n', {2: 'n'})
    print(wf.__dict__)
