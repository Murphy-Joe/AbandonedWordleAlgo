from words_filter import WordsFilter


def merge_filters(existing_filter: WordsFilter, new_filter: WordsFilter) -> WordsFilter:

    # exluded letters
    existing_filter.excluded_letters.extend(new_filter.excluded_letters)

    # indexed letters
    for k, v in new_filter.indexed_letters.items():
        existing_filter.indexed_letters.setdefault(k, v)

    # index excludes letters
    for idx, letter_list in new_filter.index_excludes_letters.items():
        if idx in existing_filter.index_excludes_letters.keys():
            existing_filter.index_excludes_letters[idx].extend(letter_list)
        else:
            existing_filter.index_excludes_letters[idx] = letter_list

    # included letters
    for letter in new_filter.included_letters:
        if letter in existing_filter.included_letters:
            existing_filter.included_letters.remove(letter)
    existing_filter.included_letters.extend(new_filter.included_letters)

    return existing_filter


if __name__ == '__main__':
    existing_filter_test = WordsFilter()
    existing_filter_test.included_letters = ['a', 'c']
    existing_filter_test.excluded_letters = ['d', 'f', 'z']
    existing_filter_test.index_excludes_letters = {
        0: ['c'],
    }
    existing_filter_test.indexed_letters = {
        2: 'a'
    }

    new_filter_test = WordsFilter()
    new_filter_test.included_letters = ['r', 's', 'c']
    new_filter_test.excluded_letters = ['u', 'q']
    new_filter_test.index_excludes_letters = {
        0: ['r'], 1: ['s'], 4: ['c']
    }
    new_filter_test.indexed_letters = {
    }

    merged_filter_test = merge_filters(existing_filter_test, new_filter_test)
    print(merged_filter_test.__dict__)
