#Реализовать функцию my_func(),
#которая принимает три позиционных аргумента и возвращает сумму наибольших двух аргументов.

def my_func():
    el_1 = int(input('number 1 '))
    el_2 = int(input('number 2 '))
    el_3 = int(input('number 3 '))
    if el_1 > el_3 and el_2 > el_3:
        res = el_1 + el_2
    elif el_1 > el_2 and el_3 > el_2:
        res = el_1 + el_3
    else:
        res = el_2 + el_3
    return res
print(my_func())