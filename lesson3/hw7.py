#Продолжить работу над заданием.
#В программу должна попадать строка из слов, разделённых пробелом.
#Каждое слово состоит из латинских букв в нижнем регистре.
#Нужно сделать вывод исходной строки, но каждое слово должно начинаться с заглавной буквы.
#Используйте написанную ранее функцию int_func().

def int_func():
    user_str = input('enter words: ').split()
    s = ''
    for el in user_str:
        s += el.capitalize() + ' '
    print(s)
int_func()