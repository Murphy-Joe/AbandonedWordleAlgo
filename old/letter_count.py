global_words_left = []


def filter_words(word_list: list[str], letter_list: list[str]) -> list[str]:
    filtered_words = []
    for word in word_list:
        if all(letter in word for letter in letter_list):
            filtered_words.append(word)
    return filtered_words


def letter_frequency(word_list: list[str]) -> dict:
    freq_results = {}
    for word in word_list:
        for ltr in word:
            freq_results.setdefault(ltr, 0)
            freq_results[ltr] += 1

    sorted_freq_results = dict(sorted(
        freq_results.items(), key=lambda x: x[1], reverse=True))
    return sorted_freq_results


def letters_to_guess(frequency_results: dict, words_left: list[str]) -> list[str]:
    ltrs_to_guess = []
    for idx, letter in enumerate(frequency_results.keys()):
        if idx <= 4 and filter_words(words_left, ltrs_to_guess + [letter]):
            ltrs_to_guess.append(letter)
        else:
            break
    return ltrs_to_guess


def letters_to_guess_for_words_left(words_left: list[str]) -> list[str]:
    return letters_to_guess(letter_frequency(words_left), words_left)


if __name__ == '__main__':
    import json

    with open('words/targets.json', 'r') as answers_json:
        answers = json.load(answers_json)

    print(letters_to_guess_for_words_left(answers))
