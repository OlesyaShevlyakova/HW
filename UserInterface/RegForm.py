import flet as ft
from Backend import Backend
import re


class RegForm(ft.UserControl):
    "Создание страницы регистрации"

    def __init__(self, page, global_dict_state):
        super().__init__()
        self.expand = True  # если объект котнейнер возвращается как объект класса, то у него не работает свойство
        # expand, это свойство нужно указывать на уровне объекта этого класса
        self.page = page
        self.page.window_height = 700
        self.page.window_width = 1000
        self.page.title = "Окно регистрации"
        self.login_new = ft.Ref[ft.TextField]()
        self.name_new = ft.Ref[ft.TextField]()
        self.lastname_new = ft.Ref[ft.TextField]()
        self.password_new = ft.Ref[ft.TextField]()
        self.calendar_new = ft.Ref[ft.TextField]()
        self.button_reg_new = ft.Ref[ft.ElevatedButton]()
        self.button_back = ft.Ref[ft.ElevatedButton]()
        self.global_dict_state = global_dict_state

    def build(self):
        return ft.Container(
            image_src='/8430432.jpg',
            alignment=ft.alignment.center, expand=True,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=
                [
                    ft.Container(width=10, height=10, alignment=ft.alignment.center),  # пустой контейнер
                    ft.Text("Введите логин", size=16, italic=True),
                    ft.TextField(ref=self.login_new, width=400, label="Логин",
                                 on_change=self.check_for_reg_button),
                    ft.Text("Введите пароль", size=16, italic=True),
                    ft.TextField(ref=self.password_new, width=400, label="Пароль",
                                 on_change=self.check_for_reg_button),
                    ft.Text("Введите имя", size=16, italic=True),
                    ft.TextField(ref=self.name_new, width=400, label="Имя",
                                 on_change=self.check_for_reg_button),
                    ft.Text("Введите фамилию", size=16, italic=True),
                    ft.TextField(ref=self.lastname_new, width=400, label="Фамилия",
                                 on_change=self.check_for_reg_button),
                    ft.Text("Введите название календаря", size=16, italic=True),
                    ft.TextField(ref=self.calendar_new, width=400, label="Название календаря",
                                 on_change=self.check_for_reg_button),
                    ft.Text("""Используйте только ЛАТИНСКИЕ буквы и цифры"""),
                    ft.ElevatedButton(
                        ref=self.button_reg_new,
                        disabled=True,
                        adaptive=True,
                        bgcolor=ft.cupertino_colors.SYSTEM_TEAL,
                        content=ft.Row(
                            [
                                ft.Icon(name=ft.icons.FAVORITE, color="pink"),
                                ft.Text("Зарегистрироваться", size=18, weight=ft.FontWeight.BOLD),
                            ],
                            tight=True
                        ),
                        on_click=self.button_reg_new_click),
                    ft.ElevatedButton(
                        ref=self.button_back,
                        width=150,
                        content=ft.Row(
                            [
                                ft.Icon(name=ft.icons.BACKUP, color="blue"),
                                ft.Text(value="Назад", size=20, color=ft.colors.LIGHT_BLUE_800),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_AROUND),
                        on_click=lambda _: self.page.go('/login')  # Возвращает на окно логина
                    )
                ]
            )
        )

    def button_reg_new_click(self, e: ft.ControlEvent):
        "Обработка нажатия на кнопку - Зарегистрироваться"
        if ((check_latin(self.login_new.current.value) is None) or
                (check_latin(self.name_new.current.value) is None) or
                (check_latin(self.lastname_new.current.value) is None) or
                (check_latin(self.password_new.current.value) is None) or
                (check_latin(self.calendar_new.current.value) is None)):
            dlg = ft.AlertDialog(title=ft.Text(f"Используйте только ЛАТИНСКИЕ буквы и цифры"))
            self.page.dialog = dlg  # мы у страницы указываем, что у нее имеется диалог
            dlg.open = True
            self.update()
            self.page.update()
        else:
            if not Backend.originality_login(self.login_new.current.value):
                dlg = ft.AlertDialog(title=ft.Text(f"Введите другой логин, данный логин уже существует"))
                self.page.dialog = dlg  # мы у страницы указываем, что у нее имеется диалог
                dlg.open = True
                self.update()
                self.page.update()
            elif len(self.login_new.current.value) < 8:
                dlg = ft.AlertDialog(title=ft.Text(f"Пароль слишком короткий, требуется минимум 8 символов"))
                self.page.dialog = dlg  # мы у страницы указываем, что у нее имеется диалог
                dlg.open = True
                self.update()
                self.page.update()
            else:
                result_back = Backend.reg_user(login_user=self.login_new.current.value,
                                               name_user=self.name_new.current.value,
                                               lastname_user=self.lastname_new.current.value,
                                               password_user=self.password_new.current.value)
                Backend.add_new_calendar(id_user=result_back, name_calendar=self.calendar_new.current.value)
                dlg = ft.AlertDialog(title=ft.Text(f"Регистрация выполнена успешно, Ваш id {result_back}"))
                self.global_dict_state['id_user'] = result_back  # чтобы сохранить id user для последующего использования
                self.global_dict_state['login_user'] = self.login_new.current.value
                self.page.dialog = dlg  # мы у страницы указываем, что у нее имеется диалог
                dlg.open = True
                self.page.go('/mainscreen')

    def check_for_reg_button(self, e: ft.ControlEvent):
        "Активация кнопки - Зарегистрироваться"
        if (len(self.login_new.current.value) > 0 and len(self.name_new.current.value) > 0 and
                len(self.lastname_new.current.value) > 0 and len(self.password_new.current.value) > 0 and
                len(self.calendar_new.current.value) > 0):
            self.button_reg_new.current.disabled = False
        else:
            self.button_reg_new.current.disabled = True
        self.update()


def check_latin(text: str):
    "Проверка на вхождение только правильных символов"
    pattern = re.compile("^[a-zA-Z0-9]*$")
    return pattern.match(text)
