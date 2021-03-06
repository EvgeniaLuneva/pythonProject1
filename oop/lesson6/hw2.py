#Реализовать класс Road (дорога).
#определить атрибуты: length (длина), width (ширина);
#значения атрибутов должны передаваться при создании экземпляра класса;
#атрибуты сделать защищёнными;
#определить метод расчёта массы асфальта, необходимого для покрытия всей дороги;
#использовать формулу: длина*ширина*масса асфальта для покрытия одного кв. метра дороги асфальтом, толщиной в 1 см*число см толщины полотна;
#проверить работу метода.

class Road:
    def __init__(self, length, width):
        self._length = length
        self._width = width
    def massCount(self):
        mass_half = 25
        depth = 5
        return (self._width*self._length*mass_half*depth)//1000

road = Road(20,5000)
print(road.massCount())

