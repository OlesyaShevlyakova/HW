import flet as ft
from Backend import Backend
class LoginForm(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.expand = True  # если объект котнейнер возвращается как объект класса, то у него не работает свойство
        # expand, это свойство нужно указывать на уровне объекта этого класса
        self.page = page
        self.login_field = ft.Ref[ft.TextField]()   # текстовое поле для ввода логина
        self.password_field = ft.Ref[ft.TextField]()   # текстовое поле для ввода пароля
        self.login_failed = ft.Ref[ft.Text]()
        self.button_come_in = ft.Ref[ft.ElevatedButton]()
        self.button_reg = ft.Ref[ft.ElevatedButton]()
        self.page.title = "Окно авторизации"
        self.page.window_width = 850  # ширина внешнего окна
        self.page.window_height = 600  # высота внешнего окна
        #self.page.window_resizable = False  # запрет изменения размера окна


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
                    ft.TextField(ref=self.login_field, width=400, label="Логин", on_change=self.check_for_login_button),
                    ft.Text("Введите пароль", size=20, italic=True),
                    ft.TextField(ref=self.password_field, width=400, label="Пароль",
                                 on_change=self.check_for_login_button),
                    ft.ElevatedButton(
                        ref=self.button_come_in,
                        width=150,
                        content=ft.Row(
                            [
                                ft.Icon(name=ft.icons.CALENDAR_MONTH, color="pink"),
                                ft.Text(value="Войти", size=20, weight=ft.FontWeight.BOLD,
                                        color=ft.colors.LIGHT_BLUE_800),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_AROUND),
                        on_click=self.button_come_in_click, disabled=True),  # кнопка "Войти"
                    ft.ElevatedButton(
                        ref=self.button_reg,
                        content=ft.Text(
                            value="Регистрация",
                            size=18,
                            weight=ft.FontWeight.BOLD
                        ),
                        on_click=lambda _: self.page.go('/reg')),  # Возвращает на окно регистрации
                    ft.Text(ref=self.login_failed, value="""Неправильный логин\пароль, либо пользователя не существует! 
                Повторите попытку или зарегистрируйте нового пользователя!""", visible=False)
                ]
            )
        )
    def check_for_login_button(self, e: ft.ControlEvent):
        "Скрытие надписи об ошибке и активация кнопки"
        self.login_failed.current.visible = False
        if len(self.password_field.current.value) > 0 and len(self.login_field.current.value) > 0:
            self.button_come_in.current.disabled = False
        else:
            self.button_come_in.current.disabled = True
        self.update()

    def button_come_in_click(self, e: ft.ControlEvent):
        "Обработка нажатия на кнопку - Войти"
        flag = Backend.auth_user(self.login_field.current.value, self.password_field.current.value)
        if not flag:
            self.login_failed.current.visible = True
            self.button_come_in.current.disabled = True
            self.update()
            self.page.update()
        else:
            #dlg = ft.AlertDialog(title=ft.Text(f"Авторизация выполнена успешно, Ваш id {flag}"))
            global gl_id_user
            gl_id_user = flag  # чтобы сохранить id user для последующего использования
            #self.page.dialog = dlg  # мы у страницы указываем, что у нее имеется диалог
            #dlg.open = True
            self.page.go('/mainscreen')
        self.password_field.current.value = ""
        #self.update()
        #self.page.update()
