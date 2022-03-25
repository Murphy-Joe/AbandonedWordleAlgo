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


def words_sorted_by_middleness(word_list: list[str], remove_dbl_ltrs=True) -> dict[str, int]:
    letter_scores = letters_sorted_by_middleness(word_list)
    word_scores = {}
    if remove_dbl_ltrs:
        word_list = [word for word in word_list if len(set(word)) == len(word)]
    for word in word_list:
        word_scores.setdefault(word, 0)
        for ltr in word:
            word_scores[word] += letter_scores[ltr]
    sorted_word_scores = dict(
        sorted(word_scores.items(), key=lambda w_s: w_s[1]))
    return sorted_word_scores


if __name__ == '__main__':
    import json

    with open('answers.json', 'r') as answers_json:
        answers = json.load(answers_json)

    print(words_sorted_by_middleness(answers))
