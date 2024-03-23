import flet as ft
from Backend import Backend
import re


class CreateCalForm(ft.UserControl):
    "Создание календаря"

    def __init__(self, page, global_dict_state):
        super().__init__()
        self.expand = True  # если объект котнейнер возвращается как объект класса, то у него не работает свойство
        # expand, это свойство нужно указывать на уровне объекта этого класса
        self.page = page
        self.page.window_height = 700
        self.page.window_width = 1000
        self.page.title = "Окно создания календаря"
        self.calendar_new = ft.Ref[ft.TextField]()
        self.button_save_new = ft.Ref[ft.ElevatedButton]()
        self.button_back = ft.Ref[ft.ElevatedButton]()
        self.global_dict_state = global_dict_state

    def build(self):
        self.load_calendars()
        return ft.Container(
            image_src='/CreateCal-2.jpg',
            alignment=ft.alignment.center_right,
            expand=True,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.END,
                controls=
                [
                    ft.Container(width=10, height=10, alignment=ft.alignment.center),  # пустой контейнер
                    ft.Text("""Создание календаря""",
                            size=40,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.BLUE),
                    ft.Container(width=70, height=70, alignment=ft.alignment.center),  # пустой контейнер
                    ft.Text("Введите название календаря", size=18, italic=True),
                    ft.Container(width=5, height=5, alignment=ft.alignment.center),  # пустой контейнер
                    ft.TextField(ref=self.calendar_new, width=400, label="Название календаря",
                                 on_change=self.check_for_save_button),
                    ft.Container(width=5, height=5, alignment=ft.alignment.center),  # пустой контейнер
                    ft.Text("""Используйте только ЛАТИНСКИЕ буквы и цифры""", size=16),
                    ft.Container(width=5, height=5, alignment=ft.alignment.center),  # пустой контейнер
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
                        on_click=lambda _: self.page.go('/mainscreen')  # Возвращает на окно логина
                    )
                ]
            )
        )

    def button_save_new_click(self, e: ft.ControlEvent):
        "Обработка нажатия на кнопку - Сохранить"
        if check_latin(self.calendar_new.current.value) is None:
            dlg = ft.AlertDialog(title=ft.Text(f"Используйте только ЛАТИНСКИЕ буквы и цифры"))
            self.page.dialog = dlg  # мы у страницы указываем, что у нее имеется диалог
            dlg.open = True
            self.update()
            self.page.update()
        else:
            Backend.add_new_calendar(id_user=self.global_dict_state['id_user'],
                                     name_calendar=self.calendar_new.current.value)
            dlg = ft.AlertDialog(title=ft.Text(f"Календарь успешно создан"))
            self.page.dialog = dlg  # мы у страницы указываем, что у нее имеется диалог
            dlg.open = True
            self.update()
            self.page.update()
            self.page.go('/mainscreen')

    def load_calendars(self):
        Backend.load_file_calendars(self.global_dict_state['id_user'])  # загружаем календари конкретного пользователя в Backend

    def check_for_save_button(self, e: ft.ControlEvent):
        "Активация кнопки - Сохранить"
        if len(self.calendar_new.current.value) > 0:
            self.button_save_new.current.disabled = False
        else:
            self.button_save_new.current.disabled = True
        self.update()


def check_latin(text: str):
    "Проверка на вхождение только правильных символов"
    pattern = re.compile("^[a-zA-Z0-9]*$")
    return pattern.match(text)
