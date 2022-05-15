#Реализуйте базовый класс Car.
#у класса должны быть следующие атрибуты:
#speed, color, name, is_police (булево). А также методы: go, stop, turn(direction),
#которые должны сообщать, что машина поехала, остановилась, повернула (куда);
#опишите несколько дочерних классов: TownCar, SportCar, WorkCar, PoliceCar;
#добавьте в базовый класс метод show_speed, который должен показывать текущую скорость автомобиля;
#для классов TownCar и WorkCar переопределите метод show_speed.
#При значении скорости свыше 60 (TownCar) и 40 (WorkCar) должно выводиться сообщение о превышении скорости.

class Car:
    def __init__(self, speed, color, name, is_police, direction):
        self.n = name
        self.s = speed
        self.c = color
        self.p = is_police
        self.d = direction
    def go(self):
        return f'car {self.n} goes'
    def stop(self):
        return f'car {self.n} stops'
    def turn(self):
        return f'car {self.n} turn {self.d}'
    def showSpeed(self):
        return f'speed {self.s}'
class TownCar(Car):
    def showSpeed(self):
        if self.s > 60:
            return f'over speed'
        else:
            return f'speed {self.s}'
class SportCar(Car):
    pass
class WorkCar(Car):
    def showSpeed(self):
        if self.s > 40:
            return f'over speed'
class PoliceCar(Car):
    def policeCar(self):
        if self.p == True:
            return f'{self.n}  is the police car'
        else:
            return 'Error'

car1 = TownCar(50, 'black', 'ford', False, 'left')
print(car1.go())
print(car1.stop())
print(car1.turn())
print(car1.showSpeed())
car2 = TownCar(80, 'white', 'kia', False, 'right')
print(car2.go())
print(car2.stop())
print(car2.turn())
print(car2.showSpeed())
car3 = SportCar(180, 'white', 'subaru', False, 'straight forward')
print(car3.go())
print(car3.stop())
print(car3.turn())
print(car3.showSpeed())
car4 = PoliceCar(180, 'white', 'bmw', True, 'straight forward')
print(car4.go())
print(car4.stop())
print(car4.turn())
print(car4.policeCar())
print(car4.showSpeed())
car5 = WorkCar(180, 'white', 'mazda', False, 'straight forward')
print(car5.go())
print(car5.stop())
print(car5.turn())
print(car5.showSpeed())
