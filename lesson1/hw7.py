#Спортсмен занимается ежедневными пробежками. В первый день его результат составил a километров.
#Каждый день спортсмен увеличивал результат на 10% относительно предыдущего.
#Требуется определить номер дня, на который результат спортсмена составит не менее b километров.
#Программа должна принимать значения параметров a и b и выводить одно натуральное число — номер дня.

a_km = int(input('enter first distance:'))
b_km = int(input('enter second distance:'))
day = 1
while a_km < b_km:
    day = day + 1
    print(day)
    a_km = round(a_km + a_km*0.1,2)
    print(a_km)
print('day', day)


