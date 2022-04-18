#Узнайте у пользователя число n.
#Найдите сумму чисел n + nn + nnn. Например, пользователь ввёл число 3. Считаем 3 + 33 + 333 = 369.

number = input('enter the nuber:')
num_2 = int(number * 2)
num_3 = int(number * 3)
number = int(number)
res = number + num_2 + num_3
print ('result:', res)


