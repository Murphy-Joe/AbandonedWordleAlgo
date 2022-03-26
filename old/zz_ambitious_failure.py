import json
from datetime import date
import copy


def game_number() -> int:
    beginning = date(year=2021, month=6, day=19)
    today = date.today()
    time_delta = today - beginning
    answers_idx = time_delta.days
    return answers_idx


def matches_exact_letters(answer: str) -> bool:
    matches_indexed_letters = False
    for index, letter in indexed_letters.items():
        if (answer[index] != letter):
            matches_indexed_letters = False
            break
        else:
            matches_indexed_letters = True
    if matches_indexed_letters:
        return True


def includes_included_letters(answer: str) -> bool:
    all_included_letters_accounted_for = False
    answer_copy = copy.copy(answer)

    for index in sorted(indexed_letters.keys(), reverse=True):
        answer_copy = answer_copy[:index] + answer_copy[(index+1):]

    for letter in included_letters:
        if letter not in answer_copy:
            all_included_letters_accounted_for = False
            break
        else:
            answer_copy = answer_copy.replace(letter, '', 1)
            all_included_letters_accounted_for = True
    if all_included_letters_accounted_for:
        return True


def excludes_excluded_letters(answer: str) -> bool:
    excludes_correct_letters = not any(
        letter in answer for letter in excluded_letters)
    if excludes_correct_letters:
        return True


def letters_at_excluded_position(answer: str) -> bool:
    for index, letters in letters_excluded_from_index.items():
        if answer[index] in letters:
            return True


def answers_that_meet_criteria(answrs: list[str]) -> list[str]:
    possible_answrs = []
    for answer in answrs:
        if indexed_letters and not matches_exact_letters(answer):
            continue

        if included_letters and not includes_included_letters(answer):
            continue

        if excluded_letters and not excludes_excluded_letters(answer):
            continue

        if letters_excluded_from_index and letters_at_excluded_position(answer):
            continue

        possible_answrs.append(answer)
    return possible_answrs


def letters_in_remaining_answers(possible_answrs: list[str]) -> dict[str, int]:
    letters_to_include_on_next_guess = {}
    possible_answers_copy = copy.copy(possible_answrs)

    for possible_answer in possible_answers_copy:
        for index in sorted(indexed_letters.keys(), reverse=True):
            possible_answer = possible_answer[:index] + \
                possible_answer[(index+1):]

        for included_letter in included_letters:
            possible_answer = possible_answer.replace(included_letter, "", 1)

        for letter in possible_answer:
            letters_to_include_on_next_guess.setdefault(letter, 0)
            letters_to_include_on_next_guess[letter] += 1
    sorted_dict = dict(sorted(letters_to_include_on_next_guess.items(),
                              key=lambda letter_count: letter_count[1]))
    return sorted_dict


def get_letters_and_its_word_splits_from_word_set(ltrs_dict: dict, remaining_answers: list[str]) -> dict[str, tuple[list[str], list[str]]]:
    split_count_per_letter = {}
    for ltr in ltrs_dict.keys():
        answers_with_letter = [
            word for word in remaining_answers if ltr in word]
        answers_without_letter = [
            word for word in remaining_answers if ltr not in word]
        split_count_per_letter.setdefault(
            ltr, (answers_with_letter, answers_without_letter))
    best_splits_first = dict(sorted(split_count_per_letter.items(),
                                    key=lambda letter_words_lists_tup: abs(len(letter_words_lists_tup[1][0]) - len(remaining_answers)/2)))
    return best_splits_first


def choose_best_letter(best_letters: dict[str, tuple[list[str], list[str]]], letters_already_chosen: list[str]) -> str:
    best_letter_list = list(best_letters.keys())
    for ltr in best_letter_list:
        if ltr not in letters_already_chosen:
            return ltr


def filter_possible_words_by_letters(letters: list[str], words_list: list[str]) -> list[str]:
    none_safe_letters = [letter for letter in letters if letter is not None]
    filtered_list = [word for word in words_list if len(
        [letter for letter in none_safe_letters if letter in word]) == len(none_safe_letters)]
    return filtered_list


def filter_possible_words_with_variable_letters(primary_letter: str, secondary_ltrs: list[str],  how_many_secondary_matches: int, words_list: list[str], must_use_primary: bool = True) -> list[str]:
    none_safe_letters = [
        letter for letter in secondary_ltrs if letter is not None]
    how_many_secondary_matches = how_many_secondary_matches - \
        (len(secondary_ltrs) - len(none_safe_letters))
    modified_words_list = []
    if must_use_primary:
        modified_words_list = [
            word for word in words_list if primary_letter in word]
    else:
        modified_words_list = words_list

    filtered_list = [word for word in modified_words_list if len(
        [letter for letter in none_safe_letters if letter in word]) >= how_many_secondary_matches]
    if len(filtered_list) == 0:
        return modified_words_list
    return filtered_list


