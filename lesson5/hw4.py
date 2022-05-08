#Напишите программу, открывающую файл на чтение и считывающую построчно данные.
# При этом английские числительные должны заменяться на русские.
# Новый блок строк должен записываться в новый текстовый файл.

dict = {'One':'Один', 'Two':'Два', 'Three':'Три', 'Four':'Четыре'}
with open("file.txt", 'r') as file:
    new_file = open("new_file.txt", 'w')
    while True:
        line = file.readline()
        line_list = line.split('—')
        print(line_list)
        if '' not in line_list:
            new_file.write(dict[line_list[0].strip()]+' —'+line_list[1])
        if not line:
            break
    new_file.close()

