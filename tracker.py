import flet as ft
import json
import os
from datetime import datetime

DATA_FILE = "workout_data.json"

def main(page: ft.Page):
    page.title = "المدرب الصارم Pro"
    page.bgcolor = "#0B101E"
    page.padding = 0
    page.horizontal_alignment = "center"

    try:
        page.window_width = 400
        page.window_height = 750
    except:
        pass

    def load_data():
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    app_data = load_data()

    # رأس التطبيق
    header = ft.Container(
        content=ft.Column([
            ft.Icon(ft.Icons.FITNESS_CENTER, color="#E11D48", size=45),
            ft.Text("المدرب الصارم", size=26, weight="bold", color="white"),
            ft.Text("لا أعذار اليوم.. استمر يا وحش!", color="#94A3B8", size=13)
        ], alignment="center", horizontal_alignment="center"),
        bgcolor="#1E293B",
        width=400,
        padding=25,
        border_radius=25,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=15, color="#000000")
    )

    def create_input(label, icon_obj):
        return ft.TextField(
            label=label,
            prefix_icon=icon_obj,
            border_radius=12,
            border_color="#334155",
            focused_border_color="#E11D48",
            bgcolor="#1E293B",
            color="white",
            height=60,
            text_size=15
        )

    pushups_input = create_input("شناو (Pushups)", ft.Icons.SPORTS_GYMNASTICS)
    pullups_input = create_input("عقلة (Pullups)", ft.Icons.STRAIGHTEN)
    dumbbells_input = create_input("دامبلز (Dumbbells)", ft.Icons.FITNESS_CENTER)

    history_list = ft.ListView(expand=True, spacing=10, padding=15)

    def update_history():
        history_list.controls.clear()
        if not app_data:
            history_list.controls.append(
                ft.Container(
                    content=ft.Text("لم تبدأ بعد! الساحة بانتظارك.", color="#94A3B8", size=15),
                    padding=20
                )
            )
        else:
            for date, stats in sorted(app_data.items(), reverse=True):
                card = ft.Container(
                    content=ft.Row([
                        ft.Container(
                            content=ft.Icon(ft.Icons.LOCAL_FIRE_DEPARTMENT, color="#E11D48", size=22),
                            bgcolor="#2A1618",
                            padding=10,
                            border_radius=10
                        ),
                        ft.Column([
                            ft.Text(f"تاريخ: {date}", weight="bold", size=14, color="white"),
                            ft.Text(f"شناو: {stats.get('pushups', 0)} | عقلة: {stats.get('pullups', 0)} | دامبلز: {stats.get('dumbbells', 0)}", color="#94A3B8", size=12)
                        ], spacing=2)
                    ]),
                    bgcolor="#1E293B",
                    border_radius=12,
                    padding=12,
                    shadow=ft.BoxShadow(blur_radius=4, color="#00000040")
                )
                history_list.controls.append(card)
        page.update()

    def save_workout(e):
        today = datetime.now().strftime("%Y-%m-%d")

        p_val = pushups_input.value
        pu_val = pullups_input.value
        d_val = dumbbells_input.value

        p = int(p_val) if p_val and p_val.strip().isdigit() else 0
        pu = int(pu_val) if pu_val and pu_val.strip().isdigit() else 0
        d = int(d_val) if d_val and d_val.strip().isdigit() else 0

        if p == 0 and pu == 0 and d == 0:
            return

        if today not in app_data:
            app_data[today] = {"pushups": 0, "pullups": 0, "dumbbells": 0}

        app_data[today]["pushups"] += p
        app_data[today]["pullups"] += pu
        app_data[today]["dumbbells"] += d

        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(app_data, f, indent=4, ensure_ascii=False)

        pushups_input.value = ""
        pullups_input.value = ""
        dumbbells_input.value = ""

        update_history()

        snack = ft.SnackBar(
            content=ft.Text("🔥 عاش يا بطل! تم تسجيل تمرينك بنجاح.", color="white", size=14, weight="bold"),
            bgcolor="#059669",
            duration=2500
        )
        page.overlay.append(snack)
        snack.open = True
        page.update()

    save_btn = ft.Container(
        content=ft.ElevatedButton(
            content=ft.Row([
                ft.Icon(ft.Icons.ADD_TASK, color="white"),
                ft.Text("سجل الإنجاز", color="white", size=16, weight="bold")
            ], alignment="center", spacing=8),
            style=ft.ButtonStyle(
                bgcolor="#E11D48",
                shape=ft.RoundedRectangleBorder(radius=12),
                padding=15,
            ),
            on_click=save_workout,
        ),
        width=360,
        padding=10
    )

    inputs_container = ft.Container(
        content=ft.Column([
            pushups_input,
            pullups_input,
            dumbbells_input,
        ], spacing=12),
        width=360,
        padding=10
    )

    page.add(
        header,
        inputs_container,
        save_btn,
        ft.Container(
            content=ft.Text("📜 سجل الانضباط:", size=16, weight="bold", color="white"),
            width=360,
            padding=10  # هنا تم التعديل لرقم مباشر وصافي
        ),
        history_list
    )

    update_history()

if __name__ == "__main__":
    if hasattr(ft, "run"):
    ft.run(main)
else:
    ft.app(target=main)
