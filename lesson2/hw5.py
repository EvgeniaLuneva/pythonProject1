# Реализовать структуру «Рейтинг», представляющую собой набор натуральных чисел,
# который не возрастает.
# У пользователя нужно запрашивать новый элемент рейтинга.
# Если в рейтинге существуют элементы с одинаковыми значениями,
# то новый элемент с тем же значением должен разместиться после них.

my_list = [7, 5, 3, 0, 2, 8, 2]
print(my_list)
number = int(input('enter number: '))
if number in my_list:
    el = my_list.index(number)
    my_list.insert(el, number)
elif number < min(my_list):
    my_list.append(number)
elif number > max(my_list):
    my_list.insert(0, number)
print(sorted(my_list, reverse=True))
