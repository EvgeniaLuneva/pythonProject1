#Создать текстовый файл (не программно), сохранить в нём несколько строк,
# выполнить подсчёт строк и слов в каждой строке.

with open("text1.txt") as text:
    list = text.read().split('\n')
    print(list)
    print('number of lines: ', len(list))
    for el in list:
        print('number of words', len(el.split()))