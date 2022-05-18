#Реализовать проект расчёта суммарного расхода ткани на производство одежды.
# Основная сущность (класс) этого проекта — одежда, которая может иметь определённое название.
# К типам одежды в этом проекте относятся пальто и костюм. У этих типов одежды существуют параметры:
# размер (для пальто) и рост (для костюма). Это могут быть обычные числа: V и H, соответственно.
# Для определения расхода ткани по каждому типу одежды использовать формулы:
# для пальто (V/6.5 + 0.5), для костюма (2*H + 0.3). Проверить работу этих методов на реальных данных.
# Реализовать общий подсчет расхода ткани.
# Проверить на практике полученные на этом уроке знания: реализовать абстрактные классы для основных классов проекта,
# проверить на практике работу декоратора @property.

from abc import ABC, abstractmethod

class Clothes:
    def __init__(self, name, param):
        self.n = name
        self.p = param
    def __str__(self):
        return f'given clothes {self.n}, size {self.p}'
    @abstractmethod
    def count(self):
        pass
class Coat(Clothes):
    @property
    def count(self):
        return self.p//6.5 + 0.5
class Suit(Clothes):
    @property
    def count(self):
        return self.p * 2 + 0.3

clothes_1 = Clothes('Suit', 42)
clothes_2 = Clothes('Coat', 1.7)
print(clothes_1.__str__())
print(clothes_2.__str__())
coat = Coat('Coat', 1.7)
print('you need ', coat.count, 'for making coat')
suit = Suit('Suit', 42)
print('you need ', suit.count, 'for making suit')



