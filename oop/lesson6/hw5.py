#Реализовать класс Stationery (канцелярская принадлежность).
# определить в нём атрибут title (название) и метод draw (отрисовка). Метод выводит сообщение «Запуск отрисовки»;
# создать три дочерних класса Pen (ручка), Pencil (карандаш), Handle (маркер);
# в каждом классе реализовать переопределение метода draw. Для каждого класса метод
# должен выводить уникальное сообщение;
# создать экземпляры классов и проверить, что выведет описанный метод для каждого экземпляра.

class Stationery:
    def __init__(self, title):
        self.t = title
    def draw(self):
        return f'start drawing'
class Pen(Stationery):
    def draw(self):
        return f'start drawing {self.t}'
class Pencil(Stationery):
    def draw(self):
        return f'start drawing {self.t}'
class Handle(Stationery):
    def draw(self):
        return f'start drawing {self.t}'
stationery = Stationery('title')
pen = Pen('by Pen')
pencil = Pencil('by Pencil')
handle = Handle('by Handle')
print(stationery.draw())
print(pen.draw())
print(handle.draw())
print(pencil.draw())