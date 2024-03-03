import flet as ft
from Backend import Backend
import re

class CalendarForm(ft.UserControl):
    "Создание страницы редактирования информации о календаре"
    def __init__(self, page, gl_id_user, target_id_calendar, name_calendar):
        super().__init__()
        self.expand = True  # если объект котнейнер возвращается как объект класса, то у него не работает свойство
        # expand, это свойство нужно указывать на уровне объекта этого класса
        self.page = page
        self.page.window_height = 600
        self.page.window_width = 850
        self.name_new_calendar = ft.Ref[ft.TextField]()
        self.info_failed = ft.Ref[ft.Text]()
        self.info_failed_user = ft.Ref[ft.Text]()
        self.button_save_new = ft.Ref[ft.ElevatedButton]()
        self.button_back = ft.Ref[ft.ElevatedButton]()
        self.target_id_calendar = target_id_calendar
        self.name_calendar = name_calendar
        self.gl_id_user = gl_id_user

    def build(self):
        self.load_calendars()
        return ft.Container(
            image_src='/1600-new.jpg',
            alignment=ft.alignment.center, expand=True,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.END,
                controls=
                [
                    ft.Text(ref=self.info_failed_user, value="""Изменение информации о календаре""",
                            size=40,
                            color=ft.colors.BLUE),
                    ft.Container(width=70, height=70, alignment=ft.alignment.center),  # пустой контейнер
                    ft.Text("Введите новое наименование календаря", size=18, italic=True),
                    ft.TextField(ref=self.name_new_calendar, width=350, label=self.name_calendar,
                                 on_change=self.check_for_save_button),
                    ft.Text(ref=self.info_failed, value="""Используйте только ЛАТИНСКИЕ буквы и цифры"""),
                    ft.Container(width=20, height=20, alignment=ft.alignment.center),  # пустой контейнер
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
                    ft.Container(width=1, height=1, alignment=ft.alignment.center),  # пустой контейнер
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

    def load_calendars(self):
        Backend.load_file_calendars(self.gl_id_user)  # загружаем календари конкретного пользователя в Backend


    def button_save_new_click(self, e: ft.ControlEvent):
        "Обработка нажатия на кнопку - Сохранить"
        if check_latin(self.name_new_calendar.current.value) is None:
            dlg = ft.AlertDialog(title=ft.Text(f"Используйте только ЛАТИНСКИЕ буквы и цифры"))
            self.page.dialog = dlg  # мы у страницы указываем, что у нее имеется диалог
            dlg.open = True
        else:
            Backend.update_calendar(target_id_calendar=self.target_id_calendar,
                                    new_name_calendar=self.name_new_calendar.current.value)
            dlg = ft.AlertDialog(title=ft.Text(f"Изменения выполнены успешно"))
            self.page.dialog = dlg  # мы у страницы указываем, что у нее имеется диалог
            dlg.open = True
        self.update()
        self.page.update()

    def check_for_save_button(self, e: ft.ControlEvent):
        "Активация кнопки - Сохранить"
        if len(self.name_new_calendar.current.value) > 0:
            self.button_save_new.current.disabled = False
        else:
            self.button_save_new.current.disabled = True
        self.update()

def check_latin(text: str):
    "Проверка на вхождение только правильных символов"
    pattern = re.compile("^[a-zA-Z0-9]*$")
    return pattern.match(text)

def test_run(page: ft.Page):
    page.add(CalendarForm(page, gl_id_user="@MishaIvanov*2", target_id_calendar="2", name_calendar="work"))

if __name__ == "__main__":
    ft.app(target=test_run, assets_dir="../assets")


