import flet as ft
from User_Interface.LoginForm import LoginForm
from User_Interface.RegForm import RegForm
from User_Interface.UserForm import UserForm
from User_Interface.CalendarForm import CalendarForm
gl_id_user = None

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
        elif page.route == "/user":
            page.views.append(
                ft.View(
                    route="/user",
                    controls=[
                        UserForm(page, gl_id_user)
                    ]
                )
            )
        elif page.route == "/calendar":
            page.views.append(
                ft.View(
                    route="/calendar",
                    controls=[
                        CalendarForm(page, "2", "work")
                    ]
                )
            )

    gl_id_user = None
    page.title = "Окно авторизации"
    page.window_width = 850  # ширина внешнего окна
    page.window_height = 600  # высота внешнего окна
    page.window_resizable = False  # запрет изменения размера окна
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  # расположение внутренних окон по центру относительно ширины
    page.on_route_change = route_change
    #page.go('/login')
    #page.go('/user')
    page.go('/calendar')





if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")