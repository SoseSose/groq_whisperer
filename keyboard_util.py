
import keyboard
import pyperclip


trigger_key = "ctrl+shift+h"

def copy_to_clipboard_and_paste(text:str):
    pyperclip.copy(text)
    keyboard.send("ctrl+v")

print(f"Press and hold {trigger_key} to start recording...")
keyboard.wait(trigger_key)
print(f"Recording... (Release {trigger_key} to stop)")
