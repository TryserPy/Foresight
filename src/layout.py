import flet as ft
import pandas as pd
import os


DATA_FILE = "./data/budget.csv"
if not os.path.exists("./data"):
    os.makedirs("./data")
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["balance"])
    df.to_csv(DATA_FILE, index=False)





def main(page: ft.Page):

    page.title = "Flet Budget App"
    page.vertical_alignment = ft.MainAxisAlignment.START 

    body_area = ft.Column(expand=True)

    def get_balance_view():
        balance_field = ft.TextField(
            label="Введите ваши сумму расхода",
            hint_text="Введите число", 
            keyboard_type=ft.KeyboardType.NUMBER
            )
        trats = ft.Text("Траты", size=30, weight="bold")
        
        def add_balance(e):
            if not balance_field.value:
                return
            
            try:
                budget = pd.read_csv(DATA_FILE)
                new_row = pd.DataFrame({"balance": [int(balance_field.value)]})
                budget = pd.concat([budget, new_row], ignore_index=True)
                budget.to_csv(DATA_FILE, index=False)

                balance_field.value = ""
                page.open(ft.SnackBar(ft.Text("Запись добавлена")))
                page.update()
            
            except ValueError:
                balance_field.error_text = "Только числа!"
                balance_field.update()



        return ft.Column(
            controls=[
                trats,
                ft.Divider(),
                ft.Row([
                    balance_field,
                    ft.ElevatedButton("Добавить", on_click=add_balance),
                ], alignment=ft.MainAxisAlignment.CENTER)
            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )



    def get_profile_view():
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.CircleAvatar(content=ft.Text("USER")),
                    ft.Text("Имя пользователя"),
                    ft.Switch(label="Темная тема")
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=20,
            bgcolor=ft.Colors.BLUE_GREY_100,
            border_radius=10
        )

    def get_stats_view():
        budget = pd.read_csv(DATA_FILE, index_col=False)

        return ft.Column(
            controls=[
                ft.Row(
                    [
                        ft.Text(budget["balance"].tail(10).to_string(index=False))
                    ], alignment=ft.MainAxisAlignment.CENTER
                )
            ]
        )


    def navigate(e):

        index = e.control.selected_index
        body_area.controls.clear()

        if index == 0:
            body_area.controls.append(get_balance_view())
        elif index == 1:
            body_area.controls.append(get_stats_view())

        body_area.update()

    
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.HOME, label="Траты"),
            ft.NavigationBarDestination(icon=ft.icons.PERSON, label="Профиль")
        ],
        on_change=navigate
    )


    body_area.controls.append(get_balance_view())
    page.add(body_area)