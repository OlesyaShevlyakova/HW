import flet as ft
from User_Interface.MainScreen.CalendarSection import CalendarSection
from User_Interface.MainScreen.EventSection import EventsSection
from User_Interface.MainScreen.ServiceSection import ServiceSection



class MainScreen(ft.UserControl):
    def __init__(self, page:ft.Page, gl_id_user: dict):
        super().__init__()
        self.page = page
        self.page.window_center()
        self.page.window_width = 1180  # ширина внешнего окна
        self.page.window_height = 700  # высота внешнего окна
        self.page.title = 'Главное окно'
        self.expand = True
        self.gl_id_user = gl_id_user


    def build(self):
        return ft.Container(
            image_src='/mainscreen_fon.jpg',
            content=ft.Column(
                [
                    ft.Row(
                        [
                            CalendarSection(self.page, self.gl_id_user),
                            #ft.VerticalDivider(width=1, thickness=1, color="black"),
                            #ft.VerticalDivider(width=90, thickness=30),
                            EventsSection(self.page, self.gl_id_user),
                            ServiceSection(self.page, self.gl_id_user),
                        ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.START,
                    )
                ],
                expand=True
            )
        )