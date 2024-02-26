import flet as ft
from User_Interface.LoginForm import LoginForm
from User_Interface.RegForm import RegForm



def run():
    ft.app(target=main, assets_dir="assets")
def main(page: ft.Page):
    def route_change(e: ft.RouteChangeEvent):
        "Обработка перехода между окнами"
        page.views.clear()
        if page.route == "/login":
            page.views.append(
                ft.View(
                    route="/login",
                    controls=[
                        LoginForm(page)
                    ]
                )
            )
        elif page.route == "/reg":
            page.views.append(
                ft.View(
                    route="/reg",
                    controls=[
                        RegForm(page)
                    ]
                )
            )

    page.title = "Окно авторизации"
    page.window_width = 850  # ширина внешнего окна
    page.window_height = 600  # высота внешнего окна
    page.window_resizable = False  # запрет изменения размера окна
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  # расположение внутренних окон по центру относительно ширины
    page.on_route_change = route_change
    page.go('/login')



if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")