with open('words/playable_words.json', 'r') as five_letter_words_json:
    words = json.load(five_letter_words_json)

with open('words/targets.json', 'r') as answers_json:
    answers = json.load(answers_json)

answers_index = game_number()

# how to exclude a second appearance of a letter
excluded_letters = ['x', 'r', 'a', 'i', 'l']
# how to include a second appearance of a letter
included_letters = ['e', 's']
letters_excluded_from_index = {0: ['e'], 2: ['t'], 1: ['s'], 3: ['e']}
indexed_letters = {4: 't'}

# results from guess
possible_answers = answers_that_meet_criteria(answers)
print('total possibles', len(possible_answers), possible_answers[:10])

if len(possible_answers) <= 2:
    # make this method that cuts out here
    print(possible_answers[0])
    quit()

total_letters_to_include_in_next_guess = letters_in_remaining_answers(
    possible_answers)
# print('total letters', len(total_letters_to_include_in_next_guess),
#       total_letters_to_include_in_next_guess)


best_letters_chosen = []
backup_letters_round2 = []
all_letters = []
# round 1 pick '1' split letter
best_letters_with_resulting_word_lists = get_letters_and_its_word_splits_from_word_set(
    total_letters_to_include_in_next_guess, possible_answers)

ltr1 = choose_best_letter(
    best_letters_with_resulting_word_lists, best_letters_chosen)
best_letters_chosen.append(ltr1)

words_w_ltr1 = best_letters_with_resulting_word_lists[ltr1][0]
words_wo_ltr1 = best_letters_with_resulting_word_lists[ltr1][1]

print(ltr1)

# round 2 pick '2' split letters
total_letter_lists2 = letters_in_remaining_answers(words_w_ltr1)
total_letter_lists3 = letters_in_remaining_answers(words_wo_ltr1)

best_letters2_w_word_splits = get_letters_and_its_word_splits_from_word_set(
    total_letter_lists2, words_w_ltr1)
best_letters3_w_word_splits = get_letters_and_its_word_splits_from_word_set(
    total_letter_lists3, words_wo_ltr1)

ltr2 = choose_best_letter(best_letters2_w_word_splits, best_letters_chosen)
best_letters_chosen.append(ltr2)
all_letters.append(ltr2)

ltr3 = choose_best_letter(best_letters3_w_word_splits, best_letters_chosen)
best_letters_chosen.append(ltr3)
all_letters.append(ltr3)

ltr2_backup = choose_best_letter(
    best_letters2_w_word_splits, best_letters_chosen)
backup_letters_round2.append(ltr2_backup)
all_letters.append(ltr2_backup)

ltr3_backup = choose_best_letter(
    best_letters3_w_word_splits, best_letters_chosen)
backup_letters_round2.append(ltr3_backup)
all_letters.append(ltr3_backup)

print(ltr2, ltr3)

# check for matching possible answers before splitting further
letters_to_filter_by = copy.copy(best_letters_chosen)
letters_used = []

secondary_letters = all_letters[1:]
next_guess_options_from_3_letters = filter_possible_words_by_letters(letters_to_filter_by,
                                                                     possible_answers)
if len(possible_answers) >= 32:
    if len(next_guess_options_from_3_letters) == 0:
        letters_to_filter_by[-1] = backup_letters_round2[-1]
        next_guess_options_from_3_letters = filter_possible_words_by_letters(letters_to_filter_by,
                                                                             possible_answers)
    if len(next_guess_options_from_3_letters) == 0:
        letters_to_filter_by[-1] = best_letters_chosen[-1]
        letters_to_filter_by[1] = backup_letters_round2[0]
        next_guess_options_from_3_letters = filter_possible_words_by_letters(letters_to_filter_by,
                                                                             possible_answers)
    if len(next_guess_options_from_3_letters) == 0:
        next_guess_options_from_3_letters = filter_possible_words_by_letters(
            best_letters_chosen, words)

