#Создайте собственный класс-исключение, который должен проверять содержимое списка на наличие только чисел.
#Проверить работу исключения на реальном примере. Запрашивать у пользователя данные и заполнять список необходимо только числами.
#Класс-исключение должен контролировать типы данных элементов списка.

class Error(Exception):
    pass
class DivByZero(Error):
    pass

my_list = []
while True:
    try:
        value = input('enter number to list:')
        if value == 'stop':
            break
        if not value.isdigit():
            raise DivByZero(value)
        my_list.append(int(value))
    except DivByZero as x:
        print('not number, try again', x)
print(my_list)