"""
Сущность, отвечающая за храние и предоставление данных
Оно хранит пользователей, календари и события.
Хранение в том числе означает сохранение между сессиями в csv файлах
(пароли пользователей хранятся как hash)

Должен быть статическим или Синглтоном

*) Нужно хранить для каждого пользователя все события которые с нима произошли но ещё не были обработаны.
"""

from Event import Event
from User import User
from Calendar import Calendar
from datetime import datetime
import csv
from Utils import str_to_date

class Backend:
    list_users = []   # храним объекты класса User
    list_events = []   # храним объекты класса Event
    list_calendars = []   # храним объекты класса Calendar
    _directory = "data/"  # директория для хранения данных, при тестах переменная меняется

    @staticmethod
    def add_user(user):
        "Добавляет пользователя"
        Backend.list_users.append(user)

    @staticmethod
    def originality_login(new_login):
        "Проверяем логин на уникальность"
        Backend.load_file_users(new_login)
        if len(Backend.info_users()) == 0:
            return True
        else:
            return False

    @staticmethod
    def info_users():
        "Возвращает информацию об пользователях"
        return Backend.list_users

    @staticmethod
    def add_event(event):
        "Добавляет событие"
        Backend.list_events.append(event)

    @staticmethod
    def info_events():
        "Возвращает информацию о событиях"
        return Backend.list_events

    @staticmethod
    def add_calendar(calendar):
        "Добавляет календарь"
        Backend.list_calendars.append(calendar)

    @staticmethod
    def add_event_into_calendar(target_id_calendar, target_id_event):
        "Добавляет событие в календарь"
        for elem in Backend.list_calendars:  # ищем нужный календарь для добавления
            if target_id_calendar == elem.info_calendars()[0]:
                our_calendar = elem  # в переменную поместить из памяти требуемый календарь
                break
        our_calendar.add_event(target_id_event)  # добавить событие в календарь
        Backend.load_file_calendars()  # загрузить в память все календари
        for i in range(len(Backend.list_calendars)):  # ищем календарь для изменения
            if target_id_calendar == Backend.list_calendars[i].info_calendars()[0]:
                Backend.list_calendars[i] = our_calendar  # обновить изменяемый календарь
                break
        Backend.save_file_calendars()  # выгрузить все календари на диск


    @staticmethod
    def info_calendars():
        "Возвращает информацию о календарях"
        return Backend.list_calendars

    @staticmethod
    def save_file_users(add_user=None):
        """Создает файл с информацией о пользователях
           Если в переменную add_user мы ничего не передали, то файл записываем, иначе добавляем информацию об User"""
        file_name = Backend._directory + 'saved_users.txt'
        if add_user is None:
            file_mode = "w"
        else:
            file_mode = "a"
        with open(file_name, file_mode, newline="") as f:
            w = csv.DictWriter(f, ["id", "name", "lastname", "login", "password"])
            if file_mode == "w":  # чтобы не повторял заголовок, когда добавляем новую информацию
                w.writeheader()
            users = Backend.info_users()
            for user in users:
                info = user.info_User()
                data = dict()
                data['id'] = info[0]
                data['name'] = info[1]
                data['lastname'] = info[2]
                data['login'] = info[3]
                data['password'] = info[4]
                w.writerow(data)

    @staticmethod
    def load_file_users(target_login=None):
        """
        Загружаем пользователей из файла
        Если в переменную target_login передали искомый логин, то загружаем пользователя с данным логином
        Иначе загружаем всех пользователей
        """
        file_name = Backend._directory + 'saved_users.txt'
        Backend.clear_users()
        with open(file_name, "r") as f:
            w = csv.DictReader(f, ["id", "name", "lastname", "login", "password"])
            next(w)  # чтобы переместить курсор на следующую строку и пропустить заголовок
            id_users = []
            for i in w:
                user = User(login=i["login"], hash_pass=i["password"], name=i["name"], lastname=i["lastname"], id=i["id"])
                if target_login is None:
                    Backend.add_user(user)
                elif i["login"] == target_login:
                    Backend.add_user(user)

                "Ищем максимальный id среди всех записей для обновления id_counter, чтобы логин был точно уникальным"
                id = i["id"]
                position = id.find("*")
                position_id = position + 1
                id_users.append(int(id[position_id:]))
            maxsimum = max(id_users) + 1
            User.change_id_counter(maxsimum)

    @staticmethod
    def save_file_events(add_event=None):
        """Создает файл с информацией о событиях. События берет из памяти backend
        Если в переменную add_event мы ничего не передали, то файл записываем, иначе добавляем информацию об Event"""
        file_name = Backend._directory + 'saved_events.txt'
        if add_event is None:
            file_mode = "w"
        else:
            file_mode = "a"
        with open(file_name, file_mode, newline="") as f:
            w = csv.DictWriter(f, ["id", "name_event", "description", "data_event", "repeat_type", "event_owner", "guests"])
            if file_mode == "w":
                w.writeheader()
            events = Backend.info_events()
            for event in events:
                info = event.info_Event()
                data = dict()
                data['id'] = info[0]
                data['name_event'] = info[1]
                data['description'] = info[2]
                data['data_event'] = info[3]
                data['repeat_type'] = info[4]
                data['event_owner'] = info[5]
                data['guests'] = info[6]
                w.writerow(data)

    @staticmethod
    def load_file_events(target_id_events=None):
        """ Загружаем события из файла
        Входящий параметр или None, или list
        Если в переменную target_id_event передали искомый/ые id, то загружаем событие с данным/ными id
        Иначе загружаем все события"""
        file_name = Backend._directory + 'saved_events.txt'
        Backend.clear_events()
        with open(file_name, "r") as f:
            w = csv.DictReader(f, ["id", "name_event", "description", "data_event", "repeat_type",
                                   "event_owner", "guests"])
            next(w)
            id_events = []
            for i in w:
                event = Event(name_event=i["name_event"], description=i["description"], event_owner=i['event_owner'],
                              guests=eval(i["guests"]), data_event=i['data_event'], repeat_type=i["repeat_type"], id=i["id"])
                if target_id_events is None:
                    Backend.add_event(event)
                elif int(i["id"]) in target_id_events:
                    Backend.add_event(event)
                id = i["id"]
                id_events.append(int(id))
            maxsimum = max(id_events) + 1
            Event.change_id_counter(maxsimum)

    @staticmethod
    def save_file_calendars(add_calendar=None):
        """Создает файл с информацией о календарях
        Если в переменную add_calendar мы ничего не передали, то файл записываем, иначе добавляем информацию об calendar"""
        file_name = Backend._directory + 'saved_calendars.txt'
        if add_calendar is None:
            file_mode = "w"
        else:
            file_mode = "a"
        with open(file_name, file_mode, newline="") as f:
            w = csv.DictWriter(f, ["id", "name_calendar", "id_user", "id_events"])
            if file_mode == "w":
                w.writeheader()
            calendars = Backend.info_calendars()
            for calendar in calendars:
                info = calendar.info_calendars()
                data = dict()
                data['id'] = info[0]
                data['name_calendar'] = info[1]
                data['id_user'] = info[2]
                data['id_events'] = info[3]
                w.writerow(data)

    @staticmethod
    def load_file_calendars(target_id_user=None):
        """Загружаем календарь из файла
        Если в переменную target_id_user передали искомый id, то загружаем календарь пользователя с данным id
        Иначе загружаем все календари"""
        file_name = Backend._directory + 'saved_calendars.txt'
        Backend.clear_calendars()
        with open(file_name, "r") as f:
            w = csv.DictReader(f, ["id", "name_calendar", "id_user", "id_events"])
            next(w)
            id_calendars = []
            for i in w:
                calendar = Calendar(id=i["id"], id_user=i["id_user"], name_calendar=i['name_calendar'],
                              id_events=eval(i["id_events"]))
                if target_id_user is None:
                    Backend.add_calendar(calendar)
                elif i["id_user"] == target_id_user:
                    Backend.add_calendar(calendar)
                "Ищем максимальный id среди всех записей для обновления id_counter, чтобы id календаря был точно уникальным"
                id = i["id"]
                id_calendars.append(int(id))
            maxsimum = max(id_calendars) + 1
            Calendar.change_id_counter(maxsimum)

            """"Ищем максимальный id среди всех записей для обновления id_counter, чтобы логин был точно уникальным"
                id = i["id"]
                position = id.find("*")
                position_id = position + 1
                id_users.append(int(id[position_id:]))
            maxsimum = max(id_users) + 1
            User.change_id_counter(maxsimum)"""


    @staticmethod
    def clear_users():
        "Очищаем список пользователей"
        Backend.list_users = []

    @staticmethod
    def update_user(target_login, new_name=None, new_lastname=None, new_password=None):
        """
        Метод обновления пользователя:
        """
        """Алгоритм обновления пользователя:
                1) загрузить в память изменяемого пользователя,
                2) изменить пользователя и сохранить его в отдельную переменную,
                3) очистить память и загрузить всех пользователей,
                4) обновить изменяемого пользователя,
                5) выгрузить всех пользователей на диск
                """
        Backend.load_file_users(target_login)  # загрузить в память изменяемого пользователя
        our_user = Backend.list_users[0]   # сохранить его в отдельную переменную
        our_user.change_user(new_name, new_lastname, new_password)   # изменить пользователя
        Backend.load_file_users()   # загрузить всех пользователей
        for i in range(len(Backend.list_users)):  # ищем пользователя для изменения
            if target_login == Backend.list_users[i].info_User()[3]:
                Backend.list_users[i] = our_user     # обновить изменяемого пользователя
                break
        Backend.save_file_users()    # выгрузить всех пользователей на диск

    @staticmethod
    def clear_calendars():
        "Очищаем список календарей"
        Backend.list_calendars = []

    @staticmethod
    def clear_events():
        "Очищаем список событий"
        Backend.list_events = []

    @staticmethod
    def update_calendar(target_id_calendar, new_name_calendar):
        "Метод обновления имени календаря"
        for elem in Backend.list_calendars:
            if target_id_calendar == elem.info_calendars()[0]:
                our_calendar = elem  # В переменную поместить из памяти требуемый календарь
                break
        our_calendar.change_name(new_name_calendar)  # Обновить имя у календаря
        Backend.load_file_calendars()  # Загрузить в память все календари
        for i in range(len(Backend.list_calendars)):  # ищем календарь для изменения
            if target_id_calendar == Backend.list_calendars[i].info_calendars()[0]:
                Backend.list_calendars[i] = our_calendar  # обновить изменяемый календарь
                break
        Backend.save_file_calendars()  # выгрузить все календари на диск

    @staticmethod
    def check_id_calendar(target_id_calendar):
        "Проверяем присутствие id календаря в памяти"
        for elem in Backend.list_calendars:
            if target_id_calendar == elem.info_calendars()[0]:
                return True
        return False

    @staticmethod
    def check_id_users(target_id_users: list):
        "Проверяем присутствие id пользователей в памяти"
        if len(target_id_users) == 0:  # если передали пустой список, то False
            return False
        else:
            list_id_user = []
            for elem in Backend.list_users:
                list_id_user.append(elem.info_id_User())
            result = all(elem in list_id_user for elem in target_id_users)
        return result

    @staticmethod
    def show_events(target_id_calendar):
        "Поиск событий календаря"
        for elem in Backend.list_calendars:
            if target_id_calendar == elem.info_calendars()[0]:
                our_calendar = elem  # В переменную поместить из памяти требуемый календарь
                break
        our_events = our_calendar.info_events()  # список всех событий нашего календаря
        Backend.load_file_events(our_events)  # загружаем из файла эти события в память
        result = Backend.info_events()
        return result


    @staticmethod
    def search_events(data_from: datetime, data_to: datetime, target_id_calendar):
        "Поиск событий из промежутка времени"
        """
        Алгоритм:
        1) На вход поступает диапазон дат и id календаря, в котором искать события из промежутка
        2) В памяти уже должен быть календарь загружен, так как в интерфейсе вопрос - в каком календаре будем смотреть
        3) По id календаря, смотрим его в памяти и обращаемся в переменную со списком событий
        4) Загружаем из файла эти события в память
        5) В цикле проходимся по списку событий, выбирая каждое событие
        6) Cобытие надо выбрать, учитывая два условия:
          а) у события нет повторения - если событие попадает в наш диапазон,добавлем его в список для вывода
          б) у события есть повторение - смотрим события, у которых дата меньше или равна началу
             нашего диапазона. И начинаем в цикле выбирать у события дату: если совпало, то в список вставляем.
             Прерываем, если вычисленная дата больше верхней границы диапазона. 
        В списке для вывода: все поля этого события, а в части даты: если без повторения, то исходную дату, а если
         повторение, то вычисленную дату.
        7) Возвращаем обратно список событий
        """

        Backend.show_events(target_id_calendar)  # возвращаем события календаря
        list_search_events = []   # список событий из нужного временного диапазона
        data_from = str_to_date(data_from)
        data_to = str_to_date(data_to)
        for elem in Backend.info_events():  # в цикле проходимся по списку событий, выбирая каждое событие
            if elem.info_Event()[4] == "N" and (data_from <= str_to_date(elem.info_Event()[3]) <= data_to):
                list_search_events.append(elem.info_Event)
            elif (elem.info_Event()[4] in ["D", "W", "M", "Y"]) and (str_to_date(elem.info_Event()[3]) <= data_to):
                for calculated_data in elem.repeat_events():
                    print(calculated_data)
                    if data_from <= calculated_data <= data_to:
                        info_with_new_date = (elem.info_Event()[0], elem.info_Event()[1], elem.info_Event()[2],
                                              calculated_data, elem.info_Event()[4], elem.info_Event()[5],
                                              elem.info_Event()[6])
                        list_search_events.append(info_with_new_date)

                    elif calculated_data > data_to:
                        break
        return list_search_events


    @staticmethod
    def add_event_into_calendar_guest(add_id_event, guests: list):  # список id гостей
        "Добавление события в календарь гостей"
        """
        Алгоритм добавления событий в календари гостей
        1) Загружаем в память все календари
        2) Проходим по списку календарей и ищем первый календарь каждого гостя
            а) запускаем цикл по id приглашенных гостей
            б) как только нашли первый календарь, то добавляем id события в него.
            в) добавляем нотификацию из id пользователя, id события и C\D события
            г) делаем брейк"""

        Backend.load_file_calendars()  # загрузить в память все календари
        lst_cal = Backend.list_calendars
        for gst in guests:  # проходим по списку гостей
            for cal in lst_cal:  # проходим по списку календарей
                if cal.info_id_user() == gst:
                    Backend.add_event_into_calendar(cal.info_calendars()[0], add_id_event)
                    #TODO: нотификация
                    break




