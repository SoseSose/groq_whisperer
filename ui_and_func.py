from ui.recording_page import TextArea
import flet as ft
from voice_to_text import StreamingV2T


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

    v2t = StreamingV2T(channels=1, sample_rate=44100, chunk=1024, record_time=10)

    def close_window(e):
        v2t.stop_update_text()
        page.window.close()

    minimize_button = ft.IconButton(
        icon=ft.icons.REMOVE,
        icon_color=ft.colors.WHITE,
        bgcolor=ft.colors.BLUE,
        icon_size=24,
        tooltip="最小化",
        on_click=minimize_window,
    )

    close_button = ft.IconButton(
        icon=ft.icons.STOP,
        icon_color=ft.colors.WHITE,
        bgcolor=ft.colors.RED,
        icon_size=24,
        tooltip="閉じる",
        on_click=close_window,
    )

    text_area = ft.Container(
        content=TextArea(v2t),
        bgcolor=ft.colors.WHITE,
        border_radius=ft.border_radius.all(10),
        padding=10,
        alignment=ft.alignment.center,
        expand=True,
    )

    top_row = ft.Row(
        [minimize_button, close_button],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    content = ft.Column(
        [
            top_row,
            ft.Container(height=10),
            text_area,
        ],
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    page.add(content)


if __name__ == "__main__":
    ft.app(target=main)
