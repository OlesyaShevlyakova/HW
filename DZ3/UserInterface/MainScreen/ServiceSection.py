import flet as ft


class ServiceSection(ft.UserControl):
    def __init__(self, page: ft.Page, global_dict_state: dict):
        super().__init__()
        self.page = page
        self.global_dict_state = global_dict_state

    def build(self):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Text(
                            # value='Пользователь',
                            value='',
                            size=13),
                        alignment=ft.alignment.top_center,
                        # width = 100,
                    ),
                    ft.Container(
                        content=ServiceSectionButton(
                            page=self.page,
                            text='Изменить информацию о пользователе',
                            route='change_user_info',
                            icon=ft.icons.SETTINGS,
                        )
                    ),
                    ft.Container(
                        content=ServiceSectionButton(
                            page=self.page,
                            text='Посмотреть события',
                            route='view_notifications',
                            icon=ft.icons.NOTIFICATIONS,
                        )
                    ),
                    ft.Container(expand=True),
                    ft.Container(
                        content=ServiceSectionButton(
                            page=self.page,
                            text='Выйти на страницу авторизации',
                            route='back_to_login',
                            icon=ft.icons.EXIT_TO_APP,
                        ),
                        bgcolor=ft.colors.TRANSPARENT,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            # content=ft.Container(ft.Text('123')),
            width=120,
            border=ft.border.all(1, ft.colors.PINK_600),
            border_radius=10,
        )


class ServiceSectionButton(ft.UserControl):
    def __init__(self, page:ft.Page,text,route,icon):
        super().__init__()
        self.page = page
        self.text = text
        self.route = route
        self.icon = icon

    def popup(self, e: ft.ContainerTapEvent):
        #dlg = ft.AlertDialog(title=ft.Text(self.text))
        #self.page.dialog = dlg  # мы у страницы указываем, что у нее имеется диалог
        #dlg.open = True
        #self.page.update()
        self.page.go('/login')

    def build(self):
        return ft.Container(
            content=ft.IconButton(
                    icon=self.icon,
                    icon_color="blue400",
                    icon_size=35,
                    tooltip=self.text,
                    on_click=self.popup,
            ),
            alignment=ft.alignment.center,
            #on_click=self.popup,
            #border = ft.border.all(1, ft.colors.PINK_600),
            # alignment=ft.alignment.top_center
            #bgcolor=ft.colors.WHITE,
            # alignment=ft.alignment.center,
            # alignment=ft.alignment.top_right,
            # expand=True,
            height=50,
            width=50,
            #border=ft.border.all(1, ft.colors.PINK_600),
        )
