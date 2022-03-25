import json
from pprint import pprint

with open('answers.json', 'r') as answers_json:
    answers = json.load(answers_json)

idx_results = {}

for answer in answers:
    for idx, letter in enumerate(answer):
        idx_results.setdefault(letter, {})
        idx_results[letter].setdefault(idx, 0)
        idx_results[letter][idx] += 1


def best_of_guess_words(guess_words: list[str]) -> str:
    if len(guess_words) == 0:
        return ''
    elif len(guess_words) == 1:
        return guess_words[0]
    else:
        best_guess = ''
        best_guess_score = 0
        for guess in guess_words:
            guess_score = 0
            for i, letter in enumerate(guess):
                guess_score += idx_results[letter][i]
            if guess_score > best_guess_score:
                best_guess = guess
                best_guess_score = guess_score
        return best_guess


if __name__ == '__main__':
    import json
    import letter_count

    with open('answers.json', 'r') as answers_json:
        answers = json.load(answers_json)

    letters_to_guess = (letter_count.letters_to_guess_for_words_left(answers))

    words_to_guess = (letter_count.filter_words(answers, letters_to_guess))

    print(best_of_guess_words(words_to_guess))
