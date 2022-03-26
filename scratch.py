import copy

dict1 = {0: ['c']}
dict2 = {0: ['r'], 1: ['s'], 4: ['c']}
merged = copy.copy(dict1)

extend = dict(dict1, **dict2)

print(extend)

# merge dictionary whose value is list
for key, value in dict2.items():
    if key in dict1.keys():
        merged[key].extend(value)
    else:
        merged.setdefault(key, value)

print(merged)
