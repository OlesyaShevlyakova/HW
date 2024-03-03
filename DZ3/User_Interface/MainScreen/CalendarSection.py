import flet as ft
from Backend import Backend

id_user='@OlesyaShevlyakova*1'

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
            content=ft.IconButton(
                icon=ft.icons.ADD,
                tooltip='Добавить новый календарь',
                on_click=self.popup,
            ),
            alignment=ft.alignment.center,
            #border = ft.border.all(1, ft.colors.PINK_600),
            # alignment=ft.alignment.top_center
            bgcolor=ft.colors.AMBER,
            # alignment=ft.alignment.center,
            # alignment=ft.alignment.top_right,
            # expand=True,
            height=100,
            width=100,
            border=ft.border.all(1, ft.colors.PINK_600),
            border_radius=10,
        )


class CalendarIcon(ft.UserControl):
    """
    Кнопка календаря пользователя
    На вход подается text - название календаря пользователя
    """
    def __init__(self, page:ft.Page, text=None):
        super().__init__()
        self.text = text
        self.page = page
    def popup(self, e: ft.ContainerTapEvent):
        """Обработка события нажатия на кнопку редактирования календаря пользователя"""
        dlg = ft.AlertDialog(title=ft.Text("Форма редактирования"))
        self.page.dialog = dlg  # мы у страницы указываем, что у нее имеется диалог
        dlg.open = True
        self.page.update()

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
                                        icon_size=20,
                                        on_click=self.popup,
                                        tooltip='Изменить календарь',
                                    ),
                                height=30,
                                width=30,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END
                    ),
                    ft.Container(
                        content=ft.TextButton(text=self.text),
                        alignment=ft.alignment.bottom_center,
                    )
                ],
                alignment=ft.MainAxisAlignment.START
            ),
        # border = ft.border.all(1, ft.colors.PINK_600),
        # alignment=ft.alignment.top_center
        bgcolor=ft.colors.AMBER,
        #alignment=ft.alignment.center,
        #alignment=ft.alignment.top_right,
        # expand=True,
        height=100,
        width=100,
        border=ft.border.all(1, ft.colors.PINK_600),
        border_radius=10,
        )


class CalendarSection(ft.UserControl):
    """
    Левая секция главного окна, где отображаются календари пользователей
    """
    def __init__(self, page:ft.Page, text=None):
        super().__init__()
        self.lst_cal = []
        self.page = page
        #self.expand = True

    def load_calendars(self):
        # Загружаем календари пользователя
        Backend.load_file_calendars(id_user)  # загружаем календари конкретного пользователя
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
                                        CalendarIcon(self.page, elem.info_calendars()[1]) for elem in self.lst_cal
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