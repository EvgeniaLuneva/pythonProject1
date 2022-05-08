import itertools

el = int(input('variable 1: '))
for i in itertools.count(el, 1):
    if i > 10:
        break
    print(i)

my_list = list(range(1,4))
for i, j in enumerate(itertools.cycle(my_list)):
    print(j)
    if i > 9:
        break
