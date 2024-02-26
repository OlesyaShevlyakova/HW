import flet as ft
from Backend import Backend


class RegForm(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.expand = True  # если объект котнейнер возвращается как объект класса, то у него не работает свойство
        # expand, это свойство нужно указывать на уровне объекта этого класса
        self.page = page
        self.login_new = ft.Ref[ft.TextField]()
        self.name_new = ft.TextField(width=400, label="Имя", on_change=self.check_for_reg_button)
        self.lastname_new = ft.TextField(width=400, label="Фамилия", on_change=self.check_for_reg_button)
        self.password_new = ft.TextField(width=400, label="Пароль", on_change=self.check_for_reg_button)
        self.info_failed = ft.Text("""Используйте только ЛАТИНСКИЕ буквы""")
        self.button_reg_new = ft.ElevatedButton(
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
            on_click=self.button_reg_new_click)
        self.button_back = ft.ElevatedButton(    # кнопка "Назад"
            width=150,
            content=ft.Row(
                [
                    ft.Icon(name=ft.icons.BACKUP, color="blue"),
                    ft.Text(value="Назад", size=20, color=ft.colors.LIGHT_BLUE_800),
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND),
            on_click=lambda _: self.page.go('/login')  # Возвращает на окно логина
            )

    def build(self):
        return ft.Container(
                image_src='/8430432.jpg',
                alignment=ft.alignment.center, expand=True,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=
                    [
                        ft.Container(width=20, height=20, alignment=ft.alignment.center),  # пустой контейнер
                        ft.Text("Введите логин", size=16, italic=True),
                        ft.TextField(ref=self.login_new,  width=400, label="Логин", on_change=self.check_for_reg_button),
                        ft.Text("Введите пароль", size=16, italic=True),
                        self.password_new,
                        ft.Text("Введите имя", size=16, italic=True),
                        self.name_new,
                        ft.Text("Введите фамилию", size=16, italic=True),
                        self.lastname_new,
                        self.info_failed,
                        self.button_reg_new,
                        self.button_back
                    ]
                )
            )

    def button_reg_new_click(self, e: ft.ControlEvent):
        "Обработка нажатия на кнопку - Зарегистрироваться"
        if not Backend.originality_login(self.login_new.current.value):
            dlg = ft.AlertDialog(title=ft.Text(f"Введите другой логин, данный логин уже существует"))
            self.page.dialog = dlg  # мы у страницы указываем, что у нее имеется диалог
            dlg.open = True
        else:
            result_back = Backend.reg_user(login_user=self.login_new.current.value, name_user=self.name_new.value, lastname_user=self.lastname_new.value, password_user=self.password_new.value)
            dlg = ft.AlertDialog(title=ft.Text(f"Регистрация выполнена успешно, Ваш id {result_back}"))
            self.page.dialog = dlg  # мы у страницы указываем, что у нее имеется диалог
            dlg.open = True
        self.update()
        self.page.update()

    def check_for_reg_button(self, e: ft.ControlEvent):
        "Активация кнопки - Зарегистрироваться"
        if len(self.login_new.current.value) > 0 and len(self.name_new.value) > 0 and len(self.lastname_new.value) > 0 and len(self.password_new.value) > 0:
            self.button_reg_new.disabled = False
        else:
            self.button_reg_new.disabled = True
        self.update()

