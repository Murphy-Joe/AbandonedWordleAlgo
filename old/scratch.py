d = [{'zerr':2}, {'har':1}]
d.sort(key=lambda kv: tuple(kv.items())[0][1])
print(d)
