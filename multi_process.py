import json
from words_filter import WordsFilter
from time import time
from multiprocessing import Pool
# from memory_profiler import profile

with open('targets.json', 'r') as targets_json:
    targets_list = json.load(targets_json)


def blank_filter() -> WordsFilter:
    return WordsFilter()


def matches_exact_letters(word: str, fltr: WordsFilter) -> bool:
    matches_indexed_letters = False
    for index, letter in fltr.IndexedLetters.items():
        if (word[index] != letter):
            matches_indexed_letters = False
            break
        else:
            matches_indexed_letters = True
    return matches_indexed_letters


def includes_included_letters(word: str, fltr: WordsFilter) -> bool:
    all_included_letters_accounted_for = False

    for letter in fltr.IncludedLetters:
        if letter not in word:
            all_included_letters_accounted_for = False
            break
        else:
            word = word.replace(letter, '', 1)
            all_included_letters_accounted_for = True
    return all_included_letters_accounted_for


def excludes_excluded_letters(word: str, fltr: WordsFilter) -> bool:
    excludes_correct_letters = not any(
        letter in word for letter in fltr.ExcludedLetters)
    return excludes_correct_letters


def letters_at_excluded_position(word: str, fltr: WordsFilter) -> bool:
    for index, letters in fltr.IndexExcludesLetters.items():
        if word[index] in letters:
            return True


def answers_that_meet_criteria(filtr: WordsFilter,  words: list[str] = None) -> list[str]:
    possible_answers = []
    if words is None:
        words = targets_list
    for word in words:
        if filtr.IndexedLetters and not matches_exact_letters(word, filtr):
            continue

        if filtr.IncludedLetters and not includes_included_letters(word, filtr):
            continue

        if filtr.ExcludedLetters and not excludes_excluded_letters(word, filtr):
            continue

        if filtr.IndexExcludesLetters and letters_at_excluded_position(word, filtr):
            continue

        possible_answers.append(word)
    return possible_answers


def narrowing_score(target, guess: str) -> int:
    new_filter = WordsFilter.get_new_filter(guess, target)
    merged_filter = WordsFilter.merge_filters(
        blank_filter(), new_filter)
    words_left = answers_that_meet_criteria(merged_filter)
    return len(words_left)


def narrowing_score_per_word(guess_list: list[str]) -> dict[str, int]:
    return_dict = {}
    targets = answers_that_meet_criteria(blank_filter())
    for tgt in targets:
        for guess in guess_list:
            return_dict.setdefault(guess, 0)
            score = narrowing_score(tgt, guess) if guess != tgt else 0
            return_dict[guess] += score
    return return_dict


def narrowing_score_per_word_multi_threaded(guess: str) -> dict[str, int]:
    return_dict = {}
    targets = answers_that_meet_criteria(blank_filter())
    for tgt in targets:
        return_dict.setdefault(guess, 0)
        score = narrowing_score(tgt, guess) if guess != tgt else 0
        return_dict[guess] += score
    return return_dict


# @profile
def run_multi():
    tops = ['oater', 'orate', 'roate', 'realo', 'irate', 'retia', 'terai', 'later', 'alter', 'alert', 'artel', 'ratel', 'taler', 'ariel', 'raile', 'arose', 'aeros', 'soare', 'stare', 'arets', 'aster', 'earst', 'rates', 'reast', 'resat',
            'stear', 'strae', 'tares', 'taser', 'tears', 'teras', 'arise', 'raise', 'aesir', 'reais', 'serai', 'arles', 'earls', 'laers', 'lares', 'laser', 'lears', 'rales', 'reals', 'seral', 'antre', 'earnt', 'raine', 'learn', 'renal', 'neral']

    with Pool() as p:
        result = p.map(narrowing_score_per_word_multi_threaded, tops[:1])

    combined_results = {}
    for r in result:
        combined_results.update(r)

    sorted_results = dict(
        sorted(combined_results.items(), key=lambda kv: kv[1]))

    return sorted_results


if __name__ == '__main__':

    with open('words/playable_words.json', 'r') as playable_words:
        guess_words = json.load(playable_words)

    answers = answers_that_meet_criteria(blank_filter())
    print(len(answers))

    t_start = time()
    print(run_multi())
    print(f"Multi-processor time taken: {time() - t_start}")
