import json
import letter_count

with open('answers.json', 'r') as answers_json:
    answers = json.load(answers_json)

letters_to_guess = (letter_count.letters_to_guess_for_words_left(answers))
words_to_guess = (letter_count.filter_words(answers, letters_to_guess))
