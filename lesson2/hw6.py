# Реализовать структуру данных «Товары».
# Она должна представлять собой список кортежей.
# Каждый кортеж хранит информацию об отдельном товаре.
# В кортеже должно быть два элемента — номер товара и словарь с параметрами,
# то есть характеристиками товара: название, цена, количество, единица измерения.
# Структуру нужно сформировать программно, запросив все данные у пользователя.

names = ['name', 'price', 'quantity', 'measure']
while True:
    for name in names:
        enter = input(f'{name}' + ' : ')
        my_dict[name] = enter
    if '' in my_dict.values():
        break
    my_list.append((i, my_dict))
    my_dict = {}
    i += 1
print(my_list)
my_dict_2 = {}
for name in names:
    k = []
    for i in my_list:
        k.append(i[1][name])
    my_dict_2[name] = k
print(my_dict_2)



