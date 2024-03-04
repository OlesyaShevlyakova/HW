import flet as ft
from User_Interface.MainScreen.CalendarSection import CalendarSection
from User_Interface.MainScreen.EventSection import EventsSection
from User_Interface.MainScreen.ServiceSection import ServiceSection


class MainScreen(ft.UserControl):
    """
    Класс реализующий отображение ссновного экрана приложения,
    где отображаются календари, события и сервисные элементы.
    """
    def __init__(self, page:ft.Page, global_dict_state: dict):
        super().__init__()
        self.page = page
        self.page.window_center()
        self.page.window_width = 1180  # ширина внешнего окна
        self.page.window_height = 700  # высота внешнего окна
        self.page.title = 'Главное окно'
        self.expand = True
        self.global_dict_state = global_dict_state # Прокидываем глобальный словарь

        # Прописываем в переменные классы отвечающий каждый за свой блок.
        # Делается для того, чтобы можно было их обновлять в callback.
        self.calendar_section = CalendarSection(self.page, self.global_dict_state, self.callback_update_events)
        self.event_section = EventsSection(self.page, self.global_dict_state)
        self.service_section = ServiceSection(self.page, self.global_dict_state)

    def build(self):
        return ft.Container(
            image_src='/mainscreen_fon.jpg',
            content=ft.Column(
                [
                    ft.Row(
                        [
                            self.calendar_section,
                            self.event_section,
                            self.service_section,
        ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.START,
                    )
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