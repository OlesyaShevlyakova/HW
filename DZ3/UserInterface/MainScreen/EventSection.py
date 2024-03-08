import flet as ft
from Backend import Backend


class EventsSection(ft.UserControl):
    """
    Центральная секция, где отображаются события из календарей пользователей
    """
    def __init__(self, page:ft.Page, global_dict_state: dict):
        super().__init__()
        self.page = page
        self.expand = True
        self.lst_events = []
        self.global_dict_state = global_dict_state
        self.grid_events = ft.GridView(
            expand=1,
            runs_count=5,
            max_extent=250,
            child_aspect_ratio=1.0,
            spacing=5,
            run_spacing=5,
        )

    def load_events(self):
        """
        Загрузка событий конкретного календаря
        """
        if self.global_dict_state["id_calendar"] != "":
            self.lst_events = Backend.show_events(self.global_dict_state["id_calendar"])

    def build(self):
        self.update_grid_events()
        return ft.Container(
            content=self.grid_events,
            #content=ft.Container(ft.Text('123')),
            #width=500,
            #expand=True,
            border=ft.border.all(1, ft.colors.PINK_600),
            border_radius=10,
            padding=20,
        )

    def update_grid_events(self):
        """
        Обновление грида, с отображаемыми событиями
        Сначала загружаем события из памяти бекенда, потом добавляем их в грид в виде
        экземпляров класса Event
        """
        self.load_events()
        if len(self.lst_events) != 0:
            self.grid_events.controls = []
            for elem in self.lst_events:
                self.grid_events.controls.append(
                    ft.Container(
                        content=
                        ft.Row(
                            [
                                Event(elem.info_Event()),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        width=100,
                        height=100,
                        border=ft.border.all(1, ft.colors.PINK_600),
                        border_radius=10,

                    ),
                )
        else:
            self.grid_events.controls.append(ft.Text('Выберите слева календарь, щёлкнув по его имени.'))

    def update_state(self):
        """
        Обновление состояния грида событий.
        Используется в колбеках от выбора конкретного календаря
        """
        self.update_grid_events()
        self.update()


class Event(ft.UserControl):
    """
    Класс реализующий форму отображения события из календаря пользователя
    """
    def __init__(self, info_event: tuple):
        super().__init__()
        self.info_event = info_event

    def build(self):
        if len(self.info_event[6]) > 0:
            guests = 'Да'
        else:
            guests = 'Нет'
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(value = f'Название: {self.info_event[1]}'),
                    ft.Text(value = f'Описание: {self.info_event[2]}'),
                    ft.Text(value = f'Дата: {self.info_event[3]}'),
                    ft.Text(value = f'Повторение: {self.info_event[4]}'),
                    ft.Text(value=f'Гости: {guests}',),
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            #padding=20,
            #width=500,
            #height=500
        )
