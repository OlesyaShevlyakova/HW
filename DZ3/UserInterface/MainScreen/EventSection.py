import flet as ft
from Backend import Backend


class EventsSection(ft.UserControl):
    """
    Центральная секция, где отображаются события из календарей пользователей
    """

    def __init__(self, page: ft.Page, global_dict_state: dict):
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
            # content=ft.Container(ft.Text('123')),
            # width=500,
            # expand=True,
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
                                Event(elem.info_Event(), self.global_dict_state),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        width=100,
                        height=100,
                        border=ft.border.all(1, ft.colors.PINK_600),
                        border_radius=10,

                    ),
                ),
            self.grid_events.controls.append(
                ft.Container(
                    content=
                    ft.Row(
                        [
                            EventAdd(),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    width=100,
                    height=100,
                    border=ft.border.all(1, ft.colors.PINK_600),
                    border_radius=10,

                ),
            )
        elif self.global_dict_state['id_calendar'] == '':
            self.grid_events.controls = []
            self.grid_events.controls.append(ft.Text('Выберите слева календарь, щёлкнув по его имени.'))
        else:
            self.grid_events.controls = []
            self.grid_events.controls.append(
                ft.Container(
                    content=
                    ft.Row(
                        [
                            EventAdd(),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    width=100,
                    height=100,
                    border=ft.border.all(1, ft.colors.PINK_600),
                    border_radius=10,
                )
            )

    def update_grid_events_by_date(self):
        """
        Обновление грида, с учетом фильтра по датам
        """
        if len(self.lst_events) != 0:
            self.grid_events.controls = []
            for elem in self.lst_events:
                self.grid_events.controls.append(
                    ft.Container(
                        content=
                        ft.Row(
                            [
                                Event(elem[0].info_Event(), self.global_dict_state, elem[1]),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        width=100,
                        height=100,
                        border=ft.border.all(1, ft.colors.PINK_600),
                        border_radius=10,

                    ),
                ),
            self.grid_events.controls.append(
                ft.Container(
                    content=
                    ft.Row(
                        [
                            EventAdd(),
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
            self.grid_events.controls = []
            self.grid_events.controls.append(ft.Text('События не обнаружены. Выберите другой фильтр по дате или '
                                                     'выберите заново календарь'))

    def update_state(self):
        """
        Обновление состояния грида событий.
        Используется в колбеках от выбора конкретного календаря
        """
        self.update_grid_events()
        self.update()

    def update_state_by_date(self, date_start, date_end):
        self.lst_events = Backend.search_events_for_webinterface(str(date_start), str(date_end),
                                                                 self.global_dict_state["id_calendar"])
        self.update_grid_events_by_date()
        self.update()


class Event(ft.UserControl):
    """
    Класс реализующий форму отображения события из календаря пользователя
    """

    def __init__(self, info_event: tuple, global_dict_state: dict, repeated_event=None):
        super().__init__()
        self.info_event = info_event
        self.repeated_event = repeated_event
        self.repeated_event_object = ft.Text(value=f'Дата с учетом повторения\nсобытия: {self.repeated_event}', size=12)
        self.global_dict_state = global_dict_state

    def build(self):
        self.global_dict_state['id_event_for_edit'] = self.info_event[0]
        if self.repeated_event is not None:
            self.repeated_event_object.visible = True
        else:
            self.repeated_event_object.visible = False
        if len(self.info_event[6]) > 0:
            guests = 'Да'
        else:
            guests = 'Нет'
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(value=f'Название: {self.info_event[1]}', size=12),
                    ft.Text(value=f'Описание: {self.info_event[2]}', size=12),
                    ft.Text(value=f'Дата: {self.info_event[3]}', size=12),
                    ft.Text(value=f'Повторение: {self.info_event[4]}', size=12),
                    ft.Text(value=f'Гости: {guests}', size=12),
                    self.repeated_event_object,
                    ft.Container(
                        content=ft.IconButton(
                            icon=ft.icons.EDIT_ATTRIBUTES,
                            tooltip='Редактировать событие',
                            on_click=lambda _: self.page.go('/edit_event'),
                        ),
                        alignment=ft.alignment.bottom_right,
                        width=180,
                        # border=ft.border.all(2, ft.colors.BLACK)
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=5,
            ),
            # padding=20,
            # width=500,
            # height=500
        )


class EventAdd(ft.UserControl):
    """
    Класс реализующий форму отображения события из календаря пользователя
    """

    def __init__(self):
        super().__init__()

    def click_add_event(self):
        pass

    def build(self):
        return ft.Container(
            content=ft.IconButton(
                icon=ft.icons.ADD_CIRCLE_OUTLINE,
                tooltip='Добавить новое событие',
                on_click=lambda _: self.page.go("/create_ev"),
            ),
            alignment=ft.alignment.center,
            # border = ft.border.all(1, ft.colors.PINK_600),
            # alignment=ft.alignment.top_center
            # bgcolor=ft.colors.AMBER,
            # alignment=ft.alignment.center,
            # alignment=ft.alignment.top_right,
            # expand=True,
            # height=100,
            # width=100,
            # border=ft.border.all(1, ft.colors.PINK_600),
            # border_radius=10,
        )
