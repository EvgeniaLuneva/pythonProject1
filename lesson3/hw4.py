#Программа принимает действительное положительное число x и целое отрицательное число y.
#Выполните возведение числа x в степень y. Задание реализуйте в виде функции my_func(x, y).
#При решении задания нужно обойтись без встроенной функции возведения числа в степень.

def my_func(x, y):
    if x > 0 and y < 0:
       res = x ** y
       print(res)
    else:
     print('Error: wrong numbers')
x = float(input('enter positive number '))
y = int(input('enter negative integer number '))
my_func(x, y)

