#Программа запрашивает у пользователя строку чисел, разделённых пробелом.
#При нажатии Enter должна выводиться сумма чисел.
#Пользователь может продолжить ввод чисел, разделённых пробелом и снова нажать Enter.
#Сумма вновь введённых чисел будет добавляться к уже подсчитанной сумме.

def my_func():
    summa = 0
    while True:
        user_str = input('enter numbers with space ').split()
        if user_str[-1] != 'r':
            for el in user_str:
                summa = summa + int(el)
            print(summa)
        elif user_str[-1] == 'r':
            user_str.pop()
            for el in user_str:
                summa = summa + int(el)
            print(summa)
            break
my_func()
