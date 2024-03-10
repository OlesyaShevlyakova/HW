import flet as ft
from UserInterface.MainScreen.CalendarSection import CalendarSection
from UserInterface.MainScreen.EventSection import EventsSection
from UserInterface.MainScreen.ServiceSection import ServiceSection



class MainScreen(ft.UserControl):
    """
    Класс реализующий отображение ссновного экрана приложения,
    где отображаются календари, события и сервисные элементы.
    """

    def __init__(self, page: ft.Page, global_dict_state: dict):
        super().__init__()
        self.page = page
        self.page.window_width = 1180  # ширина внешнего окна
        self.page.window_height = 700  # высота внешнего окна
        self.page.window_center()
        self.page.title = 'Главное окно'
        self.expand = True
        self.global_dict_state = global_dict_state  # Прокидываем глобальный словарь

        # Прописываем в переменные классы отвечающий каждый за свой блок.
        # Делается для того, чтобы можно было их обновлять в callback.
        self.calendar_section = CalendarSection(self.page, self.global_dict_state, self.callback_update_events)
        self.event_section = EventsSection(self.page, self.global_dict_state)
        self.service_section = ServiceSection(self.page, self.global_dict_state)

        # Кнопки фильтра дат
        self.button_start_date = ft.Ref[ft.ElevatedButton]()
        self.button_end_date = ft.Ref[ft.ElevatedButton]()
        self.button_apply_date = ft.Ref[ft.IconButton]()
        self.button_cancel_date = ft.Ref[ft.IconButton]()
        self.date_picker_start = ft.DatePicker(
            on_change=self.change_date_start,
            #on_dismiss=self.date_picker_dismissed_start,
            # first_date=datetime.datetime(2023, 10, 1),
            # last_date=datetime.datetime(2024, 10, 1),
        )
        self.date_picker_end = ft.DatePicker(
            on_change=self.change_date_end,
            #on_dismiss=self.selfdate_picker_dismissed_end,
            # first_date=datetime.datetime(2023, 10, 1),
            # last_date=datetime.datetime(2024, 10, 1),
        )
        self.page.overlay.append(self.date_picker_start)
        self.page.overlay.append(self.date_picker_end)


    def change_date_end(self, e: ft.ControlEvent):
        self.button_end_date.current.text = self.date_picker_end.value.date()
        self.update()

    def change_date_start(self, e: ft.ControlEvent):
        self.button_start_date.current.text = self.date_picker_start.value.date()
        #self.date_picker_end.first_date = datetime.datetime(2024, 10, 1),  # self.date_picker_start.value
        # if self.button_end_date.current.text == 'Дата конца':
        #     print(self.date_picker_start.value)
        #     print(type(self.date_picker_start.value))
            #self.date_picker_end.first_date = datetime.datetime(2024, 10, 1), #self.date_picker_start.value
            #first_date = datetime.datetime(2023, 10, 1),
        self.update()
        #self.date_picker_end.update()
        #self.page.update()

    def click_cancel_date(self, e: ft.ControlEvent):
        self.callback_update_events()

    def click_apply_date(self, e: ft.ControlEvent):
        if self.global_dict_state['id_calendar'] == '':
            dlg = ft.AlertDialog(title=ft.Text(f"Выберите календарь"))
            self.page.dialog = dlg  # мы у страницы указываем, что у нее имеется диалог
            dlg.open = True
            self.page.update()
        elif self.button_start_date.current.text == 'Дата начала' or self.button_end_date.current.text == 'Дата конца':
            dlg = ft.AlertDialog(title=ft.Text(f"Выберите обе даты"))
            self.page.dialog = dlg  # мы у страницы указываем, что у нее имеется диалог
            dlg.open = True
            self.page.update()
        else:
            self.callback_update_events_by_date(self.button_start_date.current.text, self.button_end_date.current.text)






    def build(self):
        return ft.Container(
            image_src='/mainscreen_fon.jpg',
            content=ft.Column(
                [
                    ft.Container(
                        content=
                            ft.Row(
                                [
                                    ft.ElevatedButton(
                                        ref=self.button_start_date,
                                        icon=ft.icons.CALENDAR_MONTH,
                                        text='Дата начала',
                                        on_click=lambda _: self.date_picker_start.pick_date(),
                                    ),
                                    ft.ElevatedButton(
                                        ref=self.button_end_date,
                                        icon=ft.icons.CALENDAR_MONTH,
                                        text='Дата конца',
                                        on_click=lambda _: self.date_picker_end.pick_date(),
                                    ),
                                    ft.IconButton(
                                        ref=self.button_apply_date,
                                        icon=ft.icons.CHECK_CIRCLE_OUTLINED,
                                        on_click=self.click_apply_date,
                                        tooltip='Применить фильтр',
                                    ),
                                    ft.IconButton(
                                        ref=self.button_cancel_date,
                                        icon=ft.icons.CANCEL_OUTLINED,
                                        on_click=self.click_cancel_date,
                                        tooltip='Сбросить фильтр',
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                        height=50,
                        #border=ft.border.all(1, ft.colors.PINK_600),
                        alignment=ft.alignment.bottom_center,
                    ),
                    ft.Row(
                        [
                            self.calendar_section,
                            self.event_section,
                            self.service_section,
                        ],
                        expand=True,
                        alignment=ft.MainAxisAlignment.START,
                    ),
                ],
                expand=True
            )
        )

    def callback_update_events(self):
        """
        Колбек вызова обновления секции ивентов
        Вызывается при выборе конкретного календаря
        """
        self.event_section.update_state()
        self.button_start_date.current.text = 'Дата начала'
        self.button_end_date.current.text = 'Дата конца'
        self.update()

    def callback_update_events_by_date(self, date_start, date_end):
        """
        Колбек вызова обновления секции ивентов по дате
        Вызывается при выборе диапазона дат
        """
        self.event_section.update_state_by_date(date_start, date_end)

    # def date_picker_popup(self):

