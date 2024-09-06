import flet as ft
import asyncio


class Countdown(ft.Text):
    def __init__(self, seconds):
        super().__init__()
        self.seconds = seconds
        self.color = ft.colors.BLACK

    def did_mount(self):
        self.running = True
        self.page.run_task(self.update_timer)

    def will_unmount(self):
        self.running = False

    async def update_timer(self):
        while self.seconds and self.running:
            mins, secs = divmod(self.seconds, 60)
            self.value = "{:02d}:{:02d}".format(mins, secs)
            self.update()
            await asyncio.sleep(1)
            self.seconds -= 1



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

    # いらないかも
    minimize_button = ft.IconButton(
        icon=ft.icons.REMOVE,
        icon_color=ft.colors.WHITE,
        bgcolor=ft.colors.BLUE,
        icon_size=24,
        tooltip="最小化",
        on_click=lambda _: page.window.minimize(),
    )

    close_button = ft.IconButton(
        icon=ft.icons.STOP,
        icon_color=ft.colors.WHITE,
        bgcolor=ft.colors.RED,
        icon_size=24,
        tooltip="閉じる",
        on_click=lambda _: page.window.close(),
    )

    text_area = ft.Container(
        content=Countdown(100),
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
