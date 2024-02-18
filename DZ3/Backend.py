"""
Сущность, отвечающая за храние и предоставление данных
Оно хранит пользователей, календари и события.
Хранение, в том числе, означает сохранение между сессиями в csv файлах
(пароли пользователей хранятся как hash)

Должен быть статическим или Синглтоном

Нужно хранить для каждого пользователя все события, которые с ними произошли, но ещё не были обработаны.
"""

from Event import Event
from User import User
from Calendar import Calendar
from Notification import Notification
from datetime import datetime
import csv
from Utils import str_to_date
from Utils import hash_password as hs

class Backend:
    list_users = []   # храним объекты класса User
    list_events = []   # храним объекты класса Event
    list_calendars = []   # храним объекты класса Calendar
    list_notification = []  # храним объекты класса Notification
    _directory = "data/"  # директория для хранения данных, при тестах переменная меняется
    '''Основной принцип работы с данными на диске
       для обеспечения одновременной работы нескольких пользователей.
          Для отображения - с диска загружаем только требуемые данные в память, отображаем и память очищаем.
          Для изменения по требованию пользователем - 
             1) с диска загружаем в переменную данные, которые нужно изменить
             2) в переменной загруженные данные меняем через диалог с пользователем
             3) загружаем в память backend данные всего файла
             4) заменяем в памяти backend изменяемые данные
             5) сохранем все данные из backend на диск 
          Для добавления - делаем аппенд данными файла на диске
       '''
    @staticmethod
    def add_user(user):
        "Добавляет пользователя"
        Backend.list_users.append(user)

    @staticmethod
    def originality_login(new_login):
        """Проверяем логин на уникальность
        True - уникальный
        False - неуникальный"""
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
    def info_notifications():
        "Возвращает информацию об уведомлениях"
        return Backend.list_notification

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
            maxsimum = max(id_users, default=0) + 1
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
                elif i["id"] in target_id_events:
                    Backend.add_event(event)
                id = i["id"]
                id_events.append(int(id))
            maxsimum = max(id_events, default=0) + 1
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
            maxsimum = max(id_calendars, default=0) + 1
            Calendar.change_id_counter(maxsimum)


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
    def check_id_users_event(target_id_users: list, target_id_event, oper):
        "Проверяем присутствие id пользователей в событии"
        if len(target_id_users) == 0:  # если передали пустой список, то False
            return False
        else:
            for elem in Backend.list_events:
                if target_id_event == elem.info_Event()[0]:
                    our_event = elem  # в переменную поместить из памяти требуемое событие
                    if oper == "any":
                        result = any(elem in target_id_users for elem in our_event.info_Event()[6])
                    elif oper == "all":
                        result = all(elem in our_event.info_Event()[6] for elem in target_id_users)
                    break
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
                    if data_from <= calculated_data <= data_to:
                        info_with_new_date = (elem.info_Event()[0], elem.info_Event()[1], elem.info_Event()[2],
                                              calculated_data, elem.info_Event()[4], elem.info_Event()[5],
                                              elem.info_Event()[6])
                        list_search_events.append(info_with_new_date)

                    elif calculated_data > data_to:
                        break
        return list_search_events


    @staticmethod
    def add_event_into_calendar_guest(add_id_event, guests: list, name_event):  # список id гостей
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
        Backend.clear_notification()   # очищаем список уведомлений
        for gst in guests:  # проходим по списку гостей
            for cal in lst_cal:  # проходим по списку календарей
                if cal.info_id_user() == gst:
                    Backend.add_event_into_calendar(cal.info_calendars()[0], add_id_event)
                    Backend.add_notification(id_user=gst, id_event=add_id_event, action="C", del_details=name_event)  # добавляем уведомление
                    Backend.save_file_notifications(add_notification=True)  # сохраняем уведомления
                    Backend.clear_notification()  # очищаем список уведомлений
                    break


    @staticmethod
    def check_id_event(target_id_event):
        "Проверяем присутствие id события в памяти"
        for elem in Backend.list_events:
            if target_id_event == elem.info_Event()[0]:
                return True
        return False

    @staticmethod
    def del_event_from_calendars(target_id_event):
        "Удаление события"
        """Алгоритм:
        1) Сохраняем в отдельную переменную гостей события
        2) Загружаем в память все события
        3) Удаляем требуемое событие (по id)
        4) Сохраняем события
        5) Загружаем в память все календари
        6) Удаляем событие из календарей
        7) Сохраняем календари"""
        Backend.clear_notification()  # очищаем список уведомлений
        for elem in Backend.list_events:
            if target_id_event == elem.info_Event()[0]:
                guests = elem.info_Event()[6]  # cохраняем в отдельную переменную гостей события
        Backend.load_file_events()  # загружаем в память все события
        for i in range(len(Backend.list_events)):
            if target_id_event == Backend.list_events[i].info_Event()[0]:
                name_event = Backend.list_events[i].info_Event()[1]
                Backend.list_events.pop(i)  # удаляем требуемое событие (по id)
                break
        Backend.save_file_events()  # сохраняем события
        Backend.load_file_calendars()  # загружаем в память все календари
        for i in range(len(Backend.list_calendars)):
            if target_id_event in Backend.list_calendars[i].info_calendars()[3]:
                Backend.list_calendars[i].info_calendars()[3].remove(target_id_event)  # удаляем событие из календарей
                Backend.add_notification(id_user=Backend.list_calendars[i].info_calendars()[2],
                                         id_event=target_id_event, action="D", del_details=name_event)  # добавляем уведомление
                Backend.save_file_notifications(add_notification=True)  # сохраняем уведомления
                Backend.clear_notification()  # очищаем список уведомлений
        Backend.save_file_calendars()  # сохраняем календари

    @staticmethod
    def move_event_from_calendars(source_id_calendar, target_id_event, target_id_calendar):
        "Перемещение события"
        """Алгоритм:
        1) Ожидаем, что календари конкретного пользователя в память уже загружены
        2) Из памяти Backend в отдельную переменную помещаем календарь (из которого перемещаем событие)
        3) Из памяти Backend в отдельную переменную помещаем календарь (в который перемещаем событие)
        4) Удаляем событие из календаря (источника) (отдельная переменная)
        5) Добавляем событие в целевой календарь (отдельная переменная)
        6) Загружаем в память все календари
        7) Проходим по списку календарей и заменяем старые календари из переменных на новые календари
        8) Сохраняем календари"""
        for elem in Backend.list_calendars:
            if source_id_calendar == elem.info_calendars()[0]:
                source_calendar = elem  # cохраняем в отдельную переменную календарь (из которого перемещаем событие)
            elif target_id_calendar == elem.info_calendars()[0]:
                target_calendar = elem  # cохраняем в отдельную переменную календарь (в который перемещаем событие)
        source_calendar.delete_event(target_id_event)  # удаляем событие из календаря (источника)
        target_calendar.add_event(target_id_event)  # добавляем событие в целевой календарь
        Backend.load_file_calendars()  # загружаем в память все календари
        for i in range(len(Backend.list_calendars)):
            if Backend.list_calendars[i].info_calendars()[0] == source_calendar.info_calendars()[0]:
                Backend.list_calendars[i] = source_calendar  # заменяем календарь
            elif Backend.list_calendars[i].info_calendars()[0] == target_calendar.info_calendars()[0]:
                Backend.list_calendars[i] = target_calendar  # заменяем календарь
        Backend.save_file_calendars()  # сохраняем календари



    @staticmethod
    def clear_notification():
        "Очищаем список уведомлений"
        Backend.list_notification = []

    @staticmethod
    def add_notification(id_user, id_event, action, del_details=None, id=None):
        "Добавляем уведомление"
        notification = Notification(id=id, id_user=id_user, id_event=id_event, action=action,
                                    del_details=del_details)
        Backend.list_notification.append(notification)

    def save_file_notifications(add_notification=None):
        """Создает файл с информацией об уведомлениях. События берет из памяти backend
        Если в переменную add_notification мы ничего не передали, то файл записываем, иначе добавляем информацию об Notification"""
        file_name = Backend._directory + 'saved_notifications.txt'
        if add_notification is None:
            file_mode = "w"
        else:
            file_mode = "a"
        with open(file_name, file_mode, newline="") as f:
            w = csv.DictWriter(f, ["id", "id_user", "id_event", "action", "del_details"])
            if file_mode == "w":
                w.writeheader()
            notifications = Backend.info_notifications()
            for notif in notifications:
                info = notif.info_Notif()
                data = dict()
                data['id'] = info[0]
                data['id_user'] = info[1]
                data['id_event'] = info[2]
                data['action'] = info[3]
                data['del_details'] = info[4]
                w.writerow(data)

    @staticmethod
    def load_file_notifications(target_id_notifications=None):
        """ Загружаем события из файла
        Входящий параметр или None, или list
        Если в переменную target_id_notificationt передали искомый/ые id, то загружаем уведомления с данным/ными id
        Иначе загружаем все уведомления"""
        file_name = Backend._directory + 'saved_notifications.txt'
        Backend.clear_notification()
        with open(file_name, "r") as f:
            w = csv.DictReader(f, ["id", "id_user", "id_event", "action", "del_details"])
            next(w)
            id_notifications = []
            for i in w:
                if target_id_notifications is None:
                    Backend.add_notification(id=i["id"], id_user=i["id_user"], id_event=i['id_event'],
                                             action=i["action"], del_details=i['del_details'])  # добавляем уведомление
                elif i["id"] in target_id_notifications:
                    Backend.add_notification(id=i["id"], id_user=i["id_user"], id_event=i['id_event'],
                                             action=i["action"], del_details=i['del_details'])  # добавляем уведомление
                id = i["id"]
                id_notifications.append(int(id))
            maxsimum = max(id_notifications, default=0) + 1
            Notification.change_id_counter(maxsimum)

    @staticmethod
    def check_id_notification(id_user):
        "Провереряем наличие оповещения для текущего пользователя"
        Backend.load_file_notifications()  # загружаем оповещения
        for elem in Backend.list_notification:
            if id_user == elem.info_Notif()[1]:
                Backend.clear_notification()
                return True
        Backend.clear_notification()
        return False

    @staticmethod
    def show_notifications_user(target_id_user):
        "Загружаем уведомления пользователя"
        Backend.load_file_notifications()  # загружаем все уведомления
        our_notif_elem_to_save = []
        our_notif_info = []
        for elem in Backend.list_notification:
            if target_id_user == elem.info_Notif()[1]:
                our_notif_info.append(str(elem))  # в переменную помещаем объекты уведомлений для залогиненного пользователя
            else:
                our_notif_elem_to_save.append(elem)  # в переменную помещаем объекты уведомлений для других пользователей
        Backend.clear_notification()  # очищаем backend
        for elem in our_notif_elem_to_save:
            Backend.list_notification.append(elem)  # в память добавляем уведомления других пользователей
        Backend.save_file_notifications()  # сохраняем уведомления других пользователей
        return our_notif_info

    def update_name_event(target_id_event, new_name_event):
        "Метод обновления названия события"
        for elem in Backend.list_events:
            if target_id_event == elem.info_Event()[0]:
                our_event = elem  # В переменную поместить из памяти требуемое событие
                break
        our_event.change_name_event(new_name_event)  # Обновить название у события
        Backend.load_file_events()  # Загрузить в память все события
        for i in range(len(Backend.list_events)):  # ищем событие для изменения
            if target_id_event == Backend.list_events[i].info_Event()[0]:
                Backend.list_events[i] = our_event  # обновить изменяемое событие
                break
        Backend.save_file_events()  # выгрузить все события на диск

    def update_description_event(target_id_event, new_description_event):
        "Метод обновления описания события"
        for elem in Backend.list_events:
            if target_id_event == elem.info_Event()[0]:
                our_event = elem  # в переменную поместить из памяти требуемое событие
                break
        our_event.change_description(new_description_event)  # обновить описание события
        Backend.load_file_events()  # загрузить в память все события
        for i in range(len(Backend.list_events)):  # ищем событие для изменения
            if target_id_event == Backend.list_events[i].info_Event()[0]:
                Backend.list_events[i] = our_event  # обновить изменяемое событие
                break
        Backend.save_file_events()  # выгрузить все события на диск

    def add_guests_in_event(target_id_event, guests: list):
        "Метод добавления гостей в событие"
        """Алгоритм:
        1) Ожидаем, что в памяти имеются события текущего пользователя
        2) В переменную помещаем требуемое событие
        3) В событие (новая переменная) добавляем новых гостей
        4) Загружаем в память все события
        5) Проходим по списку событий и заменяем старое событие из переменной на новое событие
        6) Сохраняем события
        7) Добавляем событие в календарь гостей
        """
        for elem in Backend.list_events:
            if target_id_event == elem.info_Event()[0]:
                our_event = elem  # В переменную поместить из памяти требуемое событие
                break
        our_event.add_list_users(guests)  # Добавляем новых гостей
        Backend.load_file_events()  # Загрузить в память все события
        for i in range(len(Backend.list_events)):  # ищем событие для изменения
            if target_id_event == Backend.list_events[i].info_Event()[0]:
                Backend.list_events[i] = our_event  # обновить изменяемое событие
                break
        Backend.save_file_events()  # выгрузить все события на диск
        Backend.add_event_into_calendar_guest(target_id_event, guests, our_event.info_Event()[1])  # добавляем событие в календарь гостей

    def del_guests_in_event(target_id_event, guests: list):
        "Метод удаления гостей из события"
        for elem in Backend.list_events:
            if target_id_event == elem.info_Event()[0]:
                our_event = elem  # В переменную поместить из памяти требуемое событие
                break
        name_event = our_event.info_Event()[1]
        our_event.remove_list_guests(guests)  # Удаляем гостей из события
        Backend.load_file_events()  # Загрузить в память все события
        for i in range(len(Backend.list_events)):  # ищем событие для изменения
            if target_id_event == Backend.list_events[i].info_Event()[0]:
                Backend.list_events[i] = our_event  # обновить изменяемое событие
                break
        Backend.save_file_events()  # выгрузить все события на диск
        Backend.del_event_from_calendars_guests(target_id_event, guests, name_event)  # добавляем событие в календарь гостей

    @staticmethod
    def del_event_from_calendars_guests(target_id_event, guest:list, name_event):
        "Метод удаления события из календарей гостей"
        """Алгоритм:
        1) Загружаем в память все календари
        2) Проходим по календарям
        3) Удаляем требуемое событие (по id) в календаре, если id_user есть в guest
        4) Сохраняем календари
        """
        Backend.clear_notification()  # очищаем список уведомлений
        Backend.load_file_calendars()  # загружаем в память все календари
        for i in range(len(Backend.list_calendars)):
            if (target_id_event in Backend.list_calendars[i].info_calendars()[3]) and ((Backend.list_calendars[i].info_calendars()[2]) in guest):
                Backend.list_calendars[i].info_calendars()[3].remove(target_id_event)  # удаляем требуемое событие (по id)
                Backend.add_notification(id_user=Backend.list_calendars[i].info_calendars()[2],id_event=target_id_event, action="D", del_details=name_event)  # добавляем уведомление
                Backend.save_file_notifications(add_notification=True)  # сохраняем уведомления
                Backend.clear_notification()  # очищаем список уведомлений
        Backend.save_file_calendars()  # сохраняем все календари

    @staticmethod
    def auth_user(login_user, password_user):
        "Метод проверки логина и пароля"
        """Возвращает True, если всё совпало, иначе False"""
        password_user = hs(password_user)
        Backend.load_file_users(login_user)  # загрузили конкретного пользователя по логину
        for elem in Backend.info_users():
            if login_user == elem.info_User()[3] and password_user == elem.info_User()[4]:
                id_user = elem.info_User()[0]
                return id_user
        else:
            return False

    @staticmethod
    def reg_user(login_user, name_user, lastname_user, password_user):
        "Регистрация нового user"
        Backend.load_file_users(target_login='*********')  # запускаем загрузку пользователей без загрузки
        # в память backend, чтобы обновить id_counter
        new_user = User(login=login_user, name=name_user, lastname=lastname_user, password=password_user)
        Backend.add_user(new_user)  # добавили в память пользователя
        Backend.save_file_users(add_user=True)  # дополнили файл с пользователями новым пользователем
        return new_user.info_id_User()




































