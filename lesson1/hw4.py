#Пользователь вводит целое положительное число.
#Найдите самую большую цифру в числе.
#Для решения используйте цикл while и арифметические операции.

number = int(input('enter positive integer number:'))
maxnum = number % 10
res = 0
while number > 0:
 if maxnum < number % 10:
    maxnum = number % 10
 res = res + 1
 number = number // 10
print('the max numeral is: ', maxnum)




