import flet as ft
from Backend import Backend
import re


class EditEvent(ft.UserControl):
    "Создание страницы редактирования информации о событии"

    def __init__(self, page, global_dict_state):
        super().__init__()
        self.expand = True  # если объект котнейнер возвращается как объект класса, то у него не работает свойство
        # expand, это свойство нужно указывать на уровне объекта этого класса
        self.page = page
        self.page.window_height = 630
        self.page.window_width = 930
        self.page.title = "Окно редактирования информации о событии"
        self.name_new_event = ft.Ref[ft.TextField]()  # новое наименование события
        self.des_new_event = ft.Ref[ft.TextField]()  # новое описание события
        self.button_save_new = ft.Ref[ft.ElevatedButton]()  # кнопка сохранить
        self.button_back = ft.Ref[ft.ElevatedButton]()  # кнопка назад
        self.calendars_user = ft.Column(
            scroll=ft.ScrollMode.ALWAYS,
        )  # список календарей пользователя
        self.rg_calendars = ft.RadioGroup(
            content=self.calendars_user,
            on_change=self.check_for_save_button
        )
        self.new_guests_event = ft.Column(
            scroll=ft.ScrollMode.ALWAYS,
        )  # список гостей
        self.global_dict_state = global_dict_state

    def build(self):
        Backend.load_file_calendars(self.global_dict_state['id_user'])  # загрузить все календари пользователя в backend
        for elem in Backend.info_calendars():
            info_calendars = elem.info_calendars()
            self.calendars_user.controls.append(
                ft.Radio(
                    value=info_calendars[0],
                    label=f"календарь {info_calendars[1]}",
                )
            )
        self.rg_calendars.value = self.global_dict_state['id_calendar']

        Backend.load_file_users()  # загрузить всех пользователей в backend
        for elem in Backend.info_users():
            info_user = elem.info_User()
            if info_user[0] != self.global_dict_state['id_user']:
                self.new_guests_event.controls.append(
                    ft.Checkbox(
                        label=f"имя {info_user[1]}, фамилия {info_user[2]}, id пользователя {info_user[0]}",
                        on_change=self.check_for_save_button,
                    )
                )
        our_event = Backend.get_event_by_id(self.global_dict_state['id_event_for_edit'])
        for x in self.new_guests_event.controls:
            if x.label.split(' ')[-1] in our_event[6]:
                x.value = True

        return ft.Container(
            image_src='/EditEvent.jpg',
            alignment=ft.alignment.center_left, expand=True,
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text("""Редактирование события""",
                                    size=40,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.colors.BLUE_900),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Column(
                                    controls=
                                    [

                                        ft.Text("""Используйте только ЛАТИНСКИЕ буквы и цифры""",
                                                size=14,
                                                color=ft.colors.RED),
                                        ft.Text("Введите новое название события", size=16, italic=True),
                                        ft.TextField(ref=self.name_new_event, width=350, label=our_event[1],
                                                     on_change=self.check_for_save_button),
                                        ft.Text("Введите новое описание события", size=16, italic=True),
                                        ft.TextField(ref=self.des_new_event, width=350, label=our_event[2],
                                                     on_change=self.check_for_save_button),
                                        ft.Text(
                                            "Если хотите переместить данное событие \n в другой календарь, выберите его",
                                            size=16,
                                            italic=True),
                                        ft.Container(
                                            content=self.rg_calendars,
                                            border=ft.border.all(2, ft.colors.BLUE),
                                            border_radius=10,
                                            padding=10,
                                            height=200,
                                        ),
                                    ]
                                ),
                                ft.Column(
                                    [
                                        ft.Container(width=20, height=20, alignment=ft.alignment.center),
                                        ft.Text("Если хотите, измените гостей \n (поставьте/удалите галочку)",
                                                size=16,
                                                italic=True),
                                        ft.Container(
                                            content=self.new_guests_event,
                                            border=ft.border.all(2, ft.colors.BLUE),
                                            border_radius=10,
                                            padding=10,
                                            height=300,
                                        ),
                                        ft.Container(width=10, height=10, alignment=ft.alignment.center),
                                        # пустой контейнер
                                        ft.ElevatedButton(
                                            ref=self.button_save_new,
                                            disabled=True,
                                            adaptive=True,
                                            bgcolor=ft.cupertino_colors.SYSTEM_TEAL,
                                            content=ft.Row(
                                                [
                                                    ft.Icon(name=ft.icons.FAVORITE, color="pink"),
                                                    ft.Text("Сохранить", size=18, weight=ft.FontWeight.BOLD),
                                                ],
                                                tight=True
                                            ),
                                            on_click=self.button_save_new_click),
                                        ft.ElevatedButton(
                                            ref=self.button_back,
                                            width=150,
                                            content=ft.Row(
                                                [
                                                    ft.Icon(name=ft.icons.BACKUP, color="blue"),
                                                    ft.Text(value="Назад", size=20, color=ft.colors.LIGHT_BLUE_800),
                                                ],
                                                alignment=ft.MainAxisAlignment.SPACE_AROUND),
                                            on_click=lambda _: self.page.go('/login')  # TODO
                                        )  # Возвращает на окно логина
                                    ],
                                ),
                            ]
                        )
                    )
                ]

            )
        )

    def button_save_new_click(self, e: ft.ControlEvent):
        "Обработка нажатия на кнопку - Сохранить"

        if ((check_latin(self.name_new_event.current.value) is None) or
                (check_latin(self.des_new_event.current.value) is None)):
            dlg = ft.AlertDialog(title=ft.Text(f"Используйте только ЛАТИНСКИЕ буквы и цифры"))
            self.page.dialog = dlg  # мы у страницы указываем, что у нее имеется диалог
            dlg.open = True
        else:
            if len(self.name_new_event.current.value) > 0:
                Backend.update_name_event(self.global_dict_state['id_event_for_edit'],
                                          self.name_new_event.current.value)  # изменяем название события
            if len(self.des_new_event.current.value) > 0:
                Backend.update_description_event(self.global_dict_state['id_event_for_edit'],
                                                 self.des_new_event.current.value)  # изменяем описание события
            if self.global_dict_state['id_calendar'] != self.rg_calendars.value:
                Backend.move_event_from_calendars(self.global_dict_state['id_calendar'],
                                                  self.global_dict_state['id_event_for_edit'],
                                                  self.rg_calendars.value)
            if self.check_guests() is True:
                new_guest = []  # новый список гостей
                our_event = Backend.get_event_by_id(self.global_dict_state['id_event_for_edit'])[
                    6]  # исходный список гостей
                for x in self.new_guests_event.controls:
                    if x.value is True:
                        new_guest.append(x.label.split(' ')[-1])  # новый список гостей
                add_new_guest = []  # этим гостям нужно событие добавить
                for elem in new_guest:
                    if elem not in our_event:  # значит это новый человек
                        add_new_guest.append(elem)
                Backend.add_guests_in_event(self.global_dict_state['id_event_for_edit'], add_new_guest)
                del_guest = []  # у этих гостей событие удалить
                for elem in our_event:  # идем по старому списку гостей
                    if elem not in new_guest:  # если человек из старого списка не значится в новом,  значит его удалили
                        del_guest.append(elem)
                Backend.del_guests_in_event(self.global_dict_state['id_event_for_edit'], del_guest)

            dlg = ft.AlertDialog(title=ft.Text(f"Изменения выполнены успешно, щелкните по экрану"))
            self.page.dialog = dlg  # мы у страницы указываем, что у нее имеется диалог
            dlg.open = True
        self.update()
        self.page.update()

    def check_for_save_button(self, e: ft.ControlEvent):
        "Активация кнопки - Сохранить"
        if ((len(self.name_new_event.current.value) > 0) or (len(self.des_new_event.current.value) > 0) or
                (self.global_dict_state['id_calendar'] != self.rg_calendars.value) or self.check_guests()):
            self.button_save_new.current.disabled = False
        else:
            self.button_save_new.current.disabled = True
        self.update()

    def check_guests(self):
        "Проверка, изменился ли список гостей"
        our_event = Backend.get_event_by_id(self.global_dict_state['id_event_for_edit'])  # список гостей
        new_guest = []
        for x in self.new_guests_event.controls:
            if x.value is True:
                new_guest.append(x.label.split(' ')[-1])
        if new_guest != our_event[6]:  # изменился список гостей
            return True
        else:
            return False  # не изменился список гостей


def check_latin(text: str):
    "Проверка на вхождение только правильных символов"
    pattern = re.compile("^[a-zA-Z0-9 ]*$")
    return pattern.match(text)
