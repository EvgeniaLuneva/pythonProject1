#Создайте собственный класс-исключение, обрабатывающий ситуацию деления на ноль.
# Проверьте его работу на данных, вводимых пользователем.
# При вводе нуля в качестве делителя программа должна корректно обработать эту ситуацию и не завершиться с ошибкой.

class MyException(Exception):
    pass

while True:
    num = int(input("Enter numerator: "))
    den = int(input("Enter denominator: "))
    try:
        if den == 0:
            raise MyException()
        else:
            print(num/den)
        break
    except MyException:
        print(f'denominator is {den}, enter some else number')
        continue