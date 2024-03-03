import flet as ft
from User_Interface.LoginForm import LoginForm
from User_Interface.RegForm import RegForm
from User_Interface.UserForm import UserForm
from User_Interface.CalendarForm import CalendarForm
from User_Interface.MainScreenForm import MainScreen
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
                        CalendarForm(page, gl_id_user="@MishaIvanov*2", target_id_calendar="2", name_calendar="personal")
                    ]
                )
            )
        elif page.route == "/mainscreen":
            page.views.append(
                ft.View(
                    route="/mainscreen",
                    controls=[
                        MainScreen(page)
                    ]
                )
            )

    gl_id_user = None
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  # расположение внутренних окон по центру относительно ширины
    page.on_route_change = route_change
    page.go('/login')





if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")