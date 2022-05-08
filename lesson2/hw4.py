# Пользователь вводит строку из нескольких слов, разделённых пробелами.
# Вывести каждое слово с новой строки. Строки нужно пронумеровать.
# Если слово длинное, выводить только первые 10 букв в слове.

str = input('enter string: ').split()
dict = {}
i = 1
for el in str:
    if len(el) > 10:
        el = el[0:10]
        dict[i] = el
    else:
        dict[i] = el
    i += 1
for key, value in dict.items():
    print(key, value)