if __name__ == "__main__":
    Backend.load_file_users()
    user1 = User("lisenok", "Olesya", "Shevlyakova", "12345")
    # Backend.add_user(user1)
    user2 = User("lis", "Maksim", "Bazhin", "Bazhin")
    # Backend.add_user(user2)
    # print(Backend.info_users())
    # print(user1)
    # day1 = Event("party", 'вечеринка', user1.info_id_User(),  user2.info_id_User(), datetime(2007, 12, 6, 15, 29))
    # Backend.add_event(day1)
    # day2 = Event("birthday", 'День рождения', user1.info_id_User(),  user2.info_id_User(), datetime(2024, 4, 5))
    # Backend.add_event(day2)
    # # print(Backend.info_events())
    # cal1 = Calendar(user1.info_id_User())
    # cal1.add_event(day1.info_id_event())
    # cal1.add_event(day2.info_id_event())
    # print(cal1.info_events())
    # print(cal1)
    # print(Backend.info_users())
    # Backend.save_file_users()user()
    # Backend.load_file_users()
    # user3 = User("lisen", "12345", "Dasha", "Shev")
    # Backend.add_user(user3)
    # print(Backend.info_users())
    # user4 = User("lis", "12345", "Maksim", "Bazhin")
    # Backend.add_user(user4)
    # print(Backend.info_users())
    user1 = User("lisenok", "Olesya", "Shevlyakova", "12345")
    # Backend.add_user(user1)
    # Backend.save_file_users()
    # print(user1.info_User())
    day1 = Event("party", 'вечеринка', user1.info_id_User(), [user2.info_id_User()], datetime(2007, 12, 6, 15, 29))
    Backend.add_event(day1)
    # Backend.save_file_events()
    # Backend.load_file_events()
    # cal1 = Calendar("@OlesyaShevlyakova*1", "work")
    # cal1.add_event(day1.info_id_event())
    # Backend.add_calendar(cal1)
    # Backend.save_file_calendars()
    # Backend.load_file_calendars()
    # print(Backend.info_calendars())
    # cal2 = Calendar("@OlesyaShev*1", "home")
    # cal2.add_event(day1.info_id_event())
    # Backend.add_calendar(cal2)
    # print(Backend.info_calendars())
    # Backend.save_file_calendars()
    # Backend.load_file_calendars()
    # print(Backend.info_calendars())
    user2 = User("lis", "Olesya", "Shevlyakova", "123")
    Backend.add_user(user2)
    Backend.save_file_users()





