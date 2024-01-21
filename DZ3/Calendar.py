"""
Класс календаря - хранит события.
он умеет искать все события из промежутка (в том числе повторяющиеся)
он умеет добавлять/удалять события.
У каждого календаря ровно один пользователь.
"""
from Event import Event
from datetime import datetime

# TODO: написать функцию обработки повторения события

class Calendar:
    _id_user = None
    _name_calendar = None
    _events = []
    _id = None  # id номер календаря
    __id_counter__ = 1

    def __init__(self, id_user, name_calendar: str, id=None, id_events=None):
        self._id_user = id_user
        self._name_calendar = name_calendar
        if id_events is not None:
            self._events = id_events
        if id is None:
            self._id = self.__class__.__id_counter__  # присвоили id новому событию
            self.__class__.__id_counter__ += 1  # увеличили инкрементальный id
        else:
            self._id = id

    @staticmethod
    def change_id_counter(new_counter):
        "Изменение id_counter"
        Calendar.__id_counter__ = new_counter

    def info_events(self):
        "Возвращает информацию о событиях календаря"
        return (self._events)

    def info_calendars(self):
        "Возвращает информацию о календаре"
        return (self._id, self._name_calendar, self._id_user, self._events)

    def change_name(self, new_name):
        "Изменение имени календаря"
        self._name_calendar = new_name

    def search_events(self, data_from: datetime, data_to: datetime):
        "Поиск событий из промежутка времени"
        list_events = []
        for elem in self._events:
            data_of_event = elem.info_data_event()
            if data_from <= data_of_event <= data_to:
                list_events.append(elem)
        return list_events

    def add_event(self, event):
        "Добавляет событие в календарь"
        self._events.append(event)

    def delete_event(self, event):
        "Удаляет событие из календаря"
        self._events.remove(event)

    def __str__(self):
        "Возвращает информацию для пользователя"
        return f"Календарь {self._id}, пользователя {self._id_user}"

    def __repr__(self):
        "Возвращает информацию для разработчика"
        return f"[{self._id}:{self._id_user}]"

    def repeat_events(self):
        "Метод обработки повторения события" #TODO
        pass


if __name__ == "__main__":
    A = Calendar("123454")
    Event1 = Event("birthday", "party day", "olesya", ["maksim", "grisha"], datetime(2008, 12, 6, 15, 29, 43))
    Event2 = Event("birthday", "party day", "olesya", ["maksim", "grisha"], datetime(2009, 12, 6, 15, 29, 43))
    Event3 = Event("birthday", "party day", "olesya", ["maksim", "grisha"], datetime(2010, 12, 6, 15, 29, 43))
    A.add_event(Event1)
    A.add_event(Event2)
    A.add_event(Event3)
    print(A.search_events(datetime(2000, 12, 6, 15, 29, 43), datetime(2009, 12, 6, 15, 29, 43)))

