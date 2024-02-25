import flet as ft
from Backend import Backend

class LoginForm(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.expand = True  # если объект котнейнер возвращается как объект класса, то у него не работает свойство
        # expand, это свойство нужно указывать на уровне объекта этого класса
        self.page = page

