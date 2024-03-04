import flet as ft
from Backend import Backend


class CalendarSection(ft.UserControl):
    """
    Класс реализующий левую секцию главного окна,
    где отображаются календари пользователей и
    кнопка добавления нового календаря
    """
    def __init__(self, page:ft.Page, global_dict_state: dict, callback_update_events):
        super().__init__()
        self.lst_cal = []
        self.page = page
        self.global_dict_state = global_dict_state
        self.callback_update_events = callback_update_events
        #self.expand = True

    def load_calendars(self):
        """
        Загрузка календарей пользователя
        """
        Backend.load_file_calendars(self.global_dict_state['id_user'])  # загружаем календари конкретного пользователя
        self.lst_cal = Backend.info_calendars()

    def build(self):
        self.load_calendars()
        calendar_column = ft.Ref[ft.Column]()
        result = ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(content=ft.Text('Календари'),alignment=ft.alignment.top_center,width=100),
                            ft.Container(
                                content=ft.Column(
                                    [
                                        CalendarIcon(
                                            self.page,
                                            elem.info_calendars(),
                                            self.global_dict_state,
                                            self.callback_update_events
                                        ) for elem in self.lst_cal
                                    ],
                                    ref=calendar_column
                                ),
                            ),
                            ft.Container(
                                content=CalendarIconAdd(self.page,'+')
                            ),
                        ],
                        #alignment=ft.MainAxisAlignment.CENTER
                    ),
                    width=120,
                    border=ft.border.all(1, ft.colors.PINK_600),
                    alignment=ft.alignment.top_center,
                    #height=500,
                    border_radius=10,
            #expand=True
        )
        return result


class CalendarIcon(ft.UserControl):
    """
    Кнопка календаря пользователя
    На вход подается:
    1) название календаря
    2) глобальный словарь, куда записывается id выбранного календаря
     Используется для понимания из какого календаря загружать события
    3) А так же подается колбек обновления ивентов в классе секции ивентов на главном экране
    """
    def __init__(self, page:ft.Page, info_calendar: list, global_dict_state: dict, callback_update_events):
        super().__init__()
        self.info_calendar = info_calendar # (self._id, self._name_calendar, self._id_user, self._events)
        self.page = page
        self.global_dict_state = global_dict_state
        self.callback_update_events = callback_update_events

    def popup(self, e: ft.ControlEvent):
        """
        Обработка события нажатия на кнопку редактирования календаря пользователя
        """
        self.page.go('/calendar')

    def click_calendar(self, e: ft.ControlEvent):
        """
        Нажатие на имя календаря выбирая конкретный календарь
        """
        self.global_dict_state['id_calendar'] = self.info_calendar[0]
        self.callback_update_events()

    def build(self):
        return ft.Container(
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=
                                    ft.IconButton(
                                        icon=ft.icons.EDIT,
                                        icon_size=30,
                                        on_click=self.popup,
                                        tooltip='Изменить календарь',
                                        #icon_color=ft.colors.BLACK,

                                    ),
                                height=40,
                                width=40,
                                #border=ft.border.all(1, ft.colors.PINK_600),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END
                    ),
                    ft.Container(
                        content=ft.TextButton(
                            text=self.info_calendar[1],
                            on_click=self.click_calendar,
                        ),
                        alignment=ft.alignment.bottom_center,
                    )
                ],
                alignment=ft.MainAxisAlignment.START
            ),
        # border = ft.border.all(1, ft.colors.PINK_600),
        # alignment=ft.alignment.top_center
        #bgcolor=ft.colors.AMBER,
        #alignment=ft.alignment.center,
        #alignment=ft.alignment.top_right,
        # expand=True,
        height=100,
        width=100,
        #border=ft.border.all(1, ft.colors.PINK_600),
        border_radius=10,
        image_src='calendar-icon-png-4122.png',

        )


class CalendarIconAdd(ft.UserControl):
    """
    Кнопка добавления нового календаря
    """
    def __init__(self, page:ft.Page, text=None):
        super().__init__()
        self.text = text
        self.page = page

    def popup(self, e: ft.ContainerTapEvent):
        """
        Обработка события нажатия на кнопку нового календаря
        """
        dlg = ft.AlertDialog(title=ft.Text("Форма добавления календаря"))
        self.page.dialog = dlg  # мы у страницы указываем, что у нее имеется диалог
        dlg.open = True
        self.page.update()

    def build(self):
        return ft.Container(
            image_src='calendar-icon-png-4122.png',
            content=ft.IconButton(
                icon=ft.icons.ADD,
                tooltip='Добавить новый календарь',
                on_click=self.popup,
            ),
            alignment=ft.alignment.center,
            #border = ft.border.all(1, ft.colors.PINK_600),
            # alignment=ft.alignment.top_center
            #bgcolor=ft.colors.AMBER,
            # alignment=ft.alignment.center,
            # alignment=ft.alignment.top_right,
            # expand=True,
            height=100,
            width=100,
            #border=ft.border.all(1, ft.colors.PINK_600),
            border_radius=10,
        )
