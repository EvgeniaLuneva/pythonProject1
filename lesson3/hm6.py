#Реализовать функцию int_func(), принимающую слова из маленьких латинских букв и возвращающую их же,
#но с прописной первой буквой.
#Например, print(int_func(‘text’)) -> Text.
k
def int_func():
    user_str = input('enter words: ')
    up_str = user_str[0].upper() + user_str[1:]
    return up_str
print(int_func())
