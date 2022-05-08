#Создать (программно) текстовый файл, записать в него программно набор чисел, разделённых пробелами.
# Программа должна подсчитывать сумму чисел в файле и выводить её на экран.

import random

file = open('file_hw5.txt', 'w')
file.write(' '.join(list(map(str,list(range(1,10))))))
file.close()
file_new = open('file_hw5.txt','r')
list = file_new.read().split()
summa = 0
for i in list:
     summa += int(i)
file_new.close()
print(summa)
