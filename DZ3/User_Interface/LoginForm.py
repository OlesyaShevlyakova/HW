import flet as ft
from Backend import Backend
class LoginForm(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.expand = True  # если объект котнейнер возвращается как объект класса, то у него не работает свойство
        # expand, это свойство нужно указывать на уровне объекта этого класса
        self.page = page
        self.login_field = ft.TextField(width=400, label="Логин",
                                        on_change=self.check_for_login_button)  # текстовое поле для ввода логина
        self.password_field = ft.TextField(width=400, label="Пароль",
                                           on_change=self.check_for_login_button)  # текстовое поле для ввода пароля
        self.login_failed = ft.Text("""Неправильный логин\пароль, либо пользователя не существует! 
                Повторите попытку или зарегистрируйте нового пользователя!""", visible=False)
        self.button_come_in = ft.ElevatedButton(
            width=150,
            content=ft.Row(
                [
                    ft.Icon(name=ft.icons.CALENDAR_MONTH, color="pink"),
                    ft.Text(value="Войти", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.LIGHT_BLUE_800),
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND),
            on_click=self.button_come_in_click, disabled=True)  # кнопка "Войти"
        self.button_reg = ft.TextButton(    # кнопка "Регистрация"
            content=ft.Text(
                value="Регистрация",
                size=18,
                weight=ft.FontWeight.BOLD
            ),
            on_click=lambda _: self.page.go('/reg'))  # Возвращает на окно регистрации


    def build(self):
        return ft.Container(
            image_src='/photo1708283759.jpeg',
            alignment=ft.alignment.center,
            expand=True,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=
                [
                    ft.Container(width=100, height=100, alignment=ft.alignment.center),  # пустой контейнер
                    ft.Text("Введите логин", size=20, italic=True),
                    self.login_field,
                    ft.Text("Введите пароль", size=20, italic=True),
                    self.password_field,
                    self.button_come_in,
                    self.button_reg,
                    self.login_failed
                ]
            )
        )
    def check_for_login_button(self, e: ft.ControlEvent):
        "Скрытие надписи об ошибке и активация кнопки"
        self.login_failed.visible = False
        if len(self.password_field.value) > 0 and len(self.login_field.value) > 0:
            self.button_come_in.disabled = False
        else:
            self.button_come_in.disabled = True
        self.update()

    def button_come_in_click(self, e: ft.ControlEvent):
        "Обработка нажатия на кнопку - Войти"
        flag = Backend.auth_user(self.login_field.value, self.password_field.value)
        if not flag:
            self.login_failed.visible = True
            self.button_come_in.disabled = True
        else:
            dlg = ft.AlertDialog(title=ft.Text(f"Авторизация выполнена успешно, Ваш id {flag}"))
            self.page.dialog = dlg  # мы у страницы указываем, что у нее имеется диалог
            dlg.open = True
        self.password_field.value = ""
        self.update()
        self.page.update()
