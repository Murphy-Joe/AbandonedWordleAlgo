import copy

# how to exclude a second appearance of a letter
excluded_letters = ['a', 't', 'r', 's', 'h', 'u', 'l', 'n', 'v', 'i', 'c']
# how to include a second appearance of a letter
included_letters = ['o', 'e']
letters_excluded_from_index = {0: ['o'], 1: ['e'],  3: ['e'], 4: ['o']}
indexed_letters = {}


def matches_exact_letters(word: str) -> bool:
    matches_indexed_letters = False
    for index, letter in indexed_letters.items():
        if (word[index] != letter):
            matches_indexed_letters = False
            break
        else:
            matches_indexed_letters = True
    if matches_indexed_letters:
        return True


def includes_included_letters(word: str) -> bool:
    all_included_letters_accounted_for = False
    answer_copy = copy.copy(word)

    # for index in sorted(indexed_letters.keys(), reverse=True):
    #     answer_copy = answer_copy[:index] + answer_copy[(index+1):]

    for letter in included_letters:
        if letter not in answer_copy:
            all_included_letters_accounted_for = False
            break
        else:
            answer_copy = answer_copy.replace(letter, '', 1)
            all_included_letters_accounted_for = True
    if all_included_letters_accounted_for:
        return True


def excludes_excluded_letters(word: str) -> bool:
    excludes_correct_letters = not any(
        letter in word for letter in excluded_letters)
    if excludes_correct_letters:
        return True


def letters_at_excluded_position(word: str) -> bool:
    for index, letters in letters_excluded_from_index.items():
        if word[index] in letters:
            return True


def answers_that_meet_criteria(words: list[str]) -> list[str]:
    possible_answers = []
    for word in words:
        if indexed_letters and not matches_exact_letters(word):
            continue

        if included_letters and not includes_included_letters(word):
            continue

        if excluded_letters and not excludes_excluded_letters(word):
            continue

        if letters_excluded_from_index and letters_at_excluded_position(word):
            continue

        possible_answers.append(word)
    return possible_answers


if __name__ == '__main__':
    import json
    import words_filter

    with open('words/playable_words.json', 'r') as five_letter_words_json:
        playable_words = json.load(five_letter_words_json)

    with open('words/targets.json', 'r') as answers_json:
        answers = json.load(answers_json)

    words_to_guess = words_filter.answers_that_meet_criteria(answers)
    print(words_to_guess)
