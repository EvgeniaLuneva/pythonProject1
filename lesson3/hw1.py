# Реализовать функцию, принимающую два числа (позиционные аргументы) и выполняющую их деление.
# Числа запрашивать у пользователя, предусмотреть обработку ситуации деления на ноль.

def div_1 ():
    num_1 = int(input('enter first number '))
    num_2 = int(input('enter second number '))
    try:
        res = num_1/num_2
        return res
    except ZeroDivisionError:
        return 'error: Devision by zero'
result = div_1()
print('result', result)