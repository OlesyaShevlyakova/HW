"""
Класс Notification хранит в себе уведомления

                    логиниться пользователь - проверяем есть ли нотификейшены для него. если есть, отображаем сообщение - прочитай нотификейшены
                    1) загрузили нотификейшены по id пользователя в память
                    2) проверили есть ли такие нотификейшены, то  оторбазили сообщение.

                    у пользователя в интерфейсе есть пункт обработать нотификации
                    1) отобразить из памяти нотификации что его добавили в события, и его удалили из событий.
                    2) если добавили, то отображаем подробну инфорацию по данному ивенту
                    3) если удалили то показываем только айдишник события и название события из которого его удалили.

                    при выборе обработать нотификации надо сохранить ид нотификаций в перменной.
                    загрузить все нотификации в память.
                    удалить оттуда прочитанные нотификации
                    сохранить оставшеес на диск.
                    """

class Notification:
    _id = None  # id уведомления
    _id_user = None  # id пользователя
    _id_event = None  # id события
    _action = None  # "C" - create, "D" - delete
    _del_details = None  # название удаленного события
    __id_counter__ = 1  # счетчик для гарантии уникальности id

    def __init__(self, id=None, id_user=None, id_event=None, action=None, del_details=None):
        """
        :param id: генерируется или заполняется при загрузке из файла
        :param id_user: заполняется при загрузке из файла или при создании уведомления
        :param id_event: заполняется при загрузке из файла или при создании уведомления
        :param action: заполняется при загрузке из файла или при создании уведомления
        :param del_details: заполняется при загрузке из файла или при создании уведомления
        """
        self._id_user = id_user
        self._id_event = id_event
        self._action = action
        self._del_details = del_details
        if id is None:
            self._id = self.__class__.__id_counter__  # присвоили id новому уведомлению
            self.__class__.__id_counter__ += 1  # увеличили инкрементальный id
            self._id = str(self._id)
        else:
            self._id = str(id)

    def info_Notif(self):
        "Возвращает информацию об уведомлениях"
        return self._id, self._id_user, self._id_event, self._action, self._del_details

    @staticmethod
    def change_id_counter(new_counter):
        "Изменение id_counter"
        Notification.__id_counter__ = new_counter

    def __str__(self):
        "Возвращает информацию для пользователя"
        result1 = f"Наменование события {self._del_details}, id события {self._id_event}, выполненное действие с событием "
        result2 = '{action}'.format(action='Создано' if self._action=='C' else 'Удалено')
        result = result1 + result2
        return result

