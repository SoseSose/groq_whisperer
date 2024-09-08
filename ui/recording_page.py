import threading
import time
import flet as ft

class TextArea(ft.Text):
    def __init__(self, text_model):
        super().__init__()
        self.text_model = text_model
        self.text_model.start_update_text()

    def did_mount(self):
        self.page.run_thread(self.update_text)

    def will_unmount(self):
        self.text_model.stop_update_text()

    def update_text(self):
        while self.text_model.running:
            self.value = self.text_model.text
            self.update()
            time.sleep(0.1)

class TextModel:
    def __init__(self):
        self.text = "start"
    
    def stop_update_text(self):
        self.running = False

    def start_update_text(self):
        self.running = True
        def update_text():
            while self.running:
                self.text = time.time()
                print(self.text)
                time.sleep(1)

        thread = threading.Thread(target=update_text, daemon=True)
        thread.start()