elif len(possible_answers) >= 8:
    # between 6-31
    # contains ltr1 and 2/4 from answer list

    next_guess_options_from_3_letters = filter_possible_words_with_variable_letters(
        best_letters_chosen[0], secondary_letters, 2, possible_answers)
    # still no? contains 2/4 from answer list
    if len(next_guess_options_from_3_letters) == 0:
        next_guess_options_from_3_letters = filter_possible_words_with_variable_letters(
            best_letters_chosen[0], secondary_letters, 2, possible_answers, False)
else:
    # 5 or less
    # contains ltr1 and 1/4 from answer list
    next_guess_options_from_3_letters = filter_possible_words_with_variable_letters(
        best_letters_chosen[0], secondary_letters, 1, possible_answers)
    # still no? contains 2/4 from answer list
    if len(next_guess_options_from_3_letters) == 0:
        next_guess_options_from_3_letters = filter_possible_words_with_variable_letters(
            best_letters_chosen[0], secondary_letters, 2, possible_answers, False)

print(letters_to_filter_by)
print(next_guess_options_from_3_letters)
# round 3 pick '4' split letters

# we have the filtered letters we used
# we need to say, gimme the split lists from filter letters 1 and 2 not 0
primary_w_filtered_letter1_possible_answers = []
primary_wo_filtered_letter1_possible_answers = []
primary_w_filtered_letter2_possible_answers = []
primary_wo_filtered_letter2_possible_answers = []

if letters_to_filter_by[1] and best_letters2_w_word_splits[
        letters_to_filter_by[1]][0]:
    primary_w_filtered_letter1_possible_answers = best_letters2_w_word_splits[
        letters_to_filter_by[1]][0]

if letters_to_filter_by[1] and best_letters2_w_word_splits[
        letters_to_filter_by[1]][1]:
    primary_wo_filtered_letter1_possible_answers = best_letters2_w_word_splits[
        letters_to_filter_by[1]][1]

if letters_to_filter_by[2] and best_letters3_w_word_splits[
        letters_to_filter_by[2]][0]:
    primary_w_filtered_letter2_possible_answers = best_letters3_w_word_splits[
        letters_to_filter_by[2]][0]

if letters_to_filter_by[2] and best_letters3_w_word_splits[
        letters_to_filter_by[2]][1]:
    primary_wo_filtered_letter2_possible_answers = best_letters3_w_word_splits[
        letters_to_filter_by[2]][1]

total_letter_lists4 = letters_in_remaining_answers(
    primary_w_filtered_letter1_possible_answers)
total_letter_lists5 = letters_in_remaining_answers(
    primary_wo_filtered_letter1_possible_answers)
total_letter_lists6 = letters_in_remaining_answers(
    primary_w_filtered_letter2_possible_answers)
total_letter_lists7 = letters_in_remaining_answers(
    primary_wo_filtered_letter2_possible_answers)

best_letters4_w_word_splits = get_letters_and_its_word_splits_from_word_set(
    total_letter_lists4, primary_w_filtered_letter1_possible_answers)
best_letters5_w_word_splits = get_letters_and_its_word_splits_from_word_set(
    total_letter_lists5, primary_wo_filtered_letter1_possible_answers)
best_letters6_w_word_splits = get_letters_and_its_word_splits_from_word_set(
    total_letter_lists6, primary_w_filtered_letter2_possible_answers)
best_letters7_w_word_splits = get_letters_and_its_word_splits_from_word_set(
    total_letter_lists7, primary_wo_filtered_letter2_possible_answers)

tertiary_letters = []
ltr4 = choose_best_letter(best_letters4_w_word_splits, letters_to_filter_by)
if ltr4:
    tertiary_letters.append(ltr4)

ltr5 = choose_best_letter(best_letters5_w_word_splits, letters_to_filter_by)
if ltr5:
    tertiary_letters.append(ltr5)

ltr6 = choose_best_letter(best_letters6_w_word_splits, letters_to_filter_by)
if ltr6:
    tertiary_letters.append(ltr6)

ltr7 = choose_best_letter(best_letters7_w_word_splits, letters_to_filter_by)
if ltr7:
    tertiary_letters.append(ltr7)

guess_with_highest_teriary_letters = ''
leading_count = 0
for guess in next_guess_options_from_3_letters:
    amt_of_tertiary_letters = 0
    for letter in tertiary_letters:
        if letter in guess:
            amt_of_tertiary_letters += 1
    if amt_of_tertiary_letters > leading_count:
        guess_with_highest_teriary_letters = guess
if not guess_with_highest_teriary_letters:
    guess_with_highest_teriary_letters = next_guess_options_from_3_letters[0]

print(guess_with_highest_teriary_letters)
