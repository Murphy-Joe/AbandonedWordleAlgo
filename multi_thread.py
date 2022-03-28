import json
from game import WordleGame
from words_filter import WordsFilter
from time import time
from concurrent.futures import ThreadPoolExecutor

with open('words/targets.json', 'r') as targets_json:
    targets_list = json.load(targets_json)


def blank_filter() -> WordsFilter:
    return WordsFilter()


def matches_exact_letters(word: str) -> bool:
    matches_indexed_letters = False
    for index, letter in blank_filter().IndexedLetters.items():
        if (word[index] != letter):
            matches_indexed_letters = False
            break
        else:
            matches_indexed_letters = True
    return matches_indexed_letters


def includes_included_letters(word: str) -> bool:
    all_included_letters_accounted_for = False

    for letter in blank_filter().IncludedLetters:
        if letter not in word:
            all_included_letters_accounted_for = False
            break
        else:
            word = word.replace(letter, '', 1)
            all_included_letters_accounted_for = True
    return all_included_letters_accounted_for


def excludes_excluded_letters(word: str) -> bool:
    excludes_correct_letters = not any(
        letter in word for letter in blank_filter().ExcludedLetters)
    return excludes_correct_letters


def letters_at_excluded_position(word: str) -> bool:
    for index, letters in blank_filter().IndexExcludesLetters.items():
        if word[index] in letters:
            return True


def answers_that_meet_criteria(filtr: WordsFilter,  words: list[str] = None) -> list[str]:
    possible_answers = []
    if words is None:
        words = targets_list
    for word in words:
        if filtr.IndexedLetters and not matches_exact_letters(word):
            continue

        if filtr.IncludedLetters and not includes_included_letters(word):
            continue

        if filtr.ExcludedLetters and not excludes_excluded_letters(word):
            continue

        if filtr.IndexExcludesLetters and letters_at_excluded_position(word):
            continue

        possible_answers.append(word)
    return possible_answers


def narrowing_score(target, guess: str) -> int:
    new_filter = WordsFilter.get_new_filter(guess, target)
    merged_filter = WordsFilter.merge_filters(
        blank_filter(), new_filter)
    words_left = answers_that_meet_criteria(merged_filter)
    return len(words_left)


def narrowing_score_per_word_multi_threaded(guess: str) -> dict[str, int]:
    return_dict = {}
    targets = answers_that_meet_criteria(blank_filter())
    for tgt in targets:
        return_dict.setdefault(guess, 0)
        score = narrowing_score(tgt, guess) if guess != tgt else 0
        return_dict[guess] += score
    return return_dict


if __name__ == '__main__':
    with open('words/playable_words.json', 'r') as playable_words:
        guess_words = json.load(playable_words)

    answers = answers_that_meet_criteria(blank_filter())
    print(len(answers))

    s_start = time()
    narrowing_score_per_word_multi_threaded(guess_words[0])
    print(f"Single-thread time taken: {time() - s_start}")

    t_start = time()
    with ThreadPoolExecutor(max_workers=10) as exe:
        result = exe.map(
            narrowing_score_per_word_multi_threaded, guess_words[:3])

    combined_results = {}
    for r in result:
        combined_results.update(r)

    print(f"Multi-thread time taken: {time() - t_start}")
    print(combined_results)
