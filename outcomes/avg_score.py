import json

# words = ['roate', 'salet', 'soare', 'reast']
# for target in words:
#     with open(f'outcomes/{target}_outcomes.json', 'r') as file_read:
#         file_obj = json.load(file_read)
#     avg_guesses_needed = sum(file_obj.values())/len(file_obj)
#     print(f'{target}: {avg_guesses_needed}')

words2 = ['salet', 'roate']
for target in words2:
    with open(f'outcomes/{target}2.json', 'r') as file_read:
        file_obj = json.load(file_read)
    avg_guesses_needed = sum(file_obj.values())/len(file_obj)
    print(f'{target}: {avg_guesses_needed}')
