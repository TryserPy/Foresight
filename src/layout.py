import datetime
import flet as ft
import csv
import os


DATA_FILE = "data/budget.csv"

APP_THEMES = {
    "dark_modern": {
        "mode": ft.ThemeMode.DARK,
        "bg": "#1f2128",
        "card_bg": "#292b36",
        "accent": "#6C5DD3",
        "text_main": "#FFFFFF",
        "text_sec": "#808191",
        "gradient": ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=["#6C5DD3", "#8B5CF6"]
        )
    },
    "light_clean": {
        "mode": ft.ThemeMode.LIGHT,
        "bg": "#F4F5F9",
        "card_bg": "#FFFFFF",
        "accent": "#4D7CFE",
        "text_main": "#1A1D1F",
        "text_sec": "#9A9FA5",
        "gradient": ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=["#4D7CFE", "#2C5AFF"]
        )
    },
    "neon_cyber": {
        "mode": ft.ThemeMode.DARK,
        "bg": "#050505",
        "card_bg": "#111111",
        "accent": "#00FF99",
        "text_main": "#E0E0E0",
        "text_sec": "#555555",
        "gradient": ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=["#00FF99", "#00CCFF"]
        )
    },
    "sunset_glow": {
        "mode": ft.ThemeMode.DARK,
        "bg": "#2D1B2E",
        "card_bg": "#442340",
        "accent": "#FFAB00",
        "text_main": "#FFD700",
        "text_sec": "#B08D9F",
        "gradient": ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=["#FF512F", "#DD2476"]
        )
    },
    "ocean_breeze": {
        "mode": ft.ThemeMode.LIGHT,
        "bg": "#E0F7FA",
        "card_bg": "#FFFFFF",
        "accent": "#00BCD4",
        "text_main": "#006064",
        "text_sec": "#68888A",
        "gradient": ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=["#00BCD4", "#26C6DA"]
        )
    }
}

TRANSLATIONS = {
    "ru": {
        "nav_dashboard": "Обзор", "nav_input": "Ввод", "nav_ai": "AI Анализ", "nav_history": "История", 
        "nav_wallet": "Кошелек", "nav_settings": "Настройки",
        "settings_title": "Настройки", "lang_label": "Язык", "curr_label": "Валюта",
        "win_size": "Размер окна", "win_resize": "Растягивание окна",
        "credits": "Об авторе", "theme_label": "Тема оформления"
    },
    "en": {
        "nav_dashboard": "Dashboard", "nav_input": "Input", "nav_ai": "AI Insight", "nav_history": "History", 
        "nav_wallet": "Wallet", "nav_settings": "Settings",
        "settings_title": "Settings", "lang_label": "Language", "curr_label": "Currency",
        "win_size": "Window Size", "win_resize": "Resizable Window",
        "credits": "Credits", "theme_label": "App Theme"
    }
}

class DataMoneyApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "DataMoney | AI Budget"
        self.page.padding = 0
        self.page.window.min_width = 1100
        self.page.window.min_height = 700
        
        self.page.fonts = {
            "Poppins": "https://fonts.gstatic.com/s/poppins/v20/pxiByp8kv8JHgFVrLGT9Z1xlFQ.woff2"
        }
        self.page.theme = ft.Theme(font_family="Poppins")

        self.current_lang = "ru"
        self.currency_symbol = "RUB"

        self.start_balance = 50000.0 
        self.is_balance_editing = False 

        self.transactions = [
            {"id": 1, "date": "2023-10-25", "category": "Еда", "amount": 1250.0, "comment": "Бизнес-ланч"},
            {"id": 2, "date": "2023-10-24", "category": "Транспорт", "amount": 450.0, "comment": "Такси"},
            {"id": 3, "date": "2023-10-23", "category": "Софт", "amount": 990.0, "comment": "Подписка"},
            {"id": 4, "date": "2023-10-22", "category": "Еда", "amount": 3200.0, "comment": "Продукты"},
            {"id": 5, "date": "2023-10-20", "category": "Развлечения", "amount": 1500.0, "comment": "Кино"},
        ]
        self.last_id = 5
        
        self.selected_ids = set()
        self.is_edit_mode = False
        self.search_query = ""

        self.current_theme_key = "dark_modern"
        self.theme = APP_THEMES[self.current_theme_key]

        self._init_components()
        
        self.content_area = ft.Container(expand=True, padding=35)
        self.nav_rail = self._build_nav_rail()
        
        self.apply_theme(self.current_theme_key)
        self._update_data_driven_ui()

    def _init_components(self):
        self.kpi_expense_text = ft.Text("0", size=26, weight=ft.FontWeight.BOLD)
        self.kpi_balance_text = ft.Text("0", size=26, weight=ft.FontWeight.BOLD)
        
        self.chart_dashboard = ft.Image(
            src="https://placehold.co/800x350/292b36/FFF?text=Dynamic+Chart+Update",
            width=800, height=350, fit=ft.ImageFit.CONTAIN, border_radius=15,
        )
        self.chart_analytics = ft.Image(
             src="https://placehold.co/800x450/292b36/FFF?text=Heatmap+Visualization",
            width=800, height=450, fit=ft.ImageFit.CONTAIN, border_radius=15,
        )

        self.amount_input = ft.TextField(
            label="Сумма", suffix_text=self.currency_symbol, 
            keyboard_type=ft.KeyboardType.NUMBER, border_radius=12,
            input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9.]", replacement_string="")
        )
        self.category_dropdown = ft.Dropdown(
            label="Категория", border_radius=12,
            options=[
                ft.dropdown.Option("Еда"), 
                ft.dropdown.Option("Транспорт"), 
                ft.dropdown.Option("Софт"), 
                ft.dropdown.Option("Развлечения"),
                ft.dropdown.Option("Шоппинг"),
                ft.dropdown.Option("Здоровье")
            ]
        )
        self.comment_input = ft.TextField(
            label="Комментарий", multiline=True, max_lines=3, border_radius=12
        )

        self.wallet_input = ft.TextField(
            label="Стартовый баланс", suffix_text=self.currency_symbol,
            keyboard_type=ft.KeyboardType.NUMBER, border_radius=12,
            input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9.]", replacement_string="")
        )

        self.table_recent = ft.DataTable(
            width=float("inf"), border_radius=10, column_spacing=20,
            columns=[
                ft.DataColumn(ft.Text("Дата")),
                ft.DataColumn(ft.Text("Категория")),
                ft.DataColumn(ft.Text("Сумма"), numeric=True),
            ],
            rows=[]
        )

        self.history_table = ft.DataTable(
            width=float("inf"),
            sort_column_index=0,
            sort_ascending=True,
            show_checkbox_column=False,
            on_select_all=self.select_all_transactions,
            columns=[
                ft.DataColumn(ft.Text("Дата"), on_sort=lambda e: self.sort_history(0, e.ascending)),
                ft.DataColumn(ft.Text("Категория"), on_sort=lambda e: self.sort_history(1, e.ascending)),
                ft.DataColumn(ft.Text("Комментарий")),
                ft.DataColumn(ft.Text("Сумма"), numeric=True, on_sort=lambda e: self.sort_history(3, e.ascending)),
            ],
            rows=[]
        )
        
        self.search_field = ft.TextField(
            hint_text="Поиск...", 
            prefix_icon=ft.Icons.SEARCH,
            border_radius=15,
            height=40,
            content_padding=10,
            text_size=14,
            on_change=self.on_search_change
        )
        
        self.ml_insight_text = ft.Text("Анализ расходов...", size=15)

    def _build_nav_rail(self):
        t = self.theme
        txt = TRANSLATIONS[self.current_lang]
        return ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            bgcolor=t["card_bg"],
            indicator_color=t["accent"],
            indicator_shape=ft.CircleBorder(),
            min_width=100,
            min_extended_width=200,
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(icon=ft.Icons.DASHBOARD_OUTLINED, selected_icon=ft.Icons.DASHBOARD, label=txt["nav_dashboard"]),
                ft.NavigationRailDestination(icon=ft.Icons.ADD_CIRCLE_OUTLINE, selected_icon=ft.Icons.ADD_CIRCLE, label=txt["nav_input"]),
                ft.NavigationRailDestination(icon=ft.Icons.INSIGHTS_OUTLINED, selected_icon=ft.Icons.INSIGHTS, label=txt["nav_ai"]),
                ft.NavigationRailDestination(icon=ft.Icons.HISTORY_OUTLINED, selected_icon=ft.Icons.HISTORY, label=txt["nav_history"]),
                ft.NavigationRailDestination(icon=ft.Icons.ACCOUNT_BALANCE_WALLET_OUTLINED, selected_icon=ft.Icons.ACCOUNT_BALANCE_WALLET, label=txt["nav_wallet"]),
                ft.NavigationRailDestination(icon=ft.Icons.SETTINGS_OUTLINED, selected_icon=ft.Icons.SETTINGS, label=txt["nav_settings"]),
            ],
            on_change=self.navigate
        )

    def select_all_transactions(self, e):
        query = self.search_query.lower()
        visible = [t for t in self.transactions if query in t["category"].lower() or query in t["comment"].lower()]
        
        if e.data == "true":
            for t in visible:
                self.selected_ids.add(t["id"])
        else:
            for t in visible:
                self.selected_ids.discard(t["id"])
        
        self._update_data_driven_ui()

    def _update_data_driven_ui(self):
        total_expense = sum(t["amount"] for t in self.transactions)
        current_balance = self.start_balance - total_expense

        self.kpi_expense_text.value = f"{total_expense:,.0f} {self.currency_symbol}"
        self.kpi_balance_text.value = f"{current_balance:,.0f} {self.currency_symbol}"

        if current_balance < (self.start_balance * 0.1):
            self.kpi_balance_text.color = "#FF5252"
        else:
            self.kpi_balance_text.color = self.theme["text_main"]

        if not self.transactions:
            self.ml_insight_text.value = "Данных пока нет. Добавьте первую операцию!"
        else:
            cat_totals = {}
            for t in self.transactions:
                cat_totals[t["category"]] = cat_totals.get(t["category"], 0) + t["amount"]
            
            self.ml_insight_text.value = (
                "Пусто"
            )

        self.wallet_input.value = str(self.start_balance)

        query = self.search_query.lower()
        filtered_transactions = [
            t for t in self.transactions 
            if query in t["category"].lower() or query in t["comment"].lower()
        ]

        self.history_table.show_checkbox_column = self.is_edit_mode

        rows = []
        for t in filtered_transactions:
            rows.append(
                ft.DataRow(
                    selected=t["id"] in self.selected_ids,
                    on_select_changed=lambda e, t_id=t["id"]: self._on_row_select(e, t_id),
                    cells=[
                        ft.DataCell(ft.Text(t["date"])),
                        ft.DataCell(ft.Text(t["category"])),
                        ft.DataCell(ft.Text(t["comment"], italic=True, color=self.theme["text_sec"])),
                        ft.DataCell(ft.Text(f"{t['amount']:.0f}", weight=ft.FontWeight.BOLD)),
                    ]
                )
            )
        self.history_table.rows = rows
        
        recent_rows = []
        for t in self.transactions[:5]:
            recent_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(t["date"])),
                        ft.DataCell(ft.Text(t["category"])),
                        ft.DataCell(ft.Text(f"{t['amount']:.0f}")),
                    ]
                )
            )
        self.table_recent.rows = recent_rows
        
        idx = self.nav_rail.selected_index
        if idx is not None:
             self.content_area.content = self._get_view_by_index(idx)

        self.page.update()

    def _on_row_select(self, e, t_id):
        if t_id in self.selected_ids:
            self.selected_ids.discard(t_id)
        else:
            self.selected_ids.add(t_id)
        self._update_data_driven_ui()

    def on_search_change(self, e):
        self.search_query = e.control.value
        self._update_data_driven_ui()

    def toggle_edit_mode(self, e):
        self.is_edit_mode = not self.is_edit_mode
        if not self.is_edit_mode:
            self.selected_ids.clear()
        
        self.content_area.content = self.get_history_view() 
        self._update_data_driven_ui()

    def show_snackbar(self, message, color="green"):
        snack = ft.SnackBar(
            content=ft.Text(message, color="white"),
            bgcolor=color,
            duration=2000
        )
        self.page.open(snack)

    def show_custom_dialog(self, title, content, actions, icon_data, icon_color):
        t = self.theme
        dlg = ft.AlertDialog(
            modal=True,
            bgcolor=t["card_bg"],
            title_padding=20,
            content_padding=20,
            shape=ft.RoundedRectangleBorder(radius=20),
            title=ft.Row([
                ft.Icon(icon_data, color=icon_color, size=30),
                ft.Text(title, color=t["text_main"], weight=ft.FontWeight.BOLD)
            ], spacing=10),
            content=ft.Text(content, color=t["text_main"], size=16),
            actions=actions,
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.open(dlg)
        return dlg

    def show_alert(self, title, message, is_error=True):
        color = "#FF5252" if is_error else "#00FF99"
        icon = ft.Icons.ERROR_OUTLINE if is_error else ft.Icons.CHECK_CIRCLE_OUTLINE
        
        def close_action(e):
             self.page.close(dlg)
        
        dlg = self.show_custom_dialog(
            title=title, 
            content=message, 
            icon_data=icon, 
            icon_color=color,
            actions=[
                ft.TextButton("Понятно", on_click=close_action, style=ft.ButtonStyle(color=self.theme["text_main"]))
            ]
        )

    def open_balance_dialog(self, e):
        self.is_balance_editing = True
        self._update_data_driven_ui() 

        t = self.theme
        new_balance_input = ft.TextField(
            label="Новый баланс", 
            value=str(self.start_balance),
            suffix_text=self.currency_symbol,
            keyboard_type=ft.KeyboardType.NUMBER,
            border_radius=12,
            bgcolor=t["bg"],
            border_color=t["accent"],
            text_style=ft.TextStyle(color=t["text_main"])
        )

        def close_action(e):
            self.is_balance_editing = False
            self.page.close(dlg)
            self._update_data_driven_ui()

        def save_action(e):
            try:
                val = float(new_balance_input.value)
                self.start_balance = val
                self.show_snackbar("Баланс обновлен!", "green")
                self.is_balance_editing = False
                self.page.close(dlg)
                self._update_data_driven_ui()
            except ValueError:
                self.show_snackbar("Введите корректное число", "red")

        dlg = ft.AlertDialog(
            modal=True,
            bgcolor=t["card_bg"],
            title=ft.Text("Изменение баланса", color=t["text_main"]),
            content=ft.Container(height=80, content=new_balance_input),
            actions=[
                ft.TextButton("Отмена", on_click=close_action, style=ft.ButtonStyle(color=t["text_sec"])),
                ft.ElevatedButton("Сохранить", on_click=save_action, style=ft.ButtonStyle(bgcolor=t["accent"], color="white"))
            ]
        )
        self.page.open(dlg)

    def save_wallet_balance_handler(self, e):
        try:
            val = float(self.wallet_input.value)
            self.start_balance = val
            self._update_data_driven_ui()
            self.show_snackbar("Баланс кошелька успешно обновлен!")
        except ValueError:
            self.show_alert("Ошибка", "Пожалуйста, введите корректное число.", is_error=True)

    def show_delete_confirm(self):
        if not self.selected_ids:
            self.show_snackbar("Ничего не выбрано для удаления", "red")
            return
        
        def confirm_delete(e):
            self.transactions = [t for t in self.transactions if t["id"] not in self.selected_ids]
            count = len(self.selected_ids)
            self.selected_ids.clear()
            self.is_edit_mode = False
            self.page.close(dlg)
            self.content_area.content = self.get_history_view()
            self._update_data_driven_ui()
            self.show_snackbar(f"Удалено записей: {count}", "green")
            
        def cancel_delete(e):
            self.page.close(dlg)
            
        t = self.theme
        dlg = ft.AlertDialog(
            modal=True,
            bgcolor=t["card_bg"],
            title=ft.Row([
                ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color="#FFAB00", size=30),
                ft.Text("Подтверждение", color=t["text_main"], weight=ft.FontWeight.BOLD)
            ], spacing=10),
            content=ft.Text(f"Вы действительно хотите удалить {len(self.selected_ids)} записей?", color=t["text_main"], size=16),
            actions=[
                ft.TextButton("Отмена", on_click=cancel_delete, style=ft.ButtonStyle(color=t["text_sec"])),
                ft.ElevatedButton("Удалить", on_click=confirm_delete, style=ft.ButtonStyle(bgcolor="#FF5252", color="white", elevation=0)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.open(dlg)

    def export_to_csv(self, e):
        try:
            filename = DATA_FILE
            with open(filename, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Date", "Category", "Amount", "Comment"])
                for t in self.transactions:
                    writer.writerow([t["id"], t["date"], t["category"], t["amount"], t["comment"]])
            
            def close_export(e):
                self.page.close(dlg)
                
            dlg = ft.AlertDialog(
                modal=True,
                bgcolor=self.theme["card_bg"],
                title=ft.Row([ft.Icon(ft.Icons.FILE_DOWNLOAD_DONE, color=self.theme["accent"]), ft.Text("Экспорт", color=self.theme["text_main"])]),
                content=ft.Text(f"Сохранено в: {os.path.abspath(filename)}", color=self.theme["text_main"]),
                actions=[ft.TextButton("ОК", on_click=close_export)]
            )
            self.page.open(dlg)
        except Exception as ex:
            self.show_alert("Ошибка экспорта", str(ex), is_error=True)

    def apply_theme(self, theme_key):
        self.current_theme_key = theme_key
        self.theme = APP_THEMES[theme_key]
        self.page.bgcolor = self.theme["bg"]
        self.page.theme_mode = self.theme["mode"]
        self.kpi_expense_text.color = self.theme["text_main"]
        self.kpi_balance_text.color = self.theme["text_main"]
        self.nav_rail = self._build_nav_rail()
        self._style_components()
        current_idx = self.nav_rail.selected_index if self.nav_rail.selected_index else 0
        self.content_area.content = self._get_view_by_index(current_idx)
        self.page.clean()
        self.page.add(
            ft.Row(
                expand=True,
                spacing=0,
                controls=[
                    self.nav_rail,
                    ft.VerticalDivider(width=1, color=ft.Colors.with_opacity(0.1, self.theme["text_sec"])),
                    self.content_area
                ]
            )
        )
        self.page.update()

    def _style_components(self):
        t = self.theme
        for control in [self.amount_input, self.category_dropdown, self.comment_input, self.search_field, self.wallet_input]:
            control.bgcolor = t["card_bg"]
            control.border_color = ft.Colors.with_opacity(0.3, t["text_sec"])
            control.border_width = 1
            control.text_style = ft.TextStyle(color=t["text_main"])
            control.label_style = ft.TextStyle(color=t["text_sec"])
            control.cursor_color = t["accent"]
            if isinstance(control, ft.TextField):
                control.hint_style = ft.TextStyle(color=ft.Colors.with_opacity(0.5, t["text_sec"]))
        for table in [self.table_recent, self.history_table]:
            table.bgcolor = t["card_bg"]
            table.heading_row_color = ft.Colors.with_opacity(0.05, t["accent"])
            table.data_row_color = {ft.ControlState.HOVERED: ft.Colors.with_opacity(0.05, t["text_main"])}
            table.heading_text_style = ft.TextStyle(color=t["text_sec"], weight=ft.FontWeight.BOLD)
            table.data_text_style = ft.TextStyle(color=t["text_main"])
        self.ml_insight_text.color = t["accent"]

    def _header(self, title, subtitle=None):
        return ft.Column([
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text(title, size=32, weight=ft.FontWeight.BOLD, color=self.theme["text_main"]),
                    self._build_theme_switcher()
                ]
            ),
            ft.Text(subtitle, size=14, color=self.theme["text_sec"]) if subtitle else ft.Container()
        ], spacing=5)

    def _build_theme_switcher(self):
        return ft.PopupMenuButton(
            icon=ft.Icons.COLOR_LENS_OUTLINED,
            icon_color=self.theme["text_sec"],
            tooltip="Сменить тему",
            items=[
                ft.PopupMenuItem(text="Modern Dark", on_click=lambda _: self.apply_theme("dark_modern")),
                ft.PopupMenuItem(text="Clean Light", on_click=lambda _: self.apply_theme("light_clean")),
                ft.PopupMenuItem(text="Cyber Neon", on_click=lambda _: self.apply_theme("neon_cyber")),
                ft.PopupMenuItem(text="Sunset Glow", on_click=lambda _: self.apply_theme("sunset_glow")),
                ft.PopupMenuItem(text="Ocean Breeze", on_click=lambda _: self.apply_theme("ocean_breeze")),
            ]
        )

    def _kpi_card(self, title, text_control, icon, trend=None, on_click=None):
        t = self.theme
        return ft.Container(
            width=240, height=140,
            border_radius=20,
            padding=25,
            gradient=t.get("gradient") if trend == "gradient_bg" else None,
            bgcolor=t["card_bg"] if trend != "gradient_bg" else None,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=15, color=ft.Colors.with_opacity(0.08, "#000000")),
            ink=True if on_click else False,
            on_click=on_click,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Container(
                                content=ft.Icon(icon, color=t["text_main"] if trend == "gradient_bg" else t["accent"]),
                                bgcolor=ft.Colors.with_opacity(0.2, "#ffffff") if trend == "gradient_bg" else ft.Colors.with_opacity(0.1, t["accent"]),
                                padding=10, border_radius=10
                            ),
                            ft.Text(trend, color="#00FF99" if trend and "+" in trend else "#FF5252", size=12, weight=ft.FontWeight.BOLD) if trend and trend != "gradient_bg" else ft.Container()
                        ]
                    ),
                    ft.Column([
                          ft.Text(title, color=ft.Colors.with_opacity(0.8, t["text_main"]), size=12),
                          text_control,
                    ], spacing=2)
                ]
            )
        )

    def get_dashboard_view(self):
        t = self.theme
        if self.is_balance_editing:
            expense_style = None 
            balance_style = "gradient_bg" 
        else:
            expense_style = "gradient_bg" 
            balance_style = "+2.4%" 

        return ft.Column(
            scroll=ft.ScrollMode.HIDDEN,
            controls=[
                self._header("Дашборд", f"Добро пожаловать. Ваши финансы под контролем."),
                ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                ft.Row(
                    wrap=True,
                    controls=[
                        self._kpi_card("Расходы (Всего)", self.kpi_expense_text, ft.Icons.WALLET, trend=expense_style),
                        self._kpi_card("Текущий баланс", self.kpi_balance_text, ft.Icons.ACCOUNT_BALANCE, trend=balance_style, on_click=self.open_balance_dialog),
                        self._kpi_card("ML Прогноз", ft.Text("Low Risk", size=26, weight=ft.FontWeight.BOLD, color=t["text_main"]), ft.Icons.TIMELINE, "Stable"),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                ft.Container(
                    bgcolor=t["card_bg"],
                    padding=25, border_radius=20,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.with_opacity(0.05, "#000000")),
                    content=ft.Column([
                        ft.Text("Динамика расходов", size=18, weight=ft.FontWeight.BOLD, color=t["text_main"]),
                        ft.Divider(color=ft.Colors.TRANSPARENT, height=10),
                        self.chart_dashboard
                    ])
                ),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                ft.Text("Последние транзакции", size=18, weight=ft.FontWeight.BOLD, color=t["text_main"]),
                ft.Container(
                    bgcolor=t["card_bg"], border_radius=20, padding=10,
                    content=self.table_recent
                )
            ]
        )

    def get_input_view(self):
        t = self.theme
        return ft.Container(
            alignment=ft.alignment.center,
            content=ft.Container(
                width=500,
                padding=40,
                bgcolor=t["card_bg"],
                border_radius=25,
                shadow=ft.BoxShadow(spread_radius=1, blur_radius=20, color=ft.Colors.with_opacity(0.1, "#000000")),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text("Новая операция", size=24, weight=ft.FontWeight.BOLD, color=t["text_main"]),
                        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                        self.amount_input,
                        ft.Container(height=10),
                        self.category_dropdown,
                        ft.Container(height=10),
                        self.comment_input,
                        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                        ft.Container(
                            width=300,
                            height=50,
                            border_radius=12,
                            gradient=t["gradient"],
                            content=ft.ElevatedButton(
                                "Сохранить запись",
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.TRANSPARENT,
                                    shadow_color=ft.Colors.TRANSPARENT,
                                    overlay_color=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                                    shape=ft.RoundedRectangleBorder(radius=12)
                                ),
                                width=300, height=50,
                                on_click=self.save_transaction_handler
                            )
                        )
                    ]
                )
            )
        )

    def get_wallet_view(self):
        t = self.theme
        return ft.Container(
            alignment=ft.alignment.center,
            content=ft.Column([
                self._header("Кошелек", "Управление основным счетом"),
                ft.Divider(height=40, color=ft.Colors.TRANSPARENT),
                ft.Container(
                    width=500,
                    padding=40,
                    bgcolor=t["card_bg"],
                    border_radius=25,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=20, color=ft.Colors.with_opacity(0.1, "#000000")),
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET_ROUNDED, size=60, color=t["accent"]),
                            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                            ft.Text("Начальный баланс", size=20, weight=ft.FontWeight.BOLD, color=t["text_main"]),
                            ft.Text("Измените стартовую сумму вашего бюджета", size=14, color=t["text_sec"]),
                            ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                            self.wallet_input,
                            ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                            ft.Container(
                                width=300,
                                height=50,
                                border_radius=12,
                                gradient=t["gradient"],
                                content=ft.ElevatedButton(
                                    "Обновить баланс",
                                    style=ft.ButtonStyle(
                                        color=ft.Colors.WHITE,
                                        bgcolor=ft.Colors.TRANSPARENT,
                                        shadow_color=ft.Colors.TRANSPARENT,
                                        shape=ft.RoundedRectangleBorder(radius=12)
                                    ),
                                    width=300, height=50,
                                    on_click=self.save_wallet_balance_handler
                                )
                            )
                        ]
                    )
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

    def get_analytics_view(self):
        t = self.theme
        return ft.Column(
            scroll=ft.ScrollMode.AUTO,
            controls=[
                self._header("AI Аналитика", "Инсайты от вашей ML модели"),
                ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                ft.Container(
                    bgcolor=ft.Colors.with_opacity(0.1, t["accent"]),
                    border=ft.border.all(1, t["accent"]),
                    border_radius=15, padding=20,
                    content=ft.Row([
                        ft.Icon(ft.Icons.AUTO_AWESOME, color=t["accent"], size=30),
                        ft.VerticalDivider(width=20, color=ft.Colors.TRANSPARENT),
                        ft.Column([
                            ft.Text("Ключевой инсайт", size=12, color=t["text_sec"], weight=ft.FontWeight.BOLD),
                            self.ml_insight_text
                        ])
                    ])
                ),
                ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                ft.Container(
                    bgcolor=t["card_bg"], padding=30, border_radius=20,
                    content=ft.Column([
                        ft.Text("Карта расходов (Heatmap)", size=18, weight=ft.FontWeight.BOLD, color=t["text_main"]),
                        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                        self.chart_analytics
                    ])
                )
            ]
        )

    def get_history_view(self):
        t = self.theme
        if self.is_edit_mode:
            action_bar = ft.Row([
                ft.Text(f"Выбрано: {len(self.selected_ids)}", color=t["text_main"], weight=ft.FontWeight.BOLD),
                ft.Row([
                    ft.TextButton("Отмена", on_click=self.toggle_edit_mode, style=ft.ButtonStyle(color=t["text_sec"])),
                    ft.ElevatedButton(
                        "Удалить", 
                        icon=ft.Icons.DELETE_OUTLINE, 
                        color="white", 
                        bgcolor="#FF5252",
                        on_click=lambda _: self.show_delete_confirm()
                    )
                ])
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        else:
            action_bar = ft.Row([
                ft.Container(width=300, content=self.search_field),
                ft.Row([
                    ft.IconButton(ft.Icons.FILE_DOWNLOAD_OUTLINED, icon_color=t["text_sec"], tooltip="Экспорт CSV", on_click=self.export_to_csv),
                    ft.OutlinedButton(
                        "Выбрать", 
                        icon=ft.Icons.CHECK_BOX_OUTLINED,
                        style=ft.ButtonStyle(color=t["accent"], side=ft.BorderSide(1, t["accent"])),
                        on_click=self.toggle_edit_mode
                    )
                ])
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        return ft.Column(
            expand=True,
            controls=[
                self._header("История", "Управление записями"),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                ft.Container(bgcolor=t["card_bg"], padding=15, border_radius=15, content=action_bar),
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                ft.Container(
                    bgcolor=t["card_bg"], border_radius=20, padding=20, expand=True,
                    content=ft.Column(scroll=ft.ScrollMode.AUTO, controls=[self.history_table])
                )
            ]
        )

    def get_settings_view(self):
        t = self.theme
        txt = TRANSLATIONS[self.current_lang]
        
        def setting_card(icon, title, control):
            return ft.Container(
                bgcolor=t["card_bg"], padding=20, border_radius=15,
                content=ft.Row([
                    ft.Row([
                        ft.Container(
                            padding=10, bgcolor=ft.Colors.with_opacity(0.1, t["accent"]), 
                            border_radius=10, content=ft.Icon(icon, color=t["accent"])
                        ),
                        ft.Text(title, color=t["text_main"], size=16, weight=ft.FontWeight.W_500)
                    ], spacing=15),
                    control
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            )

        lang_dropdown = ft.Dropdown(
            width=120, value=self.current_lang, border_radius=10, content_padding=10,
            text_style=ft.TextStyle(color=t["text_main"]),
            border_color=t["accent"],
            options=[ft.dropdown.Option("ru", "Русский"), ft.dropdown.Option("en", "English")],
            on_change=self.change_language
        )
        
        currency_dropdown = ft.Dropdown(
            width=120, value=self.currency_symbol, border_radius=10, content_padding=10,
            text_style=ft.TextStyle(color=t["text_main"]),
            border_color=t["accent"],
            options=[
                ft.dropdown.Option("RUB", "₽ (RUB)"), 
                ft.dropdown.Option("USD", "$ (USD)"), 
                ft.dropdown.Option("EUR", "€ (EUR)"),
                ft.dropdown.Option("KZT", "₸ (KZT)")
            ],
            on_change=self.change_currency
        )
        
        theme_dropdown = ft.Dropdown(
            width=150, value=self.current_theme_key, border_radius=10, content_padding=10,
            text_style=ft.TextStyle(color=t["text_main"]),
            border_color=t["accent"],
            options=[
                ft.dropdown.Option("dark_modern", "Dark Modern"),
                ft.dropdown.Option("light_clean", "Light Clean"),
                ft.dropdown.Option("neon_cyber", "Neon Cyber"),
                ft.dropdown.Option("sunset_glow", "Sunset Glow"),
                ft.dropdown.Option("ocean_breeze", "Ocean Breeze"),
            ],
            on_change=lambda e: self.apply_theme(e.control.value)
        )

        resize_switch = ft.Switch(
            value=self.page.window.resizable, 
            active_color=t["accent"],
            on_change=self.toggle_resizable
        )

        size_dropdown = ft.Dropdown(
            width=150, value=f"{int(self.page.window.width)}x{int(self.page.window.height)}",
            border_radius=10, content_padding=10,
            text_style=ft.TextStyle(color=t["text_main"]), border_color=t["accent"],
            options=[
                ft.dropdown.Option("1100x700", "Стандарт"),
                ft.dropdown.Option("1280x720", "HD"),
                ft.dropdown.Option("1920x1080", "Full HD"),
            ],
            on_change=self.resize_window_handler
        )

        return ft.Column(
            scroll=ft.ScrollMode.AUTO,
            controls=[
                self._header(txt["settings_title"], "Персонализация и система"),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                
                ft.Text("Общие", color=t["text_sec"], weight=ft.FontWeight.BOLD),
                setting_card(ft.Icons.LANGUAGE, txt["lang_label"], lang_dropdown),
                ft.Container(height=5),
                setting_card(ft.Icons.MONETIZATION_ON_OUTLINED, txt["curr_label"], currency_dropdown),
                ft.Container(height=5),
                setting_card(ft.Icons.COLOR_LENS_OUTLINED, txt["theme_label"], theme_dropdown),

                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                ft.Text("Окно приложения", color=t["text_sec"], weight=ft.FontWeight.BOLD),
                setting_card(ft.Icons.ASPECT_RATIO, txt["win_size"], size_dropdown),
                ft.Container(height=5),
                setting_card(ft.Icons.OPEN_IN_FULL, txt["win_resize"], resize_switch),

                ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                
                ft.Container(
                    width=float("inf"), height=60, border_radius=15,
                    gradient=t["gradient"],
                    ink=True,
                    on_click=lambda _: self.show_credits(),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Icon(ft.Icons.INFO_OUTLINE, color="white"),
                            ft.Text(txt["credits"], color="white", weight=ft.FontWeight.BOLD, size=18)
                        ]
                    )
                )
            ]
        )

    def change_language(self, e):
        self.current_lang = e.control.value
        self.nav_rail = self._build_nav_rail()
        self.content_area.content = self.get_settings_view()
        self.page.update()
        self.show_snackbar(f"Язык изменен на {e.control.value}")

    def change_currency(self, e):
        self.currency_symbol = e.control.value
        self.amount_input.suffix_text = self.currency_symbol
        self.wallet_input.suffix_text = self.currency_symbol
        self._update_data_driven_ui()
        self.show_snackbar("Валюта обновлена!")

    def toggle_resizable(self, e):
        self.page.window.resizable = e.control.value
        self.page.update()

    def resize_window_handler(self, e):
        w, h = map(int, e.control.value.split("x"))
        self.page.window.width = w
        self.page.window.height = h
        self.page.update()

    def show_credits(self):
        t = self.theme
        
        def open_url(url):
            self.page.launch_url(url)

        def link_button(icon, text, url, color):
            return ft.Container(
                bgcolor=ft.Colors.with_opacity(0.1, color),
                padding=10, border_radius=10,
                ink=True, on_click=lambda _: open_url(url),
                content=ft.Row([
                    ft.Icon(icon, color=color),
                    ft.Text(text, color=t["text_main"], weight=ft.FontWeight.BOLD)
                ], alignment=ft.MainAxisAlignment.CENTER)
            )

        content = ft.Column(
            tight=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=80, height=80, border_radius=40,
                    gradient=t["gradient"],
                    content=ft.Icon(ft.Icons.CODE, color="white", size=40),
                    alignment=ft.alignment.center
                ),
                ft.Text("DataMoney AI", size=24, weight=ft.FontWeight.BOLD, color=t["text_main"]),
                ft.Text("v 2.0.0 Ultimate Edition", color=t["text_sec"]),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                
                link_button(ft.Icons.TELEGRAM, "Мой Telegram", "https://t.me/Yeeapy", "#0088cc"),
                ft.Container(height=5),
                link_button(ft.Icons.TELEGRAM, "Telegram Канал", "https://t.me/PenDest", "#0088cc"),
                ft.Container(height=5),
                link_button(ft.Icons.CODE_OFF, "GitHub Репозиторий", "https://github.com/YOUR_REPO", "#333333" if t["mode"]==ft.ThemeMode.LIGHT else "#ffffff"),
                
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                ft.Text("Created with ❤️ using Flet & Python", size=10, color=t["text_sec"])
            ]
        )

        dlg = ft.AlertDialog(
            modal=True,
            bgcolor=t["card_bg"],
            content=content,
            actions=[
                ft.TextButton("Закрыть", on_click=lambda e: self.page.close(dlg))
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER
        )
        self.page.open(dlg)

    def save_transaction_handler(self, e):
        if not self.amount_input.value or not self.category_dropdown.value:
            self.show_alert("Внимание", "Пожалуйста, заполните поле суммы и выберите категорию.", is_error=True)
            return
        try:
            amount_val = float(self.amount_input.value)
        except ValueError:
            self.show_alert("Ошибка ввода", "Сумма должна быть числом", is_error=True)
            return
        self.last_id += 1
        new_trans = {
            "id": self.last_id,
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "category": self.category_dropdown.value,
            "amount": amount_val,
            "comment": self.comment_input.value if self.comment_input.value else "-"
        }
        self.transactions.insert(0, new_trans)
        self._update_data_driven_ui()
        self.show_snackbar(f"Транзакция на {amount_val} добавлена!")
        self.amount_input.value = ""
        self.comment_input.value = ""
        
        self.nav_rail.selected_index = 0
        self.page.update()

    def sort_history(self, col_idx, ascending):
        self.history_table.sort_column_index = col_idx
        self.history_table.sort_ascending = ascending
        mapping = {0: "date", 1: "category", 3: "amount"}
        if col_idx in mapping:
            key = mapping[col_idx]
            self.transactions.sort(key=lambda x: float(x[key]) if key == "amount" else x[key], reverse=not ascending)
            self._update_data_driven_ui()

    def navigate(self, e):
        idx = e.control.selected_index
        self.content_area.content = self._get_view_by_index(idx)
        self.page.update()

    def _get_view_by_index(self, idx):
        if idx == 0: return self.get_dashboard_view()
        elif idx == 1: return self.get_input_view()
        elif idx == 2: return self.get_analytics_view()
        elif idx == 3: return self.get_history_view()
        elif idx == 4: return self.get_wallet_view()
        elif idx == 5: return self.get_settings_view()
        return self.get_dashboard_view()

def main(page: ft.Page):
    app = DataMoneyApp(page)