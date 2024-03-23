"""
Класс календаря - хранит события.
он умеет искать все события из промежутка (в том числе повторяющиеся)
он умеет добавлять/удалять события.
У каждого календаря ровно один пользователь.
"""
from Event import Event
from datetime import datetime


class Calendar:
    _id_user = None
    _name_calendar = None
    _events = []  # хранит id events
    _id = None  # id номер календаря
    __id_counter__ = 1  # счетчик для гарантии уникальности id

    def __init__(self, id_user, name_calendar: str, id=None, id_events=None):
        """
        :param id: заполняется при загрузке из файла, иначе генерируется
        :param id_events: заполняется при загрузке из файла, иначе пустое
        """
        self._id_user = id_user
        self._name_calendar = name_calendar
        if id_events is not None:
            self._events = id_events
        else:
            self._events = []
        if id is None:
            self._id = self.__class__.__id_counter__  # присвоили id новому событию
            self.__class__.__id_counter__ += 1  # увеличили инкрементальный id
            self._id = str(self._id)
        else:
            self._id = str(id)

    @staticmethod
    def change_id_counter(new_counter):
        "Изменение id_counter"
        Calendar.__id_counter__ = new_counter

    def info_events(self):
        "Возвращает информацию о событиях календаря"
        return (self._events)

    def info_id_user(self):
        "Возвращает информацию об id пользователя календаря"
        return (self._id_user)

    def info_calendars(self):
        "Возвращает информацию о календаре"
        return (self._id, self._name_calendar, self._id_user, self._events)

    def change_name(self, new_name):
        "Изменение имени календаря"
        self._name_calendar = new_name

    def add_event(self, event):
        "Добавляет событие в календарь"
        self._events.append(event)

    def delete_event(self, event):
        "Удаляет событие из календаря"
        self._events.remove(event)

    def __str__(self):
        "Возвращает информацию для пользователя"
        return f"Календарь {self._id}, наменование календаря {self._name_calendar}, пользователя {self._id_user}"

    def __repr__(self):
        "Возвращает информацию для разработчика"
        return f"[{self._id}:{self._id_user}]"




