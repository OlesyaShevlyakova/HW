"""
Пользователь - имеет логин и пароль, а так же календарь.
у пользователя есть итендифекатор начинающийся с @
"""
import hashlib
from Utils import hash_password as hs
class User:
    _login = None
    _password = None
    _id = None
    _name = None
    _lastname = None
    __id_counter__ = 1

    def __init__(self, login, name, lastname, password=None, id=None, hash_pass=None):
        """
        :param password: поле заполняется при создании пользователя, при загрузке из файла - оно пустое
        :param id: заполняется при загрузке из файла, иначе генерируется
        :param hash_pass: поле заполняется при загрузке из файла
        """
        if hash_pass is None:
            self._password = hs(password)   # переводим пароль в hash
        else:
            self._password =hash_pass
        self._login = login
        self._name = name
        self._lastname = lastname
        if id is None:
            self._id = "@" + self._name + self._lastname + "*" + str(self.__class__.__id_counter__)   # присвоили id новому пользователю
            self.__class__.__id_counter__ += 1  # увеличили инкрементальный id
        else:
            self._id = id

    def info_User(self):
        "Возвращает информацию о User"
        return (self._id, self._name, self._lastname, self._login, self._password)

    def info_id_User(self):
        "Возвращает информацию об id User"
        return (self._id)

    def change_user(self, new_name=None, new_lastname=None, new_password=None):
        "Замена информации о User"
        if new_name is not None:
            self._name = new_name
        if new_lastname is not None:
            self._lastname = new_lastname
        if new_password is not None:
            self._password = hs(new_password)


    def __str__(self):
        "Возвращает информацию для пользователя"
        return f"Пользователь {self._login} с id {self._id}"

    def __repr__(self):
        "Возвращает информацию для разработчика"
        return f"[{self._login}:{self._id}]"

    @staticmethod
    def change_id_counter(new_counter):
        "Изменение id_counter"
        User.__id_counter__ = new_counter


