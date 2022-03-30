from game import WordleGame


def make_second_appearance_of_letter_uppercase(word: str) -> str:
    dumb_dict = {}
    for i, ltr in enumerate(word):
        dumb_dict.setdefault(ltr, 0)
        dumb_dict[ltr] += 1
        if dumb_dict[ltr] == 2:
            return word[:i] + word[i].upper() + word[i+1:]
    return word


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


def words_sorted_by_middleness(targets_left: list[str], guess_list: list[str]) -> dict[str, int]:
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


def stuff_after_guess(wordle_game: WordleGame):
    words_left = Solver(wordle_game).answers_that_meet_criteria(
        wordle_game.ResultsFilter, answers)

    print(f'\n{len(words_left)} words left\n')

    print(f'letters scores: {letters_sorted_by_middleness(words_left)}')

    playable_guesses = words_sorted_by_middleness(
        words_left, playable_words)

    guesses_from_targets = words_sorted_by_middleness(
        words_left, words_left)

    cnt = 0
    print(f'most narrowing guesses:')
    for word, score in playable_guesses.items():
        print(f'{word} {score}')
        cnt += 1
        if cnt > 10:
            break


if __name__ == '__main__':
    import json
    from solver import Solver

    from words_filter import WordsFilter

    with open('words/targets.json', 'r') as answers_json:
        answers = json.load(answers_json)

    with open('words/playable_words.json', 'r') as playable_words_json:
        playable_words = json.load(playable_words_json)

    game = WordleGame()
    game.make_guess('roate')
    game.make_guess('slick')
    # game.make_guess('hawms')

    stuff_after_guess(game)

    # take the score of the best word in targets list
    # anything with that score or better goes through the brute force algorithm
    # take best brute force word and make it the guess
    # if there is a tie at the top, tiebreaker goes to word from targets, otherwise just first word
