import pystray
from PIL import Image
import os


def run_pystray():
    icon_path = "download.ico"
    if not os.path.exists(icon_path):
        raise FileNotFoundError(f"Icon file '{icon_path}' not found.")
    icon_image = Image.open(icon_path)

    def exit_clicked(icon):
        icon.stop()

    menu = pystray.Menu(
        pystray.MenuItem("Exit", exit_clicked)
    )

    icon = pystray.Icon("name", icon_image, "My Tray App", menu)

    def setup(icon):
        icon.visible = False

    icon.run_detached(setup=setup)
