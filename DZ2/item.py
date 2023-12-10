import random
from datetime import datetime


class Item:
    def __init__(self, name=None, discryption=None, dispatch_time=None, tags=None, cost=None):
        self._cost = cost
        rand_str1 = str(datetime.now()) + str(random.randint(0, 10000))  # генерируем уникальный hash для id
        if hash(rand_str1) < 0:  # если hash получается отрицательный, делаем положительный, чтобы id был положительным
            self._id = hash(rand_str1) * (-1)
        else:
            self._id = hash(rand_str1)
        self.name = name
        self.discryption = discryption
        self.dispatch_time = dispatch_time
        if tags is None:
            tags = []
        self.tags = tags

    def info_Item(self):
        "Выводит информацию о Item"
        return (self._id, self.name, self.discryption, self.dispatch_time, self.tags, self._cost)

    def add_tag(self, new_tag):
        "Добавление tags в Items"
        if new_tag not in self.tags:
            self.tags.append(new_tag)

    def rm_tag(self, *args):  #
        "Удаление tags в Items"
        for elem in args:
            if elem in self.tags:
                self.tags.remove(elem)
            else:
                print(elem, "- данного tag не существует")

    def __repr__(self):
        "Возвращает информацию для разработчика"
        str_repr = str(self.tags[0:3]) + str(self._id)
        return str_repr

    def __str__(self):
        "Возвращает информацию для пользователя"
        return "имя объекта {}, описание объекта {}, дата отгрузки {}, цена {} и тэги {}".format(self.name, self.discryption, self.dispatch_time, self._cost, self.tags)

    def __len__(self):
        "Возвращает количество tags в Item"
        return len(self.tags)

    def set_cost(self, new_cost):
        "Устанавливает новую цену объекта"
        self._cost = new_cost

    def get_cost(self):
        "Возвращает цену объекта"
        return self._cost

    def __lt__(self, other):
        "Определяет больший объект"
        return self._cost < other._cost

    def add_tags(self, *tags):
        "Добавляет несколько tags"
        self.tags += list(tags)

    def rm_tags(self, *tags):
        "Удаляет несколько tags"
        list_tags = list(tags)
        new_list = [x for x in self.tags if x not in list_tags]
        self.tags = new_list

    def is_tagged(self, *find_tags):
        "Проверка на наличие, что введенные tags присутствуют в tags объекта"
        set_of_find_tag = set(find_tags)
        return set_of_find_tag.issubset(set(self.tags))

    def copy(self):
        "Создает копию существующего объекта, но с другим id"
        new_item = Item(name=self.name, discryption=self.discryption, cost=self._cost)
        return new_item

