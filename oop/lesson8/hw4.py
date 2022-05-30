#4, 5, 6
class Tech:
    def __init__(self, type_tech, price, weight):
        self.type = type_tech
        self.weight = weight
        self.price = price



class Printer(Tech):
    def __init__(self, type_tech, price, weight, model,
                 type_printer, format_paper, count_tech):
        super().__init__(type_tech, price, weight)
        self.model = model
        self.type_printer = type_printer
        self.format_paper = format_paper
        if type(count_tech) != type(1):
            while True:
                try:
                    count_tech = int(input('Enter integer number '))
                    self.count_tech = count_tech
                    break
                except ValueError:
                    continue
        else:
            self.count_tech = count_tech


class Scanner(Tech):
    def __init__(self, type_tech, price, weight, model,
                 type_scanner, format_paper, count_tech):
        super().__init__(type_tech, price, weight)
        self.model = model
        self.type_scanner = type_scanner
        self.format_paper = format_paper
        if type(count_tech) != type(1):
            while True:
                try:
                    count_tech = int(input('Enter integer number '))
                    self.count_tech = count_tech
                    break
                except ValueError:
                    continue
        else:
            self.count_tech = count_tech


class Fold:
    total_tech = {}

    def __init__(self, max_weight, sector_fold):
        self.max_weight = max_weight
        self.sector_fold = {key: [] for key in sector_fold}
        self.balance_price = 0
        self.count = 0
        self.inv_number = 100000

    def push_equipment(self, equipment):#добавляем на склад
        self.count += equipment.count_tech
        self.balance_price += equipment.price
        for _ in range(equipment.count_tech):
            self.inv_number += 1
            Fold.total_tech[self.inv_number] = equipment.__dict__

    def push_sector(self, inv_number, sector):#передача в подразделение
        tech_dict = Fold.total_tech[inv_number]
        tech_dict[sector] = inv_number
        self.sector_fold[sector].append(tech_dict)




scanner1 = Scanner('Scanner', 4000, 3, 'MDF460T', 'jet', ['A4', 'A5'], 3)#создали сканнер
fold = Fold(30000, ['T1', 'T2'])#создали склад
fold.push_equipment(scanner1)#добавилина склад екземпляр сканнера
print(Fold.total_tech)#смотрим что на складе
fold.push_sector(100001, 'T1')# добавили в подразделение, передаем инвентран. номер и название подразделения
print(fold.sector_fold)# смотрим что появилось в словаре с подразделениями подразделению