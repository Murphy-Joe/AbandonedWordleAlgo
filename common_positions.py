import json
from pprint import pprint

with open('answers.json', 'r') as answers_json:
    answers = json.load(answers_json)

idx_results = {}
freq_results = {}

for answer in answers:
    for idx, letter in enumerate(answer):
        idx_results.setdefault(letter, {})
        idx_results[letter].setdefault(idx, 0)
        idx_results[letter][idx] += 1

        freq_results.setdefault(letter, 0)
        freq_results[letter] += 1

sorted_freq_res = dict(sorted(freq_results.items(),
                              key=lambda letter_count_tup: letter_count_tup[1]))

pprint(idx_results)
print(sorted_freq_res)
print(idx_results['a'][0])
