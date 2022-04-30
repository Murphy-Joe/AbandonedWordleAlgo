letters = {'A': 2, 'a':3}
newDict={}
for k in letters.keys():
    if k.isupper():
        newKey = f"{k}{k}"
        newDict[newKey] = letters[k]
    else:
        newDict[k.upper()] = letters[k]

print(newDict)