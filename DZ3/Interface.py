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
from User import User

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
        if not flag:
            print("Данный логин не обнаружен, введите другой логин или заведите новый")
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
            Interface.consecution.append(Interface.creating_user)
        else:
            print("Введите имя")
            name_user = input()
            print("Введите фамилию")
            lastname_user = input()
            print("Введите пароль")
            password_user = input()
            new_user = User(login=login_user, name=name_user, lastname=lastname_user, password=password_user)
            Interface.backend.clear_users()
            Interface.backend.add_user(new_user)
            Interface.backend.save_file_users(add_user=True)
            Interface.consecution.append(Interface.main_screen)

    @staticmethod
    def main_screen():
        "Главное меню интерфейса"
        question = input("""
                    Выберите действие:
                    1) создать событие (выбрав календарь),
                    2) изменить событие (выбрав календарь),
                    3) удалить событие (выбрав календарь),
                    4) отобразить все события,
                    5) отобразить события из временного диапазона,
                    6) отобразить события, где я "гость"
                    7) выйти из системы,
                    8) изменить информацию о пользователе
                    """)
        if question == "1":
            Interface.consecution.append(Interface.add_event)
        elif question == "2":
            Interface.consecution.append(Interface.edit_event)
        elif question == "3":
            Interface.consecution.append(Interface.del_event)
        elif question == "4":
            Interface.consecution.append(Interface.show_events)
        elif question == "5":
            Interface.consecution.append(Interface.show_events_range)
        elif question == "6":
            Interface.consecution.append(Interface.show_events_guest)
        elif question == "7":
            Interface.consecution.append(Interface.identification_user)
        elif question == "8":
            Interface.consecution.append(Interface.change_user)
        else:
            print("Некорректный ввод данных 😎")
            Interface.consecution.append(Interface.main_screen)

    @staticmethod
    def change_user():
        "Изменить  информацию о пользователе"
        question = input("""
                            Выберите действие:
                            1) изменить имя,
                            2) изменить фамилию,
                            3) изменить пароль,
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







Interface.work()

