import flet as ft
from User_Interface.LoginForm import LoginForm
from User_Interface.RegForm import RegForm
from User_Interface.UserForm import UserForm
from User_Interface.CalendarForm import CalendarForm
from User_Interface.MainScreenForm import MainScreen
from User_Interface.CreateCalForm import CreateCalForm
from User_Interface.NotiForm import NotiForm
from User_Interface.CreateEvForm import CreateEvForm

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
                        LoginForm(page, gl_id_user)
                    ]
                )
            )
        elif page.route == "/reg":
            page.views.append(
                ft.View(
                    route="/reg",
                    controls=[
                        RegForm(page, gl_id_user)
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
                        MainScreen(page, gl_id_user)
                    ]
                )
            )
        elif page.route == "/create_cal":
            page.views.append(
                ft.View(
                    route="/create_cal",
                    controls=[
                        CreateCalForm(page, gl_id_user="@OlesyaShevlyakova*1")
                    ]
                )
            )
        elif page.route == "/noti":
            page.views.append(
                ft.View(
                    route="/noti",
                    controls=[
                        NotiForm(page, gl_id_user="@MishaIvanov*2")
                    ]
                )
            )

        elif page.route == "/create_ev":
            page.views.append(
                ft.View(
                    route="/create_ev",
                    controls=[
                        CreateEvForm(page, gl_id_user="@MishaIvanov*2")
                    ]
                )
            )

    # Глобальный словарь, пока не поняла как правильно передавать данные между view
    gl_id_user = {
        'id_user': "",
        'id_calendar': "",
        'name_calendar': ""
    }
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  # расположение внутренних окон по центру относительно ширины
    page.on_route_change = route_change
    #page.go('/login')
    page.go('/create_ev')





if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")