#Необходимо построчно прочитать файл, вычислить прибыль каждой компании, а также среднюю прибыль.
# Если фирма получила убытки, в расчёт средней прибыли её не включать.
# Далее реализовать список.
# Он должен содержать словарь с фирмами и их прибылями, а также словарь со средней прибылью.
# Если фирма получила убытки, также добавить её в словарь (со значением убытков).

from statistics import mean
import json

dict = {}
dict_profit = {}
dict_avg_prft = {}
dict_else = {}
with open("firm.txt") as text:
    for line in text:
        line_text = line.split()
        dict[line_text[0]] = line_text[1:]
    print(dict)
    for name, value in dict.items():
        gain = int(value[1])
        loss = int(value[2])
        profit = gain - loss
        if profit > 0:
            dict_profit[name] = profit
        else:
            dict_else[name] = profit
    print(dict_profit)
    print(dict_else)
    dict_avg_prft = {}
    dict_avg_prft['avg_prft: '] = mean(list(dict_profit.values()))
    print(dict_avg_prft)
    dict_profit.update(dict_else)
    print(dict_profit)
    my_list = []
    my_list.append(dict_profit)
    my_list.append(dict_avg_prft)
    print(my_list)
    result_dict = {}
    result_dict['text'] = my_list
with open("my_file.json", "w") as ff:
    json.dump(result_dict, ff)




