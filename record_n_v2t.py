from voice_to_text import VoiceToText
from recording import Recorder
from queue import Queue
import threading
import pyaudio


def streming_v2t(SAMPLE_RATE:int, CHANNELS:int, CHUNK:int):
    queue = Queue()

    def recorder_thread():
        recorder = Recorder(CHANNELS=CHANNELS, SAMPLE_RATE=SAMPLE_RATE, CHUNK=CHUNK)
        save_audio_fn = recorder.save_audio
        try:
            while True:
                data = recorder.get_sound()
                queue.put(data)
        finally:
            recorder.stop()

    def v2t_thread():
        v2t = VoiceToText()
        sound_window = []
        max_sound_window_len = 10

        while True:
            if not queue.empty():
                data = queue.get()

                if len(sound_window) < max_sound_window_len:
                    sound_window.pop(0)
                sound_window.append(data)

                sound_window.put(data)
                sound = sum(sound_window)

                f_name = save_audio_fn(sound, SAMPLE_RATE, CHANNELS)

                text = v2t.transcribe(f_name)
                print(text)

    threading.Thread(target=recorder_thread, args=(), daemon=True).start()
    threading.Thread(target=v2t_thread, args=(), daemon=True).start()

if __name__ == "__main__":
    SAMPLE_RATE = 16000
    CHANNELS = 1
    CHUNK = 1024
    streming_v2t(SAMPLE_RATE, CHANNELS, CHUNK)

