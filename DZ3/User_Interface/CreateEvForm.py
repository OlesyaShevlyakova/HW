import flet as ft
from Backend import Backend
import re

class CreateEvForm(ft.UserControl):
    "Создание страницы события"
    def __init__(self, page, gl_id_user):
        super().__init__()
        self.expand = True  # если объект котнейнер возвращается как объект класса, то у него не работает свойство
        # expand, это свойство нужно указывать на уровне объекта этого класса
        self.page = page
        self.page.window_height = 850
        self.page.window_width = 1150
        self.page.title = "Окно создания события"
        self.login_new = ft.Ref[ft.TextField]()
        self.name_new = ft.Ref[ft.TextField]()
        self.lastname_new = ft.Ref[ft.TextField]()
        self.password_new = ft.Ref[ft.TextField]()
        self.calendar_new = ft.Ref[ft.TextField]()
        self.info_failed = ft.Ref[ft.Text]()
        self.button_reg_new = ft.Ref[ft.ElevatedButton]()
        self.button_back = ft.Ref[ft.ElevatedButton]()
        self.gl_id_user = gl_id_user
    def build(self):
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
                                            ft.TextField(ref=self.login_new, width=350, label="Название",
                                                         on_change=self.check_for_reg_button),
                                            ft.Text("Введите описание события", size=18, italic=True),
                                            ft.TextField(ref=self.password_new, width=350, label="Описание",
                                                         on_change=self.check_for_reg_button),
                                            ft.Text("Введите дату события", size=18, italic=True),
                                            ft.TextField(ref=self.name_new, width=350,
                                                         label="Дата",
                                                         on_change=self.check_for_reg_button),
                                            ft.Text(ref=self.info_failed,
                                                    value="""Введите дату события в формате YYYY-MM-DD,
                                        например, 2023-01-05""", size=14),
                                            ft.Text("Введите периодичность события", size=18, italic=True),
                                            ft.TextField(ref=self.lastname_new, width=350,
                                                         label="Периодичность",
                                                         on_change=self.check_for_reg_button),
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
                                            ft.Text("Если хотите добавить гостей, укажите их id", size=16, italic=True),
                                            ft.TextField(ref=self.calendar_new, width=400, label="id пользователей",
                                                         on_change=self.check_for_reg_button),

                                            ft.ElevatedButton(
                                                ref=self.button_reg_new,
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
                                                on_click=lambda _: self.page.go('/login')
                                            )  # Возвращает на окно логина
                                        ]
                                    )
                                ]
                            )
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
        else:
            if not Backend.originality_login(self.login_new.current.value):
                dlg = ft.AlertDialog(title=ft.Text(f"Введите другой логин, данный логин уже существует"))
                self.page.dialog = dlg  # мы у страницы указываем, что у нее имеется диалог
                dlg.open = True
            else:
                result_back = Backend.reg_user(login_user=self.login_new.current.value,
                                               name_user=self.name_new.current.value,
                                               lastname_user=self.lastname_new.current.value,
                                               password_user=self.password_new.current.value)
                Backend.add_new_calendar(id_user=result_back, name_calendar=self.calendar_new.current.value)
                dlg = ft.AlertDialog(title=ft.Text(f"Регистрация выполнена успешно, Ваш id {result_back}"))
                self.gl_id_user = result_back  # чтобы сохранить id user для последующего использования
                self.page.dialog = dlg  # мы у страницы указываем, что у нее имеется диалог
                dlg.open = True
        self.update()
        self.page.update()

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