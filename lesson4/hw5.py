#Реализовать формирование списка, используя функцию range() и возможности генератора.
#В список должны войти чётные числа от 100 до 1000 (включая границы).
#Нужно получить результат вычисления произведения всех элементов списка.

from functools import reduce
my_list = [el for el in range(100,1001) if el % 2 == 0]
print(my_list)
def mult(el_prev, el):
    return el_prev * el
print(reduce(mult,my_list))