#Если фирма отработала с прибылью, вычислите рентабельность выручки.
#Это отношение прибыли к выручке.
#Далее запросите численность сотрудников фирмы и определите прибыль фирмы в расчёте на одного сотрудника.

earn = int(input('enter earning amount:'))
cost = int(input('enter cost amount:'))
if earn > cost:
    profit = earn - cost
    print('return on revenue = ', profit/earn)
    employee = int(input('enter number of employees:'))
    profitEmp = profit/employee
    print('profit per employee: ', profitEmp)
else: print('company is unprofitable')

