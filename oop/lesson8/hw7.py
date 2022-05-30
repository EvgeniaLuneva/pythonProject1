#Реализовать проект «Операции с комплексными числами». Создайте класс «Комплексное число».
# Реализуйте перегрузку методов сложения и умножения комплексных чисел. Проверьте работу проекта.
# Для этого создаёте экземпляры класса (комплексные числа),
# выполните сложение и умножение созданных экземпляров. Проверьте корректность полученного результата.

class Complex:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __add__(self, other):
        print(f'sum of z1 и z2 is ')
        return f'z3 = {self.a + other.a} + {self.b + other.b} * i'

    def __mul__(self, other):
        print(f'mul of z1 и z2 is')
        return f'z3 = {self.a * other.a - (self.b * other.b)} + {self.b * other.a + self.a*other.b} * i'

    def __str__(self):
        return f'{self.a} + {self.b} * i'


z1 = Complex(-1, 2)
z2 = Complex(3, 4)
print('z1 = ', z1)
print('z2 = ', z2)
print(z1 + z2)
print(z1 * z2)