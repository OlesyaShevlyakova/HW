"""
Позволяет зайти по логину-паролю или создать нового пользователя (а так же выйти из аккаунта)
Позволяет выбрать календарь, узнать ближайшие события, события из промежутка времени а так же
Создать событие или удалить событие
После создания события можно добавить туда пользователей
Если нас добавили в событие или удалили мы получаем уведомление.

в main можно использовать ТОЛЬКО interface
"""


from Backend import Backend
from Utils import hash_password as hs
from Utils import check_date
from User import User
from Calendar import Calendar
from Event import Event
from time import sleep

class Interface:
    backend = None
    consecution = list()
    id_user = None
    login_user = None

    @staticmethod
    def work():
        "Модуль обработки очереди задач"
        Interface.consecution = [Interface.start]

        while Interface.consecution:
            Interface.consecution[0]()
            del Interface.consecution[0]
        print("Work интерфейса закончил работу")

    @staticmethod
    def start():
        "Первичная инициализация программы"
        Interface.backend = Backend
        Interface.consecution.append(Interface.identification_user)

    @staticmethod
    def identification_user():
        "Идентификация пользователя"
        print("Введите логин")
        login_user = input()
        print("Введите пароль")
        password_user = hs(input())
        Interface.backend.load_file_users(login_user)
        flag = False
        for elem in Interface.backend.info_users():
            if login_user == elem.info_User()[3] and password_user == elem.info_User()[4]:
                flag = True
                Interface.id_user = elem.info_User()[0]
                Interface.login_user = elem.info_User()[3]
                Interface.consecution.append(Interface.main_screen)
                print("Успешная авторизация!")
                sleep(1)
        if not flag:
            print("Неправильный логин\пароль, либо логин не существует, введите другой логин или заведите новый")
            sleep(1)
            question = input("""
            Выберите действие:
            1) ввести другой логин или пароль
            2) создать новый логин
            """)
            if question == "1":
                Interface.consecution.append(Interface.identification_user)
            elif question == "2":
                Interface.consecution.append(Interface.creating_user)
            else:
                print("Некорректный ввод данных 😎")
                Interface.consecution.append(Interface.identification_user)

    @staticmethod
    def creating_user():
        "Создание пользователя"
        print("Введите логин")
        login_user = input()
        if not Interface.backend.originality_login(login_user):
            print("Введите другой логин, данный логин уже существует")
            sleep(1)
            Interface.consecution.append(Interface.creating_user)
        else:
            print("Введите имя")
            name_user = input()
            print("Введите фамилию")
            lastname_user = input()
            print("Введите пароль")
            password_user = input()
            Interface.backend.load_file_users(target_login='*********')  # запускаем загрузку пользователей без загрузки
                                                                        # в память backend, чтобы обновить id_counter
            new_user = User(login=login_user, name=name_user, lastname=lastname_user, password=password_user)
            Interface.login_user = login_user
            Interface.id_user = new_user.info_id_User()
            Interface.backend.add_user(new_user)
            Interface.backend.save_file_users(add_user=True)
            Interface.consecution.append(Interface.add_calendar)
            print("Учетная запись создана!")
            print("Пожалуйста, создайте календарь")
            sleep(2)

    @staticmethod
    def main_screen():
        "Главное меню интерфейса"
        question = input("""
                    Выберите действие:
                    ========== КАЛЕНДАРИ ==========
                    0) отобразить список календарей
                    1) создать календарь
                    2) изменить календарь
                    3) удалить календарь
                    ========== СОБЫТИЯ ==========
                    4) создать событие (выбрав календарь)
                    5) удалить событие (выбрав календарь)
                    6) отобразить все события
                    7) отобразить события из временного диапазона
                    8) отобразить события, где я "гость"
                    ========== СЕРВИСНОЕ ==========
                    9) выйти из системы
                    10) изменить информацию о пользователе
                    """)
        if question == "0":
            Interface.consecution.append(Interface.show_list_calendar)
        elif question == "1":
            Interface.consecution.append(Interface.add_calendar)
        elif question == "2":
            Interface.consecution.append(Interface.edit_calendar)
        elif question == "3":
            Interface.consecution.append(Interface.del_calendar) #TODO
        elif question == "4":
            Interface.consecution.append(Interface.add_event)
        elif question == "5":
            Interface.consecution.append(Interface.del_event)
        elif question == "6":
            Interface.consecution.append(Interface.show_events)
        elif question == "7":
            Interface.consecution.append(Interface.show_events_range)
        elif question == "8":
            Interface.consecution.append(Interface.show_events_guest)
        elif question == "9":
            Interface.consecution.append(Interface.identification_user)
        elif question == "10":
            Interface.consecution.append(Interface.change_user)
        else:
            print("Некорректный ввод данных 😎")
            Interface.consecution.append(Interface.main_screen)

    @staticmethod
    def change_user():
        "Изменить  информацию о пользователе"
        question = input("""
                            Выберите действие:
                            1) изменить имя
                            2) изменить фамилию
                            3) изменить пароль
                            4) вернуться к главному меню
                            """)
        if question == "1":
            Interface.consecution.append(Interface.change_name)
        elif question == "2":
            Interface.consecution.append(Interface.change_lastname)
        elif question == "3":
            Interface.consecution.append(Interface.change_password)
        elif question == "4":
            Interface.consecution.append(Interface.main_screen)
        else:
            print("Некорректный ввод данных 😎")
            Interface.consecution.append(Interface.change_user)

    @staticmethod
    def change_name():
        "Изменить имя пользователя"
        new_name = input("Введите новое имя")
        Interface.backend.update_user(Interface.login_user, new_name=new_name)
        print("Имя успешно изменено")
        Interface.consecution.append(Interface.change_user)

    @staticmethod
    def change_lastname():
        "Изменить фамилию пользователя"
        new_lastname = input("Введите новую фамилию")
        Interface.backend.update_user(Interface.login_user, new_lastname=new_lastname)
        print("Фамилия успешно изменена")
        Interface.consecution.append(Interface.change_user)

    @staticmethod
    def change_password():
        "Изменить пароль пользователя"
        new_password = input("Введите новый пароль")
        Interface.backend.update_user(Interface.login_user, new_password=new_password)
        print("Пароль успешно изменен")
        Interface.consecution.append(Interface.change_user)

    @staticmethod
    def show_list_calendar():
        "Отобразить список календарей"
        Interface.show_list_calendar_worker()
        Interface.consecution.append(Interface.main_screen)
        input('Нажмите Enter')

    @staticmethod
    def show_list_calendar_worker():
        """Отобразить список календарей:
                        1) загрузить в память календари конкретного пользователя,
                        2) отобразить календари пользователя
                        """
        Interface.backend.load_file_calendars(Interface.id_user)
        calendar_exist = False
        for elem in Interface.backend.info_calendars():
            if not calendar_exist:
                print('======Список календарей=====')
                calendar_exist = True
            info_calendar = elem.info_calendars()
            print(f"Календарь {info_calendar[1]}, id календаря {info_calendar[0]}, количество событий {len(info_calendar[3])}")
        if not calendar_exist:
            print('Календари не существуют! Создайте новый календарь!')
        else:
            print('============================')

    @staticmethod
    def add_calendar():
        "Cоздать календарь"
        print("Введите имя календаря")
        name_calendar = input()
        new_calendar = Calendar(id_user=Interface.id_user, name_calendar=name_calendar)
        Interface.backend.load_file_calendars(target_id_user='*********')  # запускаем загрузку календарей без загрузки
                                                                        # в память backend, чтобы обновить id_counter
        Interface.backend.add_calendar(new_calendar)
        Interface.backend.save_file_calendars(add_calendar=True)
        Interface.consecution.append(Interface.main_screen)
        print('Календарь успешно создан')
        input('Нажмите Enter')

    @staticmethod
    def edit_calendar():
        "Изменить  информацию о календаре"
        question = input("""
                                Выберите действие:
                                1) изменить имя календаря
                                2) вернуться к главному меню
                                """)
        if question == "1":
            Interface.consecution.append(Interface.change_name_calendar)
        elif question == "2":
            Interface.consecution.append(Interface.main_screen)
        else:
            print("Некорректный ввод данных 😎")
            sleep(1)
            Interface.consecution.append(Interface.edit_calendar)

    @staticmethod
    def change_name_calendar():
        "Изменить  информацию об имени календаря"
        """
        1) Отобразить все календари и спросить, какой календарь (по id) хочет изменить
        2) Проверить, что выбрал существующий id календаря
        3) Ввод нового имени календаря
        4) В переменную поместить из памяти требуемый календарь и обновить у него имя
        5) Загрузить в память все календари
        6) Подменить требуемый календарь
        7) Сохранить календари
        """
        Interface.show_list_calendar_worker()  # Отобразить список календарей пользователя
        target_id_calendar = input("Введите id календаря, имя которого хотите изменить")
        if not Interface.backend.check_id_calendar(target_id_calendar):
            print("Некорректный ввод данных 😎")
            Interface.consecution.append(Interface.change_name_calendar)
        else:
            new_name_calendar = input("Введите новое имя календаря")
            Interface.backend.update_calendar(target_id_calendar, new_name_calendar)
            print("Имя календаря успешно изменено")
            sleep(1)
            Interface.consecution.append(Interface.main_screen)

    @staticmethod
    def add_event():
        "Cоздать событие"
        print("Введите имя события")
        name_event = input()
        print("Введите описание события")
        description = input()
        while True:
            print("Введите дату события в формате YYYY-MM-DD, например 2023-01-05")
            date_event = input()
            if check_date(date_event):
                break
            else:
                print("Дата введена неправильно")
        while True:
            print("""Введите периодичность события в формате D или W или M или Y или N, где:
                                                        D - ежедневно
                                                        W - еженедельно
                                                        M - ежемесячно
                                                        Y - ежегодно
                                                        N - разово""")
            repeat_type = input().upper()
            if (len(repeat_type) == 1) and (repeat_type in ["D", "W", "M", "Y", "N"]):
                if repeat_type == "N":
                    repeat_type = None
                break
            else:
                print("Периодичность введена неправильно")
        question = input("""
                                        Будем добавлять гостей:
                                        да - 1
                                        нет - любой символ
                                        """)
        if question == "1":
            Interface.backend.load_file_users()  # загрузить всех пользователей в backend
            for elem in Interface.backend.info_users():
                info_user = elem.info_User()
                print(f"имя {info_user[1]}, id пользователя {info_user[0]}")
            while True:
                guests = input("Укажите id пользователей через пробел")
                guests = guests.split()
                result = Interface.backend.check_id_users(guests)
                if result:
                    break
                else:
                    print("Пользователи введены неверно, укажите id пользователей через пробел")
        else:
            guests = []
        new_event = Event(name_event=name_event, description=description, event_owner=Interface.id_user, guests=guests, data_event=date_event,
                 repeat_type=repeat_type)
        Interface.backend.load_file_events(target_id_event='*********')  # запускаем загрузку событий без загрузки
                                                                         # в память backend, чтобы обновить id_counter
        # TODO: У нас не добавляются события в сам календарь, Надо исправить.
        # 1) Загрузить в память календари пользователя
        # 2) Если
        # TODO: Доработать, так как надо добавлять соыбтия в календари гостей
        Interface.backend.add_event(new_event)
        Interface.backend.save_file_events(add_user=True)
        print("Успешно добавили событие")
        Interface.consecution.append(Interface.main_screen)





Interface.work()

