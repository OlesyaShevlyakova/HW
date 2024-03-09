import flet as ft
from UserInterface.LoginForm import LoginForm
from UserInterface.RegForm import RegForm
from UserInterface.UserForm import UserForm
from UserInterface.CalendarForm import CalendarForm
from UserInterface.MainScreenForm import MainScreen
from UserInterface.CreateCalForm import CreateCalForm
from UserInterface.NotiForm import NotiForm
from UserInterface.CreateEvForm import CreateEvForm


def run():
    ft.app(target=main, assets_dir="assets")


def main(page: ft.Page):
    def route_change(e: ft.RouteChangeEvent):
        "Обработка перехода между окнами"
        page.views.clear()
        if page.route == "/login": # Форма логина в приложение
            page.views.append(
                ft.View(
                    route="/login",
                    controls=[
                        LoginForm(page, global_dict_state)
                    ]
                )
            )
        elif page.route == "/reg": # Форма регистрации нового пользователя
            page.views.append(
                ft.View(
                    route="/reg",
                    controls=[
                        RegForm(page, global_dict_state)
                    ]
                )
            )
        elif page.route == "/user": # Форма редактирования информации о пользователе
            page.views.append(
                ft.View(
                    route="/user",
                    controls=[
                        UserForm(page, global_dict_state)
                    ]
                )
            )
        elif page.route == "/calendar": # Форма редактирования информации о календаре
            page.views.append(
                ft.View(
                    route="/calendar",
                    controls=[
                        CalendarForm(page, global_dict_state)
                    ]
                )
            )
        elif page.route == "/mainscreen": # Форма главного окна приложения
            page.views.append(
                ft.View(
                    route="/mainscreen",
                    controls=[
                        MainScreen(page, global_dict_state)
                    ]
                )
            )
        elif page.route == "/create_cal": # Форма создания календаря
            page.views.append(
                ft.View(
                    route="/create_cal",
                    controls=[
                        CreateCalForm(page, global_dict_state)
                    ]
                )
            )
        elif page.route == "/noti": # Форма просмотра оповещений
            page.views.append(
                ft.View(
                    route="/noti",
                    controls=[
                        NotiForm(page, global_dict_state="@MishaIvanov*2")
                    ]
                )
            )

        elif page.route == "/create_ev": # Форма создания событий
            page.views.append(
                ft.View(
                    route="/create_ev",
                    controls=[
                        CreateEvForm(page, global_dict_state="@MishaIvanov*2")
                    ]
                )
            )

    # Глобальный словарь, пока не поняла как правильно передавать данные между view, буду прокидывать словарь, который
    # передается не как значение, а как ссылка, так как является словарем, а не просто переменной
    global_dict_state = {
        'id_user': "",
        'id_calendar': "",
        'name_calendar': "",
        'CalendarForm_id_calendar':'',
        'CalendarForm_name_calendar':''
    }
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  # помещаем внутренние окна по центру относительно ширины
    page.on_route_change = route_change
    page.go('/login')


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")