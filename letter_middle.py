from game import WordleGame


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
    return sorted_freq_results


def words_sorted_by_middleness_w_upper(targets_left: list[str], guess_list: list[str]) -> dict[str, int]:
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
    sorted_word_scores = dict(
        sorted(word_scores.items(), key=lambda w_s: w_s[1]))
    return sorted_word_scores


def first_target_word_score_in_best_guesses(best_guesses: dict[str, int], targets_left: list[str]) -> int:
    for word, score in best_guesses.items():
        if word in targets_left:
            return score
    return 0


def words_for_brute_force(wordle_game: WordleGame) -> list[str]:
    words_left = Solver(wordle_game).answers_that_meet_criteria(
        wordle_game.ResultsFilter)

    playable_guesses_w_upper = words_sorted_by_middleness_w_upper(
        words_left, playable_words)

    first_target_word_score = first_target_word_score_in_best_guesses(
        playable_guesses_w_upper, words_left)

    return [word for word in playable_guesses_w_upper.keys() if playable_guesses_w_upper[word] <= first_target_word_score]


def best_guess(wordle_game: WordleGame) -> str:
    solver = Solver(wordle_game)
    words_left = solver.answers_that_meet_criteria(wordle_game.ResultsFilter)
    best_guesses = words_for_brute_force(wordle_game)
    scores_after_brute_force = solver.narrowing_scores(best_guesses)

    sorted_scores = dict(
        sorted(scores_after_brute_force.items(), key=lambda w_s: w_s[1]))
    best_score = sorted_scores[list(sorted_scores.keys())[0]]
    top_word_or_words = [word for word in scores_after_brute_force.keys(
    ) if scores_after_brute_force[word] == best_score]

    if len(top_word_or_words) == 1:
        return top_word_or_words[0]
    elif not any(word in words_left for word in top_word_or_words):
        return top_word_or_words[0]
    else:
        top_targets = [
            word for word in top_word_or_words if word in words_left]
        return top_targets[0]


if __name__ == '__main__':
    import json
    from solver import Solver

    from words_filter import WordsFilter

    with open('words/targets.json', 'r') as answers_json:
        answers = json.load(answers_json)

    with open('words/playable_words.json', 'r') as playable_words_json:
        playable_words = json.load(playable_words_json)

    game = WordleGame('found')
    game.make_guess('roate')
    game.make_guess('oundy')
    # game.make_guess('pound')
    # game.make_guess('found')

    print(best_guess(game))
