import flet as ft
from Backend import Backend
import re
from Utils import check_date


class CreateEvForm(ft.UserControl):
    "Создание страницы события"

    def __init__(self, page, global_dict_state):
        super().__init__()
        self.expand = True  # если объект котнейнер возвращается как объект класса, то у него не работает свойство
        # expand, это свойство нужно указывать на уровне объекта этого класса
        self.page = page
        self.page.window_height = 800
        self.page.window_width = 1350
        self.page.title = "Окно создания события"
        self.name_event = ft.Ref[ft.TextField]()
        self.des_event = ft.Ref[ft.TextField]()
        self.data_event = ft.Ref[ft.TextField]()
        self.repeat_event = ft.Ref[ft.TextField]()
        self.info_failed = ft.Ref[ft.Text]()
        self.button_save_new = ft.Ref[ft.ElevatedButton]()
        self.button_back = ft.Ref[ft.ElevatedButton]()
        self.global_dict_state = global_dict_state
        self.guests_event = ft.Column(
            scroll=ft.ScrollMode.ALWAYS,
        )

    def build(self):
        Backend.load_file_users()  # загрузить всех пользователей в backend
        for elem in Backend.info_users():
            info_user = elem.info_User()
            # self.global_dict_state = {'id_user': '@OlesyaShevlyakova*1', 'id_calendar': '10'}    # для тестирования
            if info_user[0] != self.global_dict_state['id_user']:
                self.guests_event.controls.append(
                    ft.Checkbox(
                        label=f"имя {info_user[1]}, фамилия {info_user[2]}, id пользователя {info_user[0]}",
                    )
                )

        return ft.Container(
            image_src='/create_even.jpg',
            alignment=ft.alignment.center_left, expand=True,
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(ref=self.info_failed, value="""Создание события""",
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

                                        ft.Text(ref=self.info_failed,
                                                value="""Используйте только ЛАТИНСКИЕ буквы и цифры"""),
                                        ft.Text("Введите название события", size=18, italic=True),
                                        ft.TextField(ref=self.name_event, width=350, label="Название",
                                                     on_change=self.check_for_save_button),
                                        ft.Text("Введите описание события", size=18, italic=True),
                                        ft.TextField(ref=self.des_event, width=350, label="Описание",
                                                     on_change=self.check_for_save_button),
                                        ft.Text("Введите дату события", size=18, italic=True),
                                        ft.TextField(ref=self.data_event, width=350,
                                                     label="Дата",
                                                     on_change=self.check_for_save_button),
                                        ft.Text(ref=self.info_failed,
                                                value="""Введите дату события в формате YYYY-MM-DD,
                                        например, 2023-01-05""", size=14),
                                        ft.Text("Введите периодичность события", size=18, italic=True),
                                        ft.TextField(ref=self.repeat_event, width=350,
                                                     label="Периодичность",
                                                     on_change=self.check_for_save_button),
                                        ft.Text(ref=self.info_failed,
                                                value="""Введите периодичность события в формате 
                D или W или M или Y или N, где:
                                    D - ежедневно
                                    W - еженедельно
                                    M - ежемесячно
                                    Y - ежегодно
                                    N - разово""", size=14),

                                    ]
                                ),
                                ft.Container(
                                    expand=True
                                ),
                                ft.Column(
                                    [
                                        ft.Container(width=70, height=70, alignment=ft.alignment.center),
                                        # пустой контейнер
                                        ft.Text("Если хотите добавить гостей, выберите их", size=16, italic=True),
                                        ft.Container(
                                            content=self.guests_event,
                                            border=ft.border.all(2, ft.colors.BLUE),
                                            border_radius=10,
                                            padding=10,
                                            height=400,
                                        ),
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
                                    ]
                                )
                            ]
                        )
                    )
                ]

            )
        )

    def button_save_new_click(self, e: ft.ControlEvent):
        "Обработка нажатия на кнопку - Сохранить"

        def check_guests(self_in):
            "Проверка выбранных гостей"
            guests = []
            for elem in self_in.guests_event.controls:
                current_id_user = elem.label.split(" ")[-1]
                if elem.value:
                    guests.append(current_id_user)
            return guests

        if ((check_latin(self.name_event.current.value) is None) or
                (check_latin(self.des_event.current.value) is None)):
            dlg = ft.AlertDialog(title=ft.Text(f"Используйте только ЛАТИНСКИЕ буквы и цифры"))
            self.page.dialog = dlg  # мы у страницы указываем, что у нее имеется диалог
            dlg.open = True
        else:
            if not check_date(self.data_event.current.value):  # проверка, что ввели корректно дату
                dlg = ft.AlertDialog(title=ft.Text(f"Дата введена неправильно"))
                self.page.dialog = dlg  # мы у страницы указываем, что у нее имеется диалог
                dlg.open = True
            else:
                if (len(self.repeat_event.current.value) == 1) and (self.repeat_event.current.value in
                                                                    ["D", "W", "M", "Y", "N"]):
                    if self.repeat_event.current.value == "N":
                        self.repeat_event.current.value = None
                    Backend.add_new_event(name_event=self.name_event.current.value,
                                          description=self.des_event.current.value,
                                          event_owner=self.global_dict_state['id_user'],
                                          data_event=self.data_event.current.value,
                                          repeat_type=self.repeat_event.current.value,
                                          guests=check_guests(self),
                                          target_id_calendar=self.global_dict_state['id_calendar']
                                          )
                    dlg = ft.AlertDialog(title=ft.Text(f"Событие добавлено в календарь! 😎"))
                    self.page.dialog = dlg  # мы у страницы указываем, что у нее имеется диалог
                    dlg.open = True
                    self.name_event.current.value = ""
                    self.des_event.current.value = ""
                    self.data_event.current.value = ""
                    self.repeat_event.current.value = ""
                    for elem in self.guests_event.controls:
                        elem.value = False
                else:
                    dlg = ft.AlertDialog(title=ft.Text(f"Периодичность введена неправильно"))
                    self.page.dialog = dlg  # мы у страницы указываем, что у нее имеется диалог
                    dlg.open = True
        self.update()
        self.page.update()

    def check_for_save_button(self, e: ft.ControlEvent):
        "Активация кнопки - Сохранить"
        if (len(self.name_event.current.value) > 0 and len(self.des_event.current.value) > 0 and
                len(self.data_event.current.value) > 0 and len(self.repeat_event.current.value) > 0):
            self.button_save_new.current.disabled = False
        else:
            self.button_save_new.current.disabled = True
        self.update()


def check_latin(text: str):
    "Проверка на вхождение только правильных символов"
    pattern = re.compile("^[a-zA-Z0-9 ]*$")
    return pattern.match(text)
