#1 Пользователь вводит время в секундах.
# Переведите время в часы, минуты, секунды и выведите в формате чч:мм:сс.
# Используйте форматирование строк.
import datetime

time_sec = input('time in seconds:')
time_sec = int(time_sec)
hour = time_sec // 3600
min = time_sec % 3600 // 60
sec = time_sec % 3600 % 60
res = datetime.time(hour,min,sec)
print (res)