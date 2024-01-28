"""
Позволяет зайти по логину-паролю или создать нового пользователя (а так же выйти из аккаунта)
Позволяет выбрать календарь, узнать ближайшие события, события из промежутка времени а так же
Создать событие или удалить событие
После создания события можно добавить туда пользователей
Если нас добавили в событие или удалили мы получаем уведомление.

в main можно использовать ТОЛЬКО interface
"""
#TODO: работу notification реализовать
#TODO: изменение события в календаре

from Backend import Backend
from Utils import hash_password as hs
from Utils import check_date
from User import User
from Calendar import Calendar
from Event import Event
from time import sleep

class Interface:
    backend = None
    tasks_list = list()  # лист очереди задач
    id_user = None  # сохранение id авторизованного пользователя
    login_user = None  # сохранение login авторизованного пользователя

    @staticmethod
    def work():
        "Модуль обработки очереди задач"
        Interface.tasks_list = [Interface.start]

        while Interface.tasks_list:
            Interface.tasks_list[0]()
            del Interface.tasks_list[0]
        print("Work интерфейса закончил работу")

    @staticmethod
    def start():
        "Первичная инициализация программы"
        Interface.backend = Backend
        Interface.tasks_list.append(Interface.identification_user)

    @staticmethod
    def identification_user():
        "Идентификация пользователя"
        print("Введите логин")
        login_user = input()
        print("Введите пароль")
        password_user = hs(input())
        Interface.backend.load_file_users(login_user)  # загрузили конкретного пользователя по логину
        flag = False
        for elem in Interface.backend.info_users():
            if login_user == elem.info_User()[3] and password_user == elem.info_User()[4]:
                flag = True
                Interface.id_user = elem.info_User()[0]
                Interface.login_user = elem.info_User()[3]
                Interface.tasks_list.append(Interface.main_screen)
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
                Interface.tasks_list.append(Interface.identification_user)
            elif question == "2":
                Interface.tasks_list.append(Interface.creating_user)
            else:
                print("Некорректный ввод данных 😎")
                Interface.tasks_list.append(Interface.identification_user)

    @staticmethod
    def creating_user():
        "Создание пользователя"
        print("Введите логин (только ЛАТИНСКИЕ буквы)")
        login_user = input()
        if not Interface.backend.originality_login(login_user):  # проверка на уникальность логина
            print("Введите другой логин, данный логин уже существует")
            sleep(1)
            Interface.tasks_list.append(Interface.creating_user)
        else:
            print("Введите имя (только ЛАТИНСКИЕ буквы)")
            name_user = input()
            print("Введите фамилию (только ЛАТИНСКИЕ буквы)")
            lastname_user = input()
            print("Введите пароль (только ЛАТИНСКИЕ буквы и цифры)")
            password_user = input()
            Interface.backend.load_file_users(target_login='*********')  # запускаем загрузку пользователей без загрузки
                                                                        # в память backend, чтобы обновить id_counter
            new_user = User(login=login_user, name=name_user, lastname=lastname_user, password=password_user)
            Interface.login_user = login_user
            Interface.id_user = new_user.info_id_User()
            Interface.backend.add_user(new_user)  # добавили в память пользователя
            Interface.backend.save_file_users(add_user=True)  # дополнили файл с пользователями новым пользователем
            print("Учетная запись создана!")
            print("Пожалуйста, создайте календарь")
            sleep(2)
            Interface.tasks_list.append(Interface.add_calendar)

    @staticmethod
    def main_screen():
        "Главное меню интерфейса"
        print()
        print('-------------------------------------------------------------------')
        print(f'Текущий логин пользователя - {Interface.login_user} и id - {Interface.id_user}')
        print('-------------------------------------------------------------------')
        question = input("""
                    Выберите действие:
                    ========== КАЛЕНДАРИ ==========
                    0) отобразить список календарей
                    1) создать календарь
                    2) изменить имя календаря
                    ========== СОБЫТИЯ ==========
                    3) создать событие (выбрав календарь)
                    4) удалить событие (выбрав календарь)
                    5) отобразить все события из выбранного календаря
                    6) отобразить события из временного диапазона (выбрав календарь)
                    7) привязать событие к другому календарю
                    ========== СЕРВИСНОЕ ==========
                    8) посмотреть оповещения
                    9) выйти из системы
                    10) изменить информацию о пользователе
                    """)
        if question == "0":
            Interface.tasks_list.append(Interface.show_list_calendar)
        elif question == "1":
            Interface.tasks_list.append(Interface.add_calendar)
        elif question == "2":
            Interface.tasks_list.append(Interface.edit_calendar)
        elif question == "3":
            Interface.tasks_list.append(Interface.add_event)
        elif question == "4":
            Interface.tasks_list.append(Interface.del_event)
        elif question == "5":
            Interface.tasks_list.append(Interface.show_events)
        elif question == "6":
            Interface.tasks_list.append(Interface.show_events_range)
        elif question == "7":
            Interface.tasks_list.append(Interface.link_to_another_calendar)
        elif question == "8":
            Interface.tasks_list.append(Interface.show_notification)
        elif question == "9":
            Interface.tasks_list.append(Interface.identification_user)
        elif question == "10":
            Interface.tasks_list.append(Interface.change_user)
        else:
            print("Некорректный ввод данных 😎")
            Interface.tasks_list.append(Interface.main_screen)

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
            Interface.tasks_list.append(Interface.change_name)
        elif question == "2":
            Interface.tasks_list.append(Interface.change_lastname)
        elif question == "3":
            Interface.tasks_list.append(Interface.change_password)
        elif question == "4":
            Interface.tasks_list.append(Interface.main_screen)
        else:
            print("Некорректный ввод данных 😎")
            Interface.tasks_list.append(Interface.change_user)

    @staticmethod
    def change_name():
        "Изменить имя пользователя"
        new_name = input("Введите новое имя (только ЛАТИНСКИЕ буквы)")
        Interface.backend.update_user(Interface.login_user, new_name=new_name)
        print("Имя успешно изменено")
        Interface.tasks_list.append(Interface.change_user)

    @staticmethod
    def change_lastname():
        "Изменить фамилию пользователя"
        new_lastname = input("Введите новую фамилию (только ЛАТИНСКИЕ буквы)")
        Interface.backend.update_user(Interface.login_user, new_lastname=new_lastname)
        print("Фамилия успешно изменена")
        Interface.tasks_list.append(Interface.change_user)

    @staticmethod
    def change_password():
        "Изменить пароль пользователя"
        new_password = input("Введите новый пароль (только ЛАТИНСКИЕ буквы и цифры)")
        Interface.backend.update_user(Interface.login_user, new_password=new_password)
        print("Пароль успешно изменен")
        Interface.tasks_list.append(Interface.change_user)

    @staticmethod
    def show_list_calendar():
        "Отобразить список календарей"
        Interface.show_list_calendar_worker()
        Interface.tasks_list.append(Interface.main_screen)
        input('Нажмите Enter')

    @staticmethod
    def show_list_calendar_worker():
        """Отобразить список календарей:
                        1) загрузить в память календари конкретного пользователя,
                        2) отобразить календари пользователя
                        """
        Interface.backend.load_file_calendars(Interface.id_user)  # загружаем календари конкретного пользователя
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
        Interface.backend.add_calendar(new_calendar)  # добавляем календарь в память
        Interface.backend.save_file_calendars(add_calendar=True)  # дописываем файл с календарями
        Interface.tasks_list.append(Interface.main_screen)
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
            Interface.tasks_list.append(Interface.change_name_calendar)
        elif question == "2":
            Interface.tasks_list.append(Interface.main_screen)
        else:
            print("Некорректный ввод данных 😎")
            sleep(1)
            Interface.tasks_list.append(Interface.edit_calendar)

    @staticmethod
    def change_name_calendar():
        "Изменить  информацию об имени календаря"
        """
        Алгоритм работы
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
        if not Interface.backend.check_id_calendar(target_id_calendar):  # проверка, что выбрали существующий календарь
            print("Некорректный ввод данных 😎")
            Interface.tasks_list.append(Interface.change_name_calendar)
        else:
            new_name_calendar = input("Введите новое имя календаря (только ЛАТИНСКИЕ буквы)")
            Interface.backend.update_calendar(target_id_calendar, new_name_calendar)
            print("Имя календаря успешно изменено")
            sleep(1)
            Interface.tasks_list.append(Interface.main_screen)

    @staticmethod
    def add_event():
        "Cоздать событие"
        print("Введите имя события (только ЛАТИНСКИЕ буквы)")
        name_event = input()
        print("Введите описание события (только ЛАТИНСКИЕ буквы)")
        description = input()
        while True:
            print("Введите дату события в формате YYYY-MM-DD, например, 2023-01-05")
            date_event = input()
            if check_date(date_event):  # проверка, что ввели корректно дату
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
                guests = input("Укажите id пользователей через пробел\n")
                guests = guests.split()
                result = Interface.backend.check_id_users(guests)
                if result:
                    break
                else:
                    print("Пользователи введены неверно, укажите id пользователей через пробел\n")
        else:
            guests = []
        Interface.backend.load_file_events(target_id_events=['*********'])  # запускаем загрузку событий без загрузки
                                                                         # в память backend, чтобы обновить id_counter
        new_event = Event(name_event=name_event, description=description, event_owner=Interface.id_user, guests=guests,
                          data_event=date_event, repeat_type=repeat_type)
        Interface.backend.clear_events()  # очищаем память backend от событий
        Interface.backend.add_event(new_event)  # добавляем событие в память backend
        Interface.backend.save_file_events(add_event=True)  # добавляем событие в файл

        """Алгоритм добавления события в календарь:
        1) Загрузить в память календари пользователя
        2) Спросить у пользователя, в какой календарь надо добавить событие
        3) Проверяем id выбранного календаря
        4) Добавляем событие в выбранный календарь"""

        print('*********Выводим ваши календари*********')
        Interface.backend.load_file_calendars(Interface.id_user)  # загружаем в память календари пользователя
        for elem in Interface.backend.info_calendars():
            print(elem)
        while True:
            target_id_calendar = input("Введите id своего календаря, в который хотите добавить своё событие\n")
            if not Interface.backend.check_id_calendar(target_id_calendar):  # проверка, что выбрали существующий календарь
                print("Некорректный ввод данных 😎")
            else:
                break
        Interface.backend.add_event_into_calendar(target_id_calendar, new_event.info_id_event())  # добавление
                                                                                                # события в календарь
        Interface.backend.add_event_into_calendar_guest(new_event.info_id_event(), guests)  # добавление события в
                                                                                            # календарь гостей
        print("Событие в календарь успешно добавлено")
        sleep(1)
        Interface.tasks_list.append(Interface.main_screen)

    @staticmethod
    def show_events():
        "Отобразить все события"
        print('*********Выводим ваши календари*********')
        Interface.backend.load_file_calendars(Interface.id_user)  # загружаем в память календари пользователя
        for elem in Interface.backend.info_calendars():
            print(elem)
        while True:
            target_id_calendar = input("Введите id своего календаря, события которого хотите увидеть\n")
            if not Interface.backend.check_id_calendar(
                    target_id_calendar):  # проверка, что выбрали существующий календарь
                print("Некорректный ввод данных 😎")
            else:
                break
        print('*********Выводим события выбранного календаря*********')
        print("id, название, описание, дата, периодичность, создатель, участники")
        for elem in Interface.backend.show_events(target_id_calendar):
            print(elem.info_Event())
        sleep(2)
        Interface.tasks_list.append(Interface.main_screen)

    @staticmethod
    def show_events_range():
        "Отобразить события из временного диапазона"
        print('*********Выводим Ваши календари*********')
        Interface.backend.load_file_calendars(Interface.id_user)  # загружаем в память календари пользователя
        for elem in Interface.backend.info_calendars():
            print(elem)
        while True:
            target_id_calendar = input("Введите id своего календаря, события которого хотите увидеть\n")
            if not Interface.backend.check_id_calendar(target_id_calendar):  # проверка, что выбрали
                                                                            # существующий календарь
                print("Некорректный ввод данных 😎")
            else:
                break
        while True:
            print("Введите дату начала диапазона в формате YYYY-MM-DD, например, 2023-01-05")
            data_from = input()
            if check_date(data_from):  # проверка, что ввели корректно дату
                break
            else:
                print("Дата введена неправильно, необходимо ввести в формате YYYY-MM-DD, например, 2023-01-05")
        while True:
            print("Введите дату конца диапазона в формате YYYY-MM-DD, например, 2023-01-05")
            data_to = input()
            if check_date(data_to):  # проверка, что ввели корректно дату
                break
            else:
                print("Дата введена неправильно, необходимо ввести в формате YYYY-MM-DD, например, 2023-01-05")
        print('*********Выводим ваши события из временного диапазона и выбранного календаря*********')
        for elem in Interface.backend.search_events(data_from, data_to, target_id_calendar):
            print(elem)
        sleep(1)
        Interface.tasks_list.append(Interface.main_screen)

    @staticmethod
    def del_event():
        "Удалить событие"
        """Алгоритм:
        1) Выбираем календарь, из которого хотим удалить событие
        2) Отображаем все события выбранного календаря, выбираем id события
        3) Удаляем событие из календарей
        """

        print('*********Выводим Ваши календари*********')
        Interface.backend.load_file_calendars(Interface.id_user)  # загружаем в память календари пользователя
        for elem in Interface.backend.info_calendars():
            print(elem)
        while True:
            target_id_calendar = input("Введите id своего календаря, событие из которого хотите удалить\n")
            if not Interface.backend.check_id_calendar(target_id_calendar):  # проверка, что выбрали
                                                                                # существующий календарь
                print("Некорректный ввод данных 😎")
            else:
                break
        print('*********Выводим события выбранного календаря*********')
        print("id, название, описание, дата, периодичность, создатель, участники")
        for elem in Interface.backend.show_events(target_id_calendar):
            print(elem.info_Event())
        while True:
            target_id_event = input("Введите id cобытия, которое хотите удалить\n")
            if not Interface.backend.check_id_event(target_id_event):  # проверка, что выбрали
                                                                        # существующее событие в календаре
                print("Некорректный ввод данных 😎")
            else:
                break
        Interface.backend.del_event_from_calendars(target_id_event)  # удаляем событие из календарей
        print("Событие из календарей успешно удалено")
        sleep(2)
        Interface.tasks_list.append(Interface.main_screen)

















if __name__ == "__main__":
    Interface.work()

