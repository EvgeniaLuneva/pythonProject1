#Реализовать класс «Дата», функция-конструктор которого должна принимать дату в виде строки формата «день-месяц-год».
# В рамках класса реализовать два метода.
# Первый, с декоратором @classmethod. Он должен извлекать число, месяц, год и преобразовывать их тип к типу «Число».
# Второй, с декоратором @staticmethod, должен проводить валидацию числа, месяца и года (например, месяц — от 1 до 12).
# Проверить работу полученной структуры на реальных данных.

class Date:
    def __init__(self, date: str) -> None:
        self.date = date

    @classmethod
    def parsing_date(cls, date_string: str, calendar_value: str) -> int:
        calendar_type = ('day', 'month', 'year')
        dict_value_date = {key: value for key, value in list(zip(calendar_type,
                                                                 list(map(int, date_string.split('-')))))}
        return dict_value_date[calendar_value]


    @staticmethod
    def validation_date(date_string: str) -> bool:
        day, month, year = list(map(int, date_string.split('-')))
        return day <= 31 and month <= 12 and year <= 3000


date1 = Date('01-04-1221')
day = Date.parsing_date('01-04-1221', 'day')
print(day)
print(Date.validation_date('30-30-300'))
print(Date.validation_date('30-05-2012'))