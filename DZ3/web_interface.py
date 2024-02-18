import flet as ft
from Backend import Backend

def run():
    ft.app(target=main, assets_dir="assets")
def main(page: ft.Page):
    def button_come_in_click(e):
        "Обработка нажатия на кнопку - Войти"
        flag = Backend.auth_user(login_field.value, password_field.value)
        if not flag:
            login_failed.visible = True
        else:
            dlg = ft.AlertDialog(title=ft.Text(f"Авторизация выполнена успешно, Ваш id {flag}"))
            page.dialog = dlg  # мы у страницы указываем, что у нее имеется диалог
            dlg.open = True
        password_field.value = ""
        page.update()

    def button_reg_click(e):
        "Обработка нажатия на кнопку - Регистрация"
        def button_reg_new_click(e):
            "Обработка нажатия на кнопку - Зарегистрироваться"
            if not Backend.originality_login(login_new.value):
                dlg = ft.AlertDialog(title=ft.Text(f"Введите другой логин, данный логин уже существует"))
                page.dialog = dlg  # мы у страницы указываем, что у нее имеется диалог
                dlg.open = True
            else:
                result_back = Backend.reg_user(login_user=login_new.value, name_user=name_new.value, lastname_user=lastname_new.value, password_user=password_new.value)
                dlg = ft.AlertDialog(title=ft.Text(f"Регистрация выполнена успешно, Ваш id {result_back}"))
                page.dialog = dlg  # мы у страницы указываем, что у нее имеется диалог
                dlg.open = True
            page.update()

        def check_for_reg_button(e):
            "Активация кнопки - Зарегистрироваться"
            if len(login_new.value) > 0 and len(name_new.value) > 0 and len(lastname_new.value) > 0 and len(password_new.value) > 0:
                button_reg_new.disabled = False
            page.update()

        page.clean()  # очистка страницы
        login_new = ft.TextField(width=400, label="Логин", on_change=check_for_reg_button)
        name_new = ft.TextField(width=400, label="Имя", on_change=check_for_reg_button)
        lastname_new = ft.TextField(width=400, label="Фамилия", on_change=check_for_reg_button)
        password_new = ft.TextField(width=400, label="Пароль", on_change=check_for_reg_button)
        info_failed = ft.Text("""Используйте только ЛАТИНСКИЕ буквы""")
        button_reg_new = ft.ElevatedButton(disabled=True,
            adaptive=True,  # a CupertinoButton will be rendered when running on apple-platform
            bgcolor=ft.cupertino_colors.SYSTEM_TEAL,
            content=ft.Row(
                [
                    ft.Icon(name=ft.icons.FAVORITE, color="pink"),
                    ft.Text("Зарегистрироваться"),
                ],
                tight=True), on_click=button_reg_new_click)
        page.add(ft.Container(image_src='/8430432.jpg',
                              alignment=ft.alignment.center, expand=True,
                              content=ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, controls=[
            ft.Text("Введите логин"),
            login_new,
            ft.Text("Введите пароль"),
            password_new,
            ft.Text("Введите Имя"),
            name_new,
            ft.Text("Введите Фамилию"),
            lastname_new,
            info_failed,
            button_reg_new])))
        page.update()

    def check_for_login_button(e):
        "Скрытие надписи об ошибке и активация кнопки"
        login_failed.visible = False
        if len(password_field.value) > 0 and len(login_field.value) > 0:
            button_come_in.disabled = False
        page.update()


    page.title = "Окно авторизации"
    page.window_width = 750  # ширина внешнего окна
    page.window_height = 550  # высота внешнего окна
    page.window_resizable = False  # запрет изменения размера окна
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  # расположение внутренних окон по центру относительно ширины
    #page.vertical_alignment = ft.MainAxisAlignment.CENTER  # расположение внутренних окон по центру относительно высоты
    login_field = ft.TextField(width=400, label="Логин", on_change=check_for_login_button)  # текстовое поле для ввода логина
    password_field = ft.TextField(width=400, label="Пароль", on_change=check_for_login_button)  # текстовое поле для ввода пароля
    login_failed = ft.Text("""Неправильный логин\пароль, либо пользователя не существует! 
Повторите попытку или зарегистрируйте нового пользователя!""", visible=False)
    button_come_in = ft.ElevatedButton(width=150,
            content=ft.Row(
                [
                    ft.Icon(name=ft.icons.CALENDAR_MONTH, color="pink"),
                    ft.Text(value="Войти", size=20, color=ft.colors.LIGHT_BLUE_800),
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND), on_click=button_come_in_click, disabled=True)  # кнопка "Войти"
    button_reg = ft.TextButton(text="Регистрация", on_click=button_reg_click)  # кнопка "Регистрация"
    page.add(ft.Container(image_src='/photo1708283759.jpeg',
                          alignment=ft.alignment.center, expand=True,
                          content=ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, controls=[
        ft.Container(width=100, height=100, alignment=ft.alignment.center),
        ft.Text("Введите логин"),
            login_field,
            ft.Text("Введите пароль"),
            password_field,
            button_come_in,
            button_reg])))
    page.add(login_failed)
    page.update()






if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")