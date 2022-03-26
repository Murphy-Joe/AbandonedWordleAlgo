def letters_sorted_by_middleness(word_list: list[str]) -> dict[str, int]:
    freq_results = {}
    for word in word_list:
        for ltr in set(word):
            freq_results.setdefault(ltr, 0)
            freq_results[ltr] += 1

    for ltr, freq in freq_results.items():
        freq_results[ltr] = abs(freq - len(word_list)/2)

    sorted_freq_results = dict(sorted(freq_results.items(),
                                      key=lambda ltr_frq: ltr_frq[1]))
    return sorted_freq_results


def words_sorted_by_middleness(word_list: list[str], letter_scores=None) -> dict[str, int]:
    if letter_scores is None:
        letter_scores = letters_sorted_by_middleness(word_list)
    word_scores = {}
    for word in word_list:
        if len(set(word)) != len(word):
            word_scores[word] = 999999
            continue
        word_scores.setdefault(word, 0)
        for ltr in word:
            try:
                word_scores[word] += letter_scores[ltr]
            except KeyError:
                word_scores[word] = 9999999
    sorted_word_scores = dict(
        sorted(word_scores.items(), key=lambda w_s: w_s[1]))
    return sorted_word_scores


if __name__ == '__main__':
    import json
    import words_filter

    with open('answers.json', 'r') as answers_json:
        answers = json.load(answers_json)

    with open('playable_words.json', 'r') as playable_words_json:
        playable_words = json.load(playable_words_json)

    words_left = words_filter.answers_that_meet_criteria(answers)

    letters_to_split_words_list = letters_sorted_by_middleness(words_left)

    playable_guesses = words_sorted_by_middleness(
        playable_words, letters_to_split_words_list)

    guesses_from_targets = words_sorted_by_middleness(
        words_left, letters_to_split_words_list)

    print(guesses_from_targets)

    cnt = 0
    for word, score in playable_guesses.items():
        print(f'{word} {score}')
        cnt += 1
        if cnt > 20:
            break
