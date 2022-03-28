from words_filter import WordsFilter


def merge_filters(existing_filter: WordsFilter, new_filter: WordsFilter) -> WordsFilter:

    # exluded letters
    existing_filter.ExcludedLetters.extend(new_filter.ExcludedLetters)

    # indexed letters
    for k, v in new_filter.IndexedLetters.items():
        existing_filter.IndexedLetters.setdefault(k, v)

    # index excludes letters
    for idx, letter_list in new_filter.IndexExcludesLetters.items():
        if idx in existing_filter.IndexExcludesLetters.keys():
            existing_filter.IndexExcludesLetters[idx].extend(letter_list)
        else:
            existing_filter.IndexExcludesLetters[idx] = letter_list

    # included letters
    for letter in new_filter.IncludedLetters:
        if letter in existing_filter.IncludedLetters:
            existing_filter.IncludedLetters.remove(letter)
    existing_filter.IncludedLetters.extend(new_filter.IncludedLetters)

    return existing_filter


if __name__ == '__main__':
    existing_filter_test = WordsFilter()
    existing_filter_test.IncludedLetters = ['a', 'c']
    existing_filter_test.ExcludedLetters = ['d', 'f', 'z']
    existing_filter_test.IndexExcludesLetters = {
        0: ['c'],
    }
    existing_filter_test.IndexedLetters = {
        2: 'a'
    }

    new_filter_test = WordsFilter()
    new_filter_test.IncludedLetters = ['r', 's', 'c']
    new_filter_test.ExcludedLetters = ['u', 'q']
    new_filter_test.IndexExcludesLetters = {
        0: ['r'], 1: ['s'], 4: ['c']
    }
    new_filter_test.IndexedLetters = {
    }

    merged_filter_test = merge_filters(existing_filter_test, new_filter_test)
    print(merged_filter_test.__dict__)
