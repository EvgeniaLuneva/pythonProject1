#Создать текстовый файл (не программно).
# Построчно записать фамилии сотрудников и величину их окладов (не менее 10 строк).
# Определить, кто из сотрудников имеет оклад менее 20 тысяч, вывести фамилии этих сотрудников.
# Выполнить подсчёт средней величины дохода сотрудников.
from statistics import mean
dict = {}
with open("empl.txt") as text:
    for line in text:
        dict[line.split()[0]] = int(line.split()[1])
for i, j in dict.items():
    if j < 20000:
        print(i)
sal_avg = mean(list(dict.values()))
print('average salary: ', round(sal_avg,2))

