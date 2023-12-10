from datetime import datetime
from item import Item


class Hub():
    _instance = None

    def __new__(cls, items=None, date=datetime.now(), hub=None, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kwargs)
            cls._instance._initialized = False  # вводим флаг, чтобы определять мы уже инициализировались или нет, без него при создании нового объекта выполняется init и теряются данные предыдущего объекта
        return cls._instance

    def __init__(self, items=None, date=datetime.now(), hub=None):
        if self._initialized == False:  # проверяем флаг
            if items is None:
                items = []
            self.items = items
            self._date = date
            self.hub = hub
            self._initialized = True
        else:
            return

    def add_item(self, *args):
        "Добавляет новый items в Hub"
        for elem in args:
            if isinstance(elem, Item):  # проверяем, что item действительно является типо Item или его наследником
                self.items.append(elem)

    def info_Hub(self):
        "Выводит информацию о Hub"
        return (self.items, self._date, self.hub)

    def __call__(self, y):
        "Возвращает items по индексу при обращении как к функции"
        if y < len(self.items):
            return self.items[y]
        else:
            return ("Нет такого элемента")

    def __repr__(self):
        "Возвращает информацию для разработчика"
        return self.items[0:3]

    def __len__(self):
        "Возвращает количество items в Hub"
        return len(self.items)

    def __str__(self):
        "Возвращает информацию для пользователя"
        return "название склада {}".format(self.hub)

    def __getitem__(self, i):
        "Возвращает items по индексу при обращении как к итерируемому элементу"
        return self.items[i]

    def find_by_id(self, id):
        "Ищет элемент по id и возвращает информацию по нему"
        for pos in range(len(self.items)):
            if self.items[pos]._id == id:
                return (pos, self.items[pos])
            else:
                return (-1, None)

    def find_by_tags(self, find_tag):
        "Ищет объекты с требуемыми tags"
        new_list = []
        set_of_find_tag = set(find_tag)
        for elem in self.items:
            if set_of_find_tag.issubset(
                    elem.tags):  # проверка на наличие, что множество искомых tags является подмножеством tags объекта
                new_list.append(elem)
        return new_list

    def rm_item(self, elem):
        "Удаляет item с id=elem или удаляет item=elem"
        if isinstance(elem, int) and self.find_by_id(elem) != (-1, None):  # проверяем elem на тип
            position, obj = self.find_by_id(elem)                          # int и на наличие данного id в нашем items
            self.items.pop(position)  # удаляем item с id=elem
        elif isinstance(elem, Item) and (elem in self.items):
            self.items.remove(elem)
        else:
            print("Данного id или элемента item не существует")
            return None

    def drop_items(self, items_for_del):
        "Удаляет все товары из Hub, которые содержатся в items"
        new_items = [x for x in self.items if x not in items_for_del]
        self.items = new_items

    def clear(self):
        "Полностью очищает весь контейнер items"
        self.items.clear()

    @property
    def date(self):
        "Получение даты из хаба"
        return self._date

    @date.setter
    def date(self, value):
        "Установка даты в хабе"
        self._date = value

    def find_by_date(self, *args):
        "Возвращает лист всех Item, подходящих по дате"
        out_list = []
        if len(args) == 1:
            for elem in self.items:
                if elem.dispatch_time <= args[0]:
                    out_list.append(elem)
            return out_list
        elif len(args) == 2:
            for elem in self.items:
                if args[0] <= elem.dispatch_time <= args[1]:
                    out_list.append(elem)
            return out_list
        else:
            raise Exception("not found")

    def find_most_valuable(self, amount=1):
        "Возвращает первые amount самых дорогих предметов на складе или все"
        cost_list = []
        new_lst = []
        for elem in self.items:
            cost_list.append((elem, elem._cost))
        sorted_cost_list = sorted(cost_list, key=lambda price: price[1], reverse=True)  # сортировка по цене в tuple
        "КАК МОЖНО ОПТИМИЗИРОВАТЬ БЛОК, ИДУЩИЙ НИЖЕ?"
        if amount <= len(cost_list):
            res = sorted_cost_list[: amount]
        else:
            res = sorted_cost_list[:]
        for elem in res:  # для возвращения объектов без цены
            new_lst.append(elem[0])
        return new_lst