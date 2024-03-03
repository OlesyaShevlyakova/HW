import flet as ft
from Backend import Backend


class NotiForm(ft.UserControl):
    "Создание страницы просмотра сообщений"
    def __init__(self, page, gl_id_user):
        super().__init__()
        self.expand = True  # если объект котнейнер возвращается как объект класса, то у него не работает свойство
        # expand, это свойство нужно указывать на уровне объекта этого класса
        self.page = page
        self.page.window_height = 600
        self.page.window_width = 850
        self.page.title = "Окно оповещений"
        self.info_failed_user = ft.Ref[ft.Text]()
        self.button_back = ft.Ref[ft.ElevatedButton]()
        self.gl_id_user = gl_id_user

    def build(self):
        noti = Backend.show_notifications_user(self.gl_id_user)
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
                        on_click=lambda _: self.page.go('/login')  # Возвращает на окно логина  #TODO
                    ),
                    ft.Text(ref=self.info_failed_user, value="""Ваши оповещения""",
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



if __name__ == "__main__":
    ft.app(target=test_run, assets_dir="../assets")