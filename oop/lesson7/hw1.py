# Реализовать класс Matrix (матрица). Обеспечить перегрузку конструктора класса (метод __init__()),
# который должен принимать данные (список списков) для формирования матрицы.
#Следующий шаг — реализовать перегрузку метода __str__() для вывода матрицы в привычном виде.
# Далее реализовать перегрузку метода __add__() для реализации операции сложения двух объектов класса Matrix
# (двух матриц). Результатом сложения должна быть новая матрица.


class Matrix:
    def __init__(self, matrix):
        self.matrix = matrix

    def __str__(self):
        text = ''
        for i in self.matrix:
            for j in i:
                text += str(j) + ' '
            text += '\n'
        return text

    def __getitem__(self, index):
        return self.matrix[index]

    def __add__(self, other):
        result = ''
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                result += str(self.matrix[i][j] + other[i][j]) + ' '
            result += '\n'
        return result



m1 = [[1, 2, 3, 4], [5, 3, 5, 4], [5, 3, 5, 4]]
m2 = [[3, 2, 3, 4], [6, 3, 5, 5], [5, 3, 5, 4]]

mat1 = Matrix(m1)
mat2 = Matrix(m2)
print(mat1)
print(mat2)
res = mat1 + mat2
print(res)






