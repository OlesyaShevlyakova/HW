"""
Позволяет зайти по логину-паролю или создать нового пользователя (а так же выйти из аккаунта)
Позволяет выбрать календарь, узнать ближайшие события, события из промежутка времени а так же
Создать событие или удалить событие
После создания события можно добавить туда пользователей
Если нас добавили в событие или удалили мы получаем уведомление.

в main можно использовать ТОЛЬКО interface
"""

# TODO: написать интерфейс смены пароля

from Backend import Backend
from Utils import hash_password as hs
from User import User

class Interface:
    backend = None
    consecution = list()
    id_user = None

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
        pass







Interface.work()

