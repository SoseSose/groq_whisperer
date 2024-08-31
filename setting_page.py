import flet as ft

#設定画面はトレイからのみ呼び出し
def main(page: ft.Page):
    page.title = "Voice Assistant"
    page.padding = 10
    page.bgcolor = ft.colors.BLUE_GREY_100
    page.window.width = 300
    page.window.height = 400
    page.window.resizable = False
    page.window.always_on_top = True
    page.window.title_bar_hidden = True
    page.window.title_bar_buttons_hidden = True


    def minimize_window(e):
        page.window.minimized = True
        page.update()

    back_button = ft.IconButton(
        icon=ft.icons.REMOVE,
        icon_color=ft.colors.WHITE,
        bgcolor=ft.colors.BLUE,
        icon_size=24,
        tooltip="最小化",
        on_click=minimize_window,
    )

    close_button = ft.IconButton(
        icon=ft.icons.CLOSE,
        icon_color=ft.colors.WHITE,
        bgcolor=ft.colors.RED,
        icon_size=24,
        tooltip="閉じる",
        on_click=lambda _: page.window.close(),
    )

    settings_area = ft.Container(
        content=ft.Column(
            [
                ft.Text("設定", size=20, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Switch(label="通知を有効にする", value=True),
                ft.Slider(min=0, max=100, divisions=10, label="音量"),
                ft.Dropdown(
                    label="テーマ",
                    options=[
                        ft.dropdown.Option("ライト"),
                        ft.dropdown.Option("ダーク"),
                        ft.dropdown.Option("システム設定に従う"),
                    ],
                    value="システム設定に従う",
                ),
                ft.ElevatedButton("設定を保存", on_click=lambda _: page.go("/recording")),
            ]
        ),
        bgcolor=ft.colors.WHITE,
        border_radius=ft.border_radius.all(10),
        padding=20,
        expand=True,
    )

    top_row = ft.Row(
        [back_button, close_button],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    content = ft.Column(
        [
            top_row,
            ft.Container(height=10),
            settings_area,
        ],
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    page.add(content)



if __name__ == "__main__":
    ft.app(target=main)
