# Создать программный файл в текстовом формате, записать в него построчно данные, вводимые пользователем.
# Об окончании ввода данных будет свидетельствовать пустая строка.

my_file = open('text.txt', 'w')
while True:
    text = input('enter the text: ')
    if text == '':
        my_file.close()
        break
    else:
        my_file.write(text+'\n')