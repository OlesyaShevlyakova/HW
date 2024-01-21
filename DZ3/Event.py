"""
Описывает некоторе "событие" - промежуток времени с присвоенными характеристиками
У события должно быть описание, название и список участников
Событие может быть единожды созданым
Или периодическим (каждый день/месяц/год/неделю)

Каждый пользователь ивента имеет свою "роль"
организатор умеет изменять названия, список участников, описание, а так же может удалить событие
участник может покинуть событие

запрос на хранение в json
Уметь создавать из json и записывать в него

Иметь покрытие тестами
Комментарии на нетривиальных методах и в целом документация
"""

import json
from datetime import datetime

class Event:
    _description = None   # описание события
    _name_event = None    # название события
    _event_owner = None    # создатель события
    _event_guests = []  # участники события
    _repeat_type = None   # периодичность события - D W M Y
    _data_event = None    # дата события
    _id = None   # id номер события
    __id_counter__ = 1

    def __init__(self, name_event: str, description: str, event_owner: str, guests: list, data_event: datetime,
                 repeat_type=None, id=None):
        self._name_event = name_event
        self._description = description
        self._event_owner = event_owner
        self._event_guests = guests
        self._repeat_type = repeat_type
        self._data_event = data_event
        if id is None:
            self._id = self.__class__.__id_counter__  # присвоили id новому событию
            self.__class__.__id_counter__ += 1  # увеличили инкрементальный id
        else:
            self._id = id

    def info_Event(self):
        "Возвращает информацию о Event"
        return (self._id, self._name_event, self._description, self._data_event, self._repeat_type, self._event_owner,
                self._event_guests)

    def info_data_event(self):
        "Возвращает информацию о дате Event"
        return (self._data_event)

    def info_id_event(self):
        "Возвращает информацию об id Event"
        return (self._id)

    def change_name_event(self, new_name_event):
        "Замена названия Event"
        self._name_event = new_name_event

    def change_description(self, new_description):
        "Замена описания Event"
        self._description = new_description

    def add_list_users(self, new_guests: list):
        "Добавляет список участников в Event"
        for elem in new_guests:
            if elem not in self._event_guests:
                self._event_guests.append(elem)

    def remove_list_guests(self, del_guests: list):
        "Удаляет список участников в Event"
        for elem in del_guests:
            if elem in self._event_guests:
                self._event_guests.remove(elem)

    def get_json(self):
        "Создаем json"
        # создаем словарь
        mydict = {"name_event": self._name_event, "data_event": str(self._data_event), "description": self._description,
                  "event_owner": self._event_owner, "guests": self._event_guests, "repeat_type": self._repeat_type}
        # сериализуем его в JSON-структуру, как строку
        stroka = json.dumps(mydict)
        return stroka

    def take_json(self, new_json):
        "Получение информации из json и обновление данных Event"
        # проводим десериализацию JSON-объекта
        new_dict = json.loads(new_json)
        self._name_event = new_dict["name_event"]
        self._data_event = new_dict["data_event"]
        self._description = new_dict["description"]
        self._event_owner = new_dict["event_owner"]
        self._event_guests = new_dict["guests"]
        self._repeat_type = new_dict["repeat_type"]

    def __str__(self):
        "Возвращает информацию для пользователя"
        return f"Название события {self._name_event} с id {self._id}"

    def __repr__(self):
        "Возвращает информацию для разработчика"
        return f"[{self._id}:{self._name_event}]"

    @staticmethod
    def change_id_counter(new_counter):
        "Изменение id_counter"
        Event.__id_counter__ = new_counter


if __name__ == "__main__":
    Day = Event("birthday", "party day", "olesya", ["maksim", "grisha"],
                datetime(2007, 12, 6, 15, 29, 43))
    Day.remove_list_guests(["maksim"])
    print(Day._event_guests)
    print(Day.info_Event())
    print(Day.get_json())
    print('123')
    print(Day.take_json('{"name_event": "birthday", "data_event": "2007-12-06 15:29:43", "description": "party day", "event_owner": "olesya", "guests": ["grisha"], "repeat_type": null}'))
    print(Day.info_Event())



