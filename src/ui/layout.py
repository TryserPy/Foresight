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
        "nav_wallet": "Кошелек", "nav_settings": "Настройки", "nav_stats": "Статистика",
        "settings_title": "Настройки", "lang_label": "Язык", "curr_label": "Валюта",
        "win_size": "Размер окна", "win_resize": "Растягивание окна",
        "credits": "Об авторе", "theme_label": "Тема оформления",
        "dash_title": "Дашборд", "dash_sub": "Добро пожаловать. Ваши финансы под контролем.",
        "kpi_expense": "Расходы (Всего)", "kpi_balance": "Текущий баланс", "kpi_ml": "ML Прогноз",
        "chart_title": "Динамика расходов", "recent_trans": "Последние транзакции",
        "input_title": "Новая операция", "amount_label": "Сумма", "cat_label": "Категория",
        "comment_label": "Комментарий", "save_btn": "Сохранить запись",
        "wallet_title": "Кошелек", "wallet_sub": "Управление основным счетом",
        "wallet_start": "Начальный баланс", "wallet_desc": "Измените стартовую сумму вашего бюджета",
        "wallet_update": "Обновить баланс",
        "ai_title": "AI Аналитика", "ai_sub": "Инсайты от вашей ML модели",
        "ai_insight": "Ключевой инсайт", "ai_heatmap": "Карта расходов (Heatmap)",
        "hist_title": "История", "hist_sub": "Управление записями",
        "search_hint": "Поиск...", "col_date": "Дата", "col_cat": "Категория", "col_sum": "Сумма",
        "col_com": "Комментарий", "btn_select": "Выбрать", "btn_cancel": "Отмена", "btn_delete": "Удалить",
        "sel_count": "Выбрано:", "set_gen": "Общие", "set_win": "Окно приложения",
        "err_title": "Ошибка", "err_num": "Введите корректное число", "snack_saved": "Сохранено!",
        "snack_del": "Удалено записей:", "confirm_title": "Подтверждение", 
        "confirm_text": "Вы действительно хотите удалить выбранные записи?",
        "export_title": "Экспорт", "export_saved": "Сохранено в:", "empty_data": "Данных пока нет.",
        "stats_title": "Анализ финансов", "stats_sub": "Визуализация ваших расходов и привычек",
        "stat_avg_check": "Средний чек", "stat_max_pay": "Макс. трата", "stat_top_cat": "Топ категория",
        "chart_weekly": "Активность по дням недели", "chart_structure": "Структура расходов",
        "stat_budget_health": "Здоровье бюджета", "stat_safe_zone": "Безопасная зона"
    },
    "en": {
        "nav_dashboard": "Dashboard", "nav_input": "Input", "nav_ai": "AI Insight", "nav_history": "History", 
        "nav_wallet": "Wallet", "nav_settings": "Settings", "nav_stats": "Statistics",
        "settings_title": "Settings", "lang_label": "Language", "curr_label": "Currency",
        "win_size": "Window Size", "win_resize": "Resizable Window",
        "credits": "Credits", "theme_label": "App Theme",
        "dash_title": "Dashboard", "dash_sub": "Welcome back. Your finances are under control.",
        "kpi_expense": "Expenses (Total)", "kpi_balance": "Current Balance", "kpi_ml": "ML Forecast",
        "chart_title": "Expense Dynamics", "recent_trans": "Recent Transactions",
        "input_title": "New Operation", "amount_label": "Amount", "cat_label": "Category",
        "comment_label": "Comment", "save_btn": "Save Record",
        "wallet_title": "Wallet", "wallet_sub": "Main account management",
        "wallet_start": "Initial Balance", "wallet_desc": "Modify your budget starting amount",
        "wallet_update": "Update Balance",
        "ai_title": "AI Analytics", "ai_sub": "Insights from your ML model",
        "ai_insight": "Key Insight", "ai_heatmap": "Expense Heatmap",
        "hist_title": "History", "hist_sub": "Manage your records",
        "search_hint": "Search...", "col_date": "Date", "col_cat": "Category", "col_sum": "Amount",
        "col_com": "Comment", "btn_select": "Select", "btn_cancel": "Cancel", "btn_delete": "Delete",
        "sel_count": "Selected:", "set_gen": "General", "set_win": "Application Window",
        "err_title": "Error", "err_num": "Please enter a valid number", "snack_saved": "Saved!",
        "snack_del": "Records deleted:", "confirm_title": "Confirmation",
        "confirm_text": "Do you really want to delete selected records?",
        "export_title": "Export", "export_saved": "Saved to:", "empty_data": "No data yet.",
        "stats_title": "Financial Analysis", "stats_sub": "Visualization of your expenses and habits",
        "stat_avg_check": "Average Check", "stat_max_pay": "Max Purchase", "stat_top_cat": "Top Category",
        "chart_weekly": "Weekly Activity", "chart_structure": "Expense Structure",
        "stat_budget_health": "Budget Health", "stat_safe_zone": "Safe Zone"
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

    def tr(self, key):
        return TRANSLATIONS.get(self.current_lang, TRANSLATIONS["en"]).get(key, key)

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
            label=self.tr("amount_label"), suffix_text=self.currency_symbol, 
            keyboard_type=ft.KeyboardType.NUMBER, border_radius=12,
            input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9.]", replacement_string="")
        )
        self.category_dropdown = ft.Dropdown(
            label=self.tr("cat_label"), border_radius=12,
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
            label=self.tr("comment_label"), multiline=True, max_lines=3, border_radius=12
        )

        self.wallet_input = ft.TextField(
            label=self.tr("wallet_start"), suffix_text=self.currency_symbol,
            keyboard_type=ft.KeyboardType.NUMBER, border_radius=12,
            input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9.]", replacement_string="")
        )

        self.table_recent = ft.DataTable(
            width=float("inf"), border_radius=10, column_spacing=20,
            columns=[
                ft.DataColumn(ft.Text(self.tr("col_date"))),
                ft.DataColumn(ft.Text(self.tr("col_cat"))),
                ft.DataColumn(ft.Text(self.tr("col_sum")), numeric=True),
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
                ft.DataColumn(ft.Text(self.tr("col_date")), on_sort=lambda e: self.sort_history(0, e.ascending)),
                ft.DataColumn(ft.Text(self.tr("col_cat")), on_sort=lambda e: self.sort_history(1, e.ascending)),
                ft.DataColumn(ft.Text(self.tr("col_com"))),
                ft.DataColumn(ft.Text(self.tr("col_sum")), numeric=True, on_sort=lambda e: self.sort_history(3, e.ascending)),
            ],
            rows=[]
        )
        
        self.search_field = ft.TextField(
            hint_text=self.tr("search_hint"), 
            prefix_icon=ft.Icons.SEARCH,
            border_radius=15,
            height=40,
            content_padding=10,
            text_size=14,
            on_change=self.on_search_change
        )
        
        self.ml_insight_text = ft.Text("...", size=15)

    def _build_nav_rail(self):
        t = self.theme
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
                ft.NavigationRailDestination(icon=ft.Icons.DASHBOARD_OUTLINED, selected_icon=ft.Icons.DASHBOARD, label=self.tr("nav_dashboard")),
                ft.NavigationRailDestination(icon=ft.Icons.ADD_CIRCLE_OUTLINE, selected_icon=ft.Icons.ADD_CIRCLE, label=self.tr("nav_input")),
                ft.NavigationRailDestination(icon=ft.Icons.INSIGHTS_OUTLINED, selected_icon=ft.Icons.INSIGHTS, label=self.tr("nav_ai")),
                ft.NavigationRailDestination(icon=ft.Icons.BAR_CHART_OUTLINED, selected_icon=ft.Icons.BAR_CHART, label=self.tr("nav_stats")),
                ft.NavigationRailDestination(icon=ft.Icons.HISTORY_OUTLINED, selected_icon=ft.Icons.HISTORY, label=self.tr("nav_history")),
                ft.NavigationRailDestination(icon=ft.Icons.ACCOUNT_BALANCE_WALLET_OUTLINED, selected_icon=ft.Icons.ACCOUNT_BALANCE_WALLET, label=self.tr("nav_wallet")),
                ft.NavigationRailDestination(icon=ft.Icons.SETTINGS_OUTLINED, selected_icon=ft.Icons.SETTINGS, label=self.tr("nav_settings")),
            ],
            on_change=self.navigate
        )

    def _update_components_text(self):
        self.amount_input.label = self.tr("amount_label")
        self.category_dropdown.label = self.tr("cat_label")
        self.comment_input.label = self.tr("comment_label")
        self.wallet_input.label = self.tr("wallet_start")
        self.search_field.hint_text = self.tr("search_hint")
        
        self.table_recent.columns[0].label.value = self.tr("col_date")
        self.table_recent.columns[1].label.value = self.tr("col_cat")
        self.table_recent.columns[2].label.value = self.tr("col_sum")
        
        self.history_table.columns[0].label.value = self.tr("col_date")
        self.history_table.columns[1].label.value = self.tr("col_cat")
        self.history_table.columns[2].label.value = self.tr("col_com")
        self.history_table.columns[3].label.value = self.tr("col_sum")

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
            self.ml_insight_text.value = self.tr("empty_data")
        else:
            self.ml_insight_text.value = "Stable"

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
        
        idx = self.nav_rail.selected_index if self.nav_rail.selected_index is not None else 0
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
                ft.TextButton("OK", on_click=close_action, style=ft.ButtonStyle(color=self.theme["text_main"]))
            ]
        )

    def open_balance_dialog(self, e):
        self.is_balance_editing = True
        self._update_data_driven_ui() 

        t = self.theme
        new_balance_input = ft.TextField(
            label=self.tr("wallet_start"), 
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
                self.show_snackbar(self.tr("snack_saved"), "green")
                self.is_balance_editing = False
                self.page.close(dlg)
                self._update_data_driven_ui()
            except ValueError:
                self.show_snackbar(self.tr("err_num"), "red")

        dlg = ft.AlertDialog(
            modal=True,
            bgcolor=t["card_bg"],
            title=ft.Text(self.tr("wallet_start"), color=t["text_main"]),
            content=ft.Container(height=80, content=new_balance_input),
            actions=[
                ft.TextButton(self.tr("btn_cancel"), on_click=close_action, style=ft.ButtonStyle(color=t["text_sec"])),
                ft.ElevatedButton(self.tr("save_btn"), on_click=save_action, style=ft.ButtonStyle(bgcolor=t["accent"], color="white"))
            ]
        )
        self.page.open(dlg)

    def save_wallet_balance_handler(self, e):
        try:
            val = float(self.wallet_input.value)
            self.start_balance = val
            self._update_data_driven_ui()
            self.show_snackbar(self.tr("snack_saved"))
        except ValueError:
            self.show_alert(self.tr("err_title"), self.tr("err_num"), is_error=True)

    def show_delete_confirm(self):
        if not self.selected_ids:
            return
        
        def confirm_delete(e):
            self.transactions = [t for t in self.transactions if t["id"] not in self.selected_ids]
            count = len(self.selected_ids)
            self.selected_ids.clear()
            self.is_edit_mode = False
            self.page.close(dlg)
            self.content_area.content = self.get_history_view()
            self._update_data_driven_ui()
            self.show_snackbar(f"{self.tr('snack_del')} {count}", "green")
            
        def cancel_delete(e):
            self.page.close(dlg)
            
        t = self.theme
        dlg = ft.AlertDialog(
            modal=True,
            bgcolor=t["card_bg"],
            title=ft.Row([
                ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color="#FFAB00", size=30),
                ft.Text(self.tr("confirm_title"), color=t["text_main"], weight=ft.FontWeight.BOLD)
            ], spacing=10),
            content=ft.Text(self.tr("confirm_text"), color=t["text_main"], size=16),
            actions=[
                ft.TextButton(self.tr("btn_cancel"), on_click=cancel_delete, style=ft.ButtonStyle(color=t["text_sec"])),
                ft.ElevatedButton(self.tr("btn_delete"), on_click=confirm_delete, style=ft.ButtonStyle(bgcolor="#FF5252", color="white", elevation=0)),
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
                title=ft.Row([ft.Icon(ft.Icons.FILE_DOWNLOAD_DONE, color=self.theme["accent"]), ft.Text(self.tr("export_title"), color=self.theme["text_main"])]),
                content=ft.Text(f"{self.tr('export_saved')} {os.path.abspath(filename)}", color=self.theme["text_main"]),
                actions=[ft.TextButton("ОК", on_click=close_export)]
            )
            self.page.open(dlg)
        except Exception as ex:
            self.show_alert(self.tr("err_title"), str(ex), is_error=True)

    def apply_theme(self, theme_key):
        self.current_theme_key = theme_key
        self.theme = APP_THEMES[theme_key]
        self.page.bgcolor = self.theme["bg"]
        self.page.theme_mode = self.theme["mode"]
        self.kpi_expense_text.color = self.theme["text_main"]
        self.kpi_balance_text.color = self.theme["text_main"]
        self.nav_rail = self._build_nav_rail()
        self._style_components()
        current_idx = self.nav_rail.selected_index if self.nav_rail.selected_index is not None else 0
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
            tooltip=self.tr("theme_label"),
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
                self._header(self.tr("dash_title"), self.tr("dash_sub")),
                ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                ft.Row(
                    wrap=True,
                    controls=[
                        self._kpi_card(self.tr("kpi_expense"), self.kpi_expense_text, ft.Icons.WALLET, trend=expense_style),
                        self._kpi_card(self.tr("kpi_balance"), self.kpi_balance_text, ft.Icons.ACCOUNT_BALANCE, trend=balance_style, on_click=self.open_balance_dialog),
                        self._kpi_card(self.tr("kpi_ml"), ft.Text("Low Risk", size=26, weight=ft.FontWeight.BOLD, color=t["text_main"]), ft.Icons.TIMELINE, "Stable"),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                ft.Container(
                    bgcolor=t["card_bg"],
                    padding=25, border_radius=20,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.with_opacity(0.05, "#000000")),
                    content=ft.Column([
                        ft.Text(self.tr("chart_title"), size=18, weight=ft.FontWeight.BOLD, color=t["text_main"]),
                        ft.Divider(color=ft.Colors.TRANSPARENT, height=10),
                        self.chart_dashboard
                    ])
                ),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                ft.Text(self.tr("recent_trans"), size=18, weight=ft.FontWeight.BOLD, color=t["text_main"]),
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
                        ft.Text(self.tr("input_title"), size=24, weight=ft.FontWeight.BOLD, color=t["text_main"]),
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
                                self.tr("save_btn"),
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
                self._header(self.tr("wallet_title"), self.tr("wallet_sub")),
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
                            ft.Text(self.tr("wallet_start"), size=20, weight=ft.FontWeight.BOLD, color=t["text_main"]),
                            ft.Text(self.tr("wallet_desc"), size=14, color=t["text_sec"]),
                            ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                            self.wallet_input,
                            ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                            ft.Container(
                                width=300,
                                height=50,
                                border_radius=12,
                                gradient=t["gradient"],
                                content=ft.ElevatedButton(
                                    self.tr("wallet_update"),
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
                self._header(self.tr("ai_title"), self.tr("ai_sub")),
                ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                ft.Container(
                    bgcolor=ft.Colors.with_opacity(0.1, t["accent"]),
                    border=ft.border.all(1, t["accent"]),
                    border_radius=15, padding=20,
                    content=ft.Row([
                        ft.Icon(ft.Icons.AUTO_AWESOME, color=t["accent"], size=30),
                        ft.VerticalDivider(width=20, color=ft.Colors.TRANSPARENT),
                        ft.Column([
                            ft.Text(self.tr("ai_insight"), size=12, color=t["text_sec"], weight=ft.FontWeight.BOLD),
                            self.ml_insight_text
                        ])
                    ])
                ),
                ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                ft.Container(
                    bgcolor=t["card_bg"], padding=30, border_radius=20,
                    content=ft.Column([
                        ft.Text(self.tr("ai_heatmap"), size=18, weight=ft.FontWeight.BOLD, color=t["text_main"]),
                        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                        self.chart_analytics
                    ])
                )
            ]
        )

    def get_statistics_view(self):
        t = self.theme
        
        def stat_mini_card(title, value, icon, color_idx=0):
            colors = [t["accent"], "#FFAB00", "#FF5252", "#00E5FF"]
            icon_color = colors[color_idx % len(colors)]
            
            return ft.Container(
                bgcolor=t["card_bg"],
                padding=20,
                border_radius=20,
                expand=True, 
                content=ft.Row([
                    ft.Container(
                        padding=12, 
                        bgcolor=ft.Colors.with_opacity(0.1, icon_color),
                        border_radius=12,
                        content=ft.Icon(icon, color=icon_color, size=24)
                    ),
                    ft.Column([
                        ft.Text(title, color=t["text_sec"], size=12),
                        ft.Text(value, color=t["text_main"], size=18, weight=ft.FontWeight.BOLD)
                    ], spacing=2)
                ])
            )

        chart_data = [
            ft.BarChartGroup(x=0, bar_rods=[ft.BarChartRod(from_y=0, to_y=4000, width=20, color=t["accent"], border_radius=5)]),
            ft.BarChartGroup(x=1, bar_rods=[ft.BarChartRod(from_y=0, to_y=2000, width=20, color="#FF5252", border_radius=5)]),
            ft.BarChartGroup(x=2, bar_rods=[ft.BarChartRod(from_y=0, to_y=5500, width=20, color=t["accent"], border_radius=5)]),
            ft.BarChartGroup(x=3, bar_rods=[ft.BarChartRod(from_y=0, to_y=1000, width=20, color=t["text_sec"], border_radius=5)]),
            ft.BarChartGroup(x=4, bar_rods=[ft.BarChartRod(from_y=0, to_y=8000, width=20, color="#00FF99", border_radius=5)]),
            ft.BarChartGroup(x=5, bar_rods=[ft.BarChartRod(from_y=0, to_y=3500, width=20, color=t["accent"], border_radius=5)]),
            ft.BarChartGroup(x=6, bar_rods=[ft.BarChartRod(from_y=0, to_y=6000, width=20, color=t["accent"], border_radius=5)]),
        ]

        bar_chart = ft.BarChart(
            bar_groups=chart_data,
            border=ft.border.only(bottom=ft.BorderSide(1, t["text_sec"])),
            left_axis=ft.ChartAxis(labels_size=40, title=ft.Text("RUB", color=t["text_sec"], size=10), title_size=20),
            bottom_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(value=0, label=ft.Text("Пн", color=t["text_sec"], size=10)),
                    ft.ChartAxisLabel(value=1, label=ft.Text("Вт", color=t["text_sec"], size=10)),
                    ft.ChartAxisLabel(value=2, label=ft.Text("Ср", color=t["text_sec"], size=10)),
                    ft.ChartAxisLabel(value=3, label=ft.Text("Чт", color=t["text_sec"], size=10)),
                    ft.ChartAxisLabel(value=4, label=ft.Text("Пт", color=t["text_sec"], size=10)),
                    ft.ChartAxisLabel(value=5, label=ft.Text("Сб", color=t["text_sec"], size=10)),
                    ft.ChartAxisLabel(value=6, label=ft.Text("Вс", color=t["text_sec"], size=10)),
                ]
            ),
            horizontal_grid_lines=ft.ChartGridLines(color=ft.Colors.with_opacity(0.1, t["text_sec"]), width=1),
            tooltip_bgcolor=t["card_bg"],
            max_y=10000,
        )

        pie_chart = ft.PieChart(
            sections=[
                ft.PieChartSection(40, color=t["accent"], radius=30, title="40%", title_style=ft.TextStyle(size=12, color="white", weight=ft.FontWeight.BOLD)),
                ft.PieChartSection(30, color="#FFAB00", radius=30, title="30%", title_style=ft.TextStyle(size=12, color="white", weight=ft.FontWeight.BOLD)),
                ft.PieChartSection(15, color="#FF5252", radius=30, title="15%", title_style=ft.TextStyle(size=12, color="white", weight=ft.FontWeight.BOLD)),
                ft.PieChartSection(15, color="#00BCD4", radius=30, title="15%", title_style=ft.TextStyle(size=12, color="white", weight=ft.FontWeight.BOLD)),
            ],
            sections_space=2,
            center_space_radius=40,
        )

        def legend_item(color, text, value):
            return ft.Row([
                ft.Container(width=10, height=10, bgcolor=color, border_radius=2),
                ft.Text(text, size=12, color=t["text_sec"]),
                ft.Text(value, size=12, color=t["text_main"], weight=ft.FontWeight.BOLD)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        return ft.Column(
            scroll=ft.ScrollMode.AUTO,
            controls=[
                self._header(self.tr("stats_title"), self.tr("stats_sub")),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),

                ft.Row([
                    stat_mini_card(self.tr("stat_avg_check"), f"1,850 {self.currency_symbol}", ft.Icons.ANALYTICS, 0),
                    stat_mini_card(self.tr("stat_max_pay"), f"12,500 {self.currency_symbol}", ft.Icons.SHOPPING_BAG, 1),
                    stat_mini_card(self.tr("stat_top_cat"), "Еда", ft.Icons.PIE_CHART, 3),
                ], spacing=20),

                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),

                ft.Container(
                    bgcolor=t["card_bg"],
                    border_radius=20,
                    padding=30,
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.BAR_CHART_ROUNDED, color=t["accent"]),
                            ft.Text(self.tr("chart_weekly"), size=16, weight=ft.FontWeight.BOLD, color=t["text_main"]),
                        ]),
                        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                        ft.Container(
                            height=250,
                            content=bar_chart
                        )
                    ])
                ),

                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),

                ft.Row([
                    ft.Container(
                        expand=2,
                        bgcolor=t["card_bg"],
                        border_radius=20,
                        padding=25,
                        content=ft.Column([
                            ft.Text(self.tr("chart_structure"), size=16, weight=ft.FontWeight.BOLD, color=t["text_main"]),
                            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                            ft.Row([
                                ft.Container(width=120, height=120, content=pie_chart),
                                ft.Container(width=20),
                                ft.Column([
                                    legend_item(t["accent"], "Еда", "40%"),
                                    legend_item("#FFAB00", "Транспорт", "30%"),
                                    legend_item("#FF5252", "Развлечения", "15%"),
                                    legend_item("#00BCD4", "Софт", "15%"),
                                ], expand=True, alignment=ft.MainAxisAlignment.CENTER, spacing=10)
                            ], alignment=ft.MainAxisAlignment.CENTER)
                        ])
                    ),
                    ft.Container(width=20),
                    ft.Container(
                        expand=1,
                        bgcolor=t["card_bg"],
                        border_radius=20,
                        padding=25,
                        content=ft.Column([
                            ft.Text(self.tr("stat_budget_health"), size=14, weight=ft.FontWeight.BOLD, color=t["text_main"]),
                            ft.Divider(height=15, color=ft.Colors.TRANSPARENT),
                            ft.Stack([
                                ft.PieChart(
                                    sections=[
                                        ft.PieChartSection(75, color="#00FF99", radius=10),
                                        ft.PieChartSection(25, color=ft.Colors.with_opacity(0.1, t["text_sec"]), radius=10),
                                    ],
                                    sections_space=0,
                                    center_space_radius=50
                                ),
                                ft.Container(
                                    alignment=ft.alignment.center,
                                    content=ft.Column([
                                        ft.Text("75%", size=20, weight=ft.FontWeight.BOLD, color="#00FF99"),
                                        ft.Text(self.tr("stat_safe_zone"), size=10, color=t["text_sec"])
                                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=0)
                                )
                            ], height=120),
                            ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                            ft.Text("Расходы в норме. Вы укладываетесь в лимиты.", size=11, color=t["text_sec"], text_align=ft.TextAlign.CENTER)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    )
                ])
            ]
        )

    def get_history_view(self):
        t = self.theme
        if self.is_edit_mode:
            action_bar = ft.Row([
                ft.Text(f"{self.tr('sel_count')} {len(self.selected_ids)}", color=t["text_main"], weight=ft.FontWeight.BOLD),
                ft.Row([
                    ft.TextButton(self.tr("btn_cancel"), on_click=self.toggle_edit_mode, style=ft.ButtonStyle(color=t["text_sec"])),
                    ft.ElevatedButton(
                        self.tr("btn_delete"), 
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
                    ft.IconButton(ft.Icons.FILE_DOWNLOAD_OUTLINED, icon_color=t["text_sec"], tooltip="CSV", on_click=self.export_to_csv),
                    ft.OutlinedButton(
                        self.tr("btn_select"), 
                        icon=ft.Icons.CHECK_BOX_OUTLINED,
                        style=ft.ButtonStyle(color=t["accent"], side=ft.BorderSide(1, t["accent"])),
                        on_click=self.toggle_edit_mode
                    )
                ])
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        return ft.Column(
            expand=True,
            controls=[
                self._header(self.tr("hist_title"), self.tr("hist_sub")),
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
                ft.dropdown.Option("1100x700", "Standard"),
                ft.dropdown.Option("1280x720", "HD"),
                ft.dropdown.Option("1920x1080", "Full HD"),
            ],
            on_change=self.resize_window_handler
        )

        return ft.Column(
            scroll=ft.ScrollMode.AUTO,
            controls=[
                self._header(self.tr("settings_title"), self.tr("dash_sub")),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                
                ft.Text(self.tr("set_gen"), color=t["text_sec"], weight=ft.FontWeight.BOLD),
                setting_card(ft.Icons.LANGUAGE, self.tr("lang_label"), lang_dropdown),
                ft.Container(height=5),
                setting_card(ft.Icons.MONETIZATION_ON_OUTLINED, self.tr("curr_label"), currency_dropdown),
                ft.Container(height=5),
                setting_card(ft.Icons.COLOR_LENS_OUTLINED, self.tr("theme_label"), theme_dropdown),

                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                ft.Text(self.tr("set_win"), color=t["text_sec"], weight=ft.FontWeight.BOLD),
                setting_card(ft.Icons.ASPECT_RATIO, self.tr("win_size"), size_dropdown),
                ft.Container(height=5),
                setting_card(ft.Icons.OPEN_IN_FULL, self.tr("win_resize"), resize_switch),

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
                            ft.Text(self.tr("credits"), color="white", weight=ft.FontWeight.BOLD, size=18)
                        ]
                    )
                )
            ]
        )

    def change_language(self, e):
        self.current_lang = e.control.value
        self.nav_rail = self._build_nav_rail()
        self._update_components_text()
        
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
        
        idx = self.nav_rail.selected_index if self.nav_rail.selected_index is not None else 6
        self.content_area.content = self._get_view_by_index(idx)
        self.page.update()

    def change_currency(self, e):
        self.currency_symbol = e.control.value
        self.amount_input.suffix_text = self.currency_symbol
        self.wallet_input.suffix_text = self.currency_symbol
        self._update_data_driven_ui()
        self.show_snackbar("Updated!")

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
                link_button(ft.Icons.CODE_OFF, "GitHub Репозиторий", "https://github.com/TryserPy/Foresight", "#333333" if t["mode"]==ft.ThemeMode.LIGHT else "#ffffff"),
                
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                ft.Text("Created with ❤️ using Flet & Python", size=10, color=t["text_sec"])
            ]
        )

        dlg = ft.AlertDialog(
            modal=True,
            bgcolor=t["card_bg"],
            content=content,
            actions=[
                ft.TextButton("Close", on_click=lambda e: self.page.close(dlg))
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER
        )
        self.page.open(dlg)

    def save_transaction_handler(self, e):
        if not self.amount_input.value or not self.category_dropdown.value:
            self.show_alert(self.tr("err_title"), "Please fill fields", is_error=True)
            return
        try:
            amount_val = float(self.amount_input.value)
        except ValueError:
            self.show_alert(self.tr("err_title"), self.tr("err_num"), is_error=True)
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
        self.show_snackbar(self.tr("snack_saved"))
        self.amount_input.value = ""
        self.comment_input.value = ""
        
        self.nav_rail.selected_index = 0
        self.content_area.content = self.get_dashboard_view()
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
        elif idx == 3: return self.get_statistics_view()
        elif idx == 4: return self.get_history_view()
        elif idx == 5: return self.get_wallet_view()
        elif idx == 6: return self.get_settings_view()
        return self.get_dashboard_view()

def main(page: ft.Page):
    app = DataMoneyApp(page)