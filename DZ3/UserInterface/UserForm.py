import flet as ft
from Backend import Backend
import re


class UserForm(ft.UserControl):
    "Создание страницы редактирования информации о пользователе"

    def __init__(self, page, global_dict_state):
        super().__init__()
        self.expand = True  # если объект котнейнер возвращается как объект класса, то у него не работает свойство
        # expand, это свойство нужно указывать на уровне объекта этого класса
        self.page = page
        self.page.window_height = 600
        self.page.window_width = 850
        self.page.title = "Окно редактирования информации о пользователе"
        self.name_new = ft.Ref[ft.TextField]()
        self.lastname_new = ft.Ref[ft.TextField]()
        self.password_new = ft.Ref[ft.TextField]()
        self.info_failed = ft.Ref[ft.Text]()
        self.info_failed_user = ft.Ref[ft.Text]()
        self.button_save_new = ft.Ref[ft.ElevatedButton]()
        self.button_back = ft.Ref[ft.ElevatedButton]()
        self.info_our_user = None
        self.global_dict_state = global_dict_state

    def build(self):
        self.load_user()
        return ft.Container(
            image_src='/user-1.jpg',
            alignment=ft.alignment.center, expand=True,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.END,
                controls=
                [
                    ft.Text(ref=self.info_failed_user, value="""Изменение информации о пользователе""",
                            size=40,
                            color=ft.colors.BROWN),
                    ft.Container(width=15, height=15, alignment=ft.alignment.center),  # пустой контейнер
                    ft.Text("Введите новое имя", size=16, italic=True),
                    ft.TextField(ref=self.name_new, width=400, label=self.info_our_user[1],
                                 on_change=self.check_for_save_button),
                    ft.Text("Введите новую фамилию", size=16, italic=True),
                    ft.TextField(ref=self.lastname_new, width=400, label=self.info_our_user[2],
                                 on_change=self.check_for_save_button),
                    ft.Text("Введите новый пароль", size=16, italic=True),
                    ft.TextField(ref=self.password_new, width=400, label="Пароль",
                                 on_change=self.check_for_save_button),
                    ft.Text(ref=self.info_failed, value="""Используйте только ЛАТИНСКИЕ буквы и цифры"""),
                    ft.ElevatedButton(
                        ref=self.button_save_new,
                        disabled=True,
                        adaptive=True,
                        bgcolor=ft.cupertino_colors.SYSTEM_TEAL,
                        content=ft.Row(
                            [
                                ft.Icon(name=ft.icons.SAVE, color="pink"),
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
                        on_click=lambda _: self.page.go('/login')  # Возвращает на окно логина  #TODO
                    )
                ]
            )
        )

    def load_user(self):
        Backend.load_file_users(self.global_dict_state)  # загружаем конкретного пользователя в Backend
        self.info_our_user = Backend.info_users()[0].info_User()  # информация о текущем пользователе

    def button_save_new_click(self, e: ft.ControlEvent):
        "Обработка нажатия на кнопку - Сохранить"
        if ((check_latin(self.name_new.current.value) is None) or
                (check_latin(self.lastname_new.current.value) is None) or
                (check_latin(self.password_new.current.value) is None)):
            dlg = ft.AlertDialog(title=ft.Text(f"Используйте только ЛАТИНСКИЕ буквы и цифры"))
            self.page.dialog = dlg  # мы у страницы указываем, что у нее имеется диалог
            dlg.open = True
        else:
            if len(self.name_new.current.value) == 0:
                new_name = None
            else:
                new_name = self.name_new.current.value
            if len(self.lastname_new.current.value) == 0:
                new_lastname = None
            else:
                new_lastname = self.lastname_new.current.value
            if len(self.password_new.current.value) == 0:
                new_password = None
            else:
                new_password = self.password_new.current.value
            Backend.update_user(target_login=self.info_our_user[3], new_name=new_name, new_lastname=new_lastname,
                                new_password=new_password)
            dlg = ft.AlertDialog(title=ft.Text(f"Изменения выполнены успешно"))
            self.page.dialog = dlg  # мы у страницы указываем, что у нее имеется диалог
            dlg.open = True
        self.update()
        self.page.update()

    def check_for_save_button(self, e: ft.ControlEvent):
        "Активация кнопки - Сохранить"
        if (len(self.name_new.current.value) > 0 or
                len(self.lastname_new.current.value) > 0 or len(self.password_new.current.value) > 0):
            self.button_save_new.current.disabled = False
        else:
            self.button_save_new.current.disabled = True
        self.update()


def check_latin(text: str):
    "Проверка на вхождение только правильных символов"
    pattern = re.compile("^[a-zA-Z0-9]*$")
    return pattern.match(text)
