#Запросите у пользователя значения выручки и издержек фирмы.
#Определите, с каким финансовым результатом работает фирма.
#Например, прибыль — выручка больше издержек, или убыток — издержки больше выручки.
#Выведите соответствующее сообщение.

earn = int(input('enter earning amount:'))
cost = int(input('enter cost amount:'))
if earn > cost:
    print('company is profitable')
elif cost > earn:
    print('company is unprofitable')
else: print('zero profit')