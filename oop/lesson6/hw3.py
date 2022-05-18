#Реализовать базовый класс Worker (работник).
# определить атрибуты: name, surname, position (должность), income (доход);
# последний атрибут должен быть защищённым и ссылаться на словарь, содержащий элементы:
# оклад и премия, например, {"wage": wage, "bonus": bonus};
# создать класс Position (должность) на базе класса Worker;
# в классе Position реализовать методы получения полного имени сотрудника (get_full_name)
# и дохода с учётом премии (get_total_income);
# проверить работу примера на реальных данных: создать экземпляры класса Position,
# передать данные, проверить значения атрибутов, вызвать методы экземпляров.

class Worker:
    def __init__(self, name, surname, wage, bonus):
        self.name = name
        self.surname = surname
        self._income = {"wage": wage, "bonus": bonus}
class Position(Worker):
    def get_full_name(self):
        return self.name + ' ' + self.surname
    def get_total_income(self):
        return sum(self._income.values())
position_1 = Position('name', 'surname', 20, 30)
print(position_1.get_full_name())
print(position_1.get_total_income())

position_2 = Position('name1', 'surname1', 2000, 30000)
print(position_2.get_full_name())
print(position_2.get_total_income())
