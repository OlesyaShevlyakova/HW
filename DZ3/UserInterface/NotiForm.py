import flet as ft
from Backend import Backend


class NotiForm(ft.UserControl):
    "Создание страницы просмотра сообщений"

    def __init__(self, page, global_dict_state):
        super().__init__()
        self.expand = True  # если объект котнейнер возвращается как объект класса, то у него не работает свойство
        # expand, это свойство нужно указывать на уровне объекта этого класса
        self.page = page
        self.page.window_height = 600
        self.page.window_width = 850
        self.page.title = "Окно оповещений"
        self.button_back = ft.Ref[ft.ElevatedButton]()
        self.global_dict_state = global_dict_state

    def build(self):
        noti = Backend.show_notifications_user(self.global_dict_state['id_user'])
        return ft.Container(
            image_src='/Noti.jpg',
            alignment=ft.alignment.center_right,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.END,
                controls=
                [
                    ft.Container(width=10, height=10, alignment=ft.alignment.center),  # пустой контейнер
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
                    ),
                    ft.Text("""Ваши оповещения""",
                            size=40,
                            color=ft.colors.RED),
                    ft.Container(width=10, height=10, alignment=ft.alignment.center),  # пустой контейнер
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(elem) for elem in noti
                            ],
                        ),
                        width=350,
                    ),  # контейнер с оповещениями
                    ft.Container(width=70, height=70, alignment=ft.alignment.center),  # пустой контейнер
                ]
            )
        )

