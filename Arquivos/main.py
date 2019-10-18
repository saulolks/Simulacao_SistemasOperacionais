data = [1, 2, 3, 4, {'a': 12}]
print(data)


for item in data:
    if type(item) is dict:
        print(list(item.keys())[0])
    else:
        print(item)