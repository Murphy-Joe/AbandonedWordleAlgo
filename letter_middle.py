import json
from time import time
from game import WordleGame
from solver import Solver

with open('words/playable_words.json', 'r') as playable_words_json:
    playable_words = json.load(playable_words_json)


def make_second_appearance_of_letter_uppercase(word: str) -> str:
    if len(word) == len(set(word)):
        return word
    word_builder = ''
    for ltr in word:
        if ltr not in word_builder:
            word_builder += ltr
        else:
            word_builder += ltr.upper()
    return word_builder


def letters_sorted_by_middleness(word_list: list[str]) -> dict[str, int]:
    freq_results = {}
    word_list = [make_second_appearance_of_letter_uppercase(
        word) for word in word_list]
    for word in word_list:
        for ltr in set(word):
            freq_results.setdefault(ltr, 0)
            freq_results[ltr] += 1

    for ltr, freq in freq_results.items():
        freq_results[ltr] = abs(freq - len(word_list)/2)

    sorted_freq_results = dict(sorted(freq_results.items(),
                                      key=lambda ltr_frq: ltr_frq[1]))

    print(f'\nletter freq scores')
    cnt = 0
    for ltr, freq in sorted_freq_results.items():
        print(ltr, freq)
        cnt += 1
        if cnt > 10:
            break

    return sorted_freq_results


def words_sorted_by_middleness_w_upper(targets_left: list[str], guess_list: list[str]) -> list[tuple[str, int]]:
    letter_scores = letters_sorted_by_middleness(targets_left)
    guess_list = [make_second_appearance_of_letter_uppercase(
        word) for word in guess_list]
    word_scores = {}
    for word in guess_list:
        word_scores.setdefault(word, 0)
        for ltr in word:
            try:
                word_scores[word] += letter_scores[ltr]
            except KeyError:  # ltr not in targets_left
                word_scores[word] += len(targets_left)
    sorted_word_scores = sorted(word_scores.items(), key=lambda w_s: w_s[1])

    # print(
    #     f'\nbest words per middleness score out of {len(sorted_word_scores)}')
    # for i, (k, v) in enumerate(sorted_word_scores.items()):
    #     print(k, v)
    #     if i > 10:
    #         break
    return sorted_word_scores


def words_for_brute_force(wordle_game: WordleGame) -> list[str]:
    words_left = Solver(wordle_game).answers_that_meet_criteria(
        wordle_game.ResultsFilter)

    playable_guesses_w_upper = words_sorted_by_middleness_w_upper(
        words_left, playable_words)

    print(f'\nword eligibility for brute force algo')
    cnt = 0
    for k, v in playable_guesses_w_upper:
        print(k, v)
        cnt += 1
        if cnt > 10:
            break

    guesses_w_upper_from_targets = words_sorted_by_middleness_w_upper(
        words_left, words_left)

    best_playable_guesses_w_upper = [tup[0]
                                     for tup in playable_guesses_w_upper[:40]]
    best_guesses_w_upper_from_targets = [tup[0]
                                         for tup in guesses_w_upper_from_targets[:10]]
    best_guesses = best_playable_guesses_w_upper + best_guesses_w_upper_from_targets

    return list(set(best_guesses))


def best_guess(wordle_game: WordleGame) -> str:
    solver = Solver(wordle_game)
    words_left = solver.answers_that_meet_criteria(wordle_game.ResultsFilter)
    best_guesses = words_for_brute_force(wordle_game)

    brute_force_start = time()
    scores_after_brute_force = solver.narrowing_scores(
        best_guesses, words_left)
    brute_force_end = time()
    print(f'\nbrute force time: {brute_force_end-brute_force_start}')

    sorted_scores = dict(
        sorted(scores_after_brute_force.items(), key=lambda w_s: w_s[1]))

    cnt = 0
    print(f'\nbest words after brute force out of {len(sorted_scores)}')
    for k, v in sorted_scores.items():
        print(k, v)
        cnt += 1
        if cnt > 10:
            break
    best_score = sorted_scores[list(sorted_scores.keys())[0]]
    top_word_or_words = [
        word for word in scores_after_brute_force if scores_after_brute_force[word] == best_score]

    if len(top_word_or_words) == 1:
        return top_word_or_words[0]
    elif not any(word in words_left for word in top_word_or_words):
        return top_word_or_words[0]
    else:
        top_targets = [
            word for word in top_word_or_words if word in words_left]
        return top_targets[0]


if __name__ == '__main__':

    import random
    from solver import Solver

    with open('words/targets.json', 'r') as answers_json:
        answers = json.load(answers_json)

    total_start = time()
    # print(random.choice(answers))
    game = WordleGame('epoxy')
    game.make_guess('oater')
    game.make_guess('shuln')
    # game.make_guess('weedy')
    # game.make_guess('fewer')

    remaining_answers = Solver(
        game).answers_that_meet_criteria(game.ResultsFilter)
    print(f'words left: {remaining_answers}') if len(
        remaining_answers) < 6 else print(f'words left: {len(remaining_answers)}')
    print(f'\nbest guess: {best_guess(game)}')
    total_end = time()
    print(f'\ntotal time: {total_end-total_start}')
