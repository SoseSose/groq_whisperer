from voice_to_text import VoiceToText
from recording import Recorder
from queue import Queue
import threading
import pyaudio


def streming_v2t(channels:int, sample_rate:int, chunk:int, record_time:int):
    queue = Queue()

    recorder = Recorder(channels=channels, sample_rate=sample_rate, chunk=chunk)
    save_audio_fn = recorder.save_audio

    def recorder_thread():
        try:
            while True:
                data = recorder.get_sound()
                queue.put(data)

        except Exception as e:
            print(e.str())
        finally:
            recorder.stop()



    def v2t_thread():
        v2t = VoiceToText()
        max_sound_window_len = record_time * sample_rate // chunk 
        sound_window = []

        while True:
            if not queue.empty():
                sound_window.append(queue.get())
                sound_window = sound_window[len(sound_window) - max_sound_window_len:]
                f_name = save_audio_fn(sound_window)

                text = v2t.transcribe_audio(f_name)
                print(text)

    threading.Thread(target=recorder_thread, args=(), daemon=True).start()
    # threading.Thread(target=v2t_thread, args=(), daemon=True).start()
    v2t_thread()

if __name__ == "__main__":
    SAMPLE_RATE = 16000
    CHANNELS = 1
    CHUNK = 1024 * 10
    record_time = 10
    streming_v2t(channels=CHANNELS, sample_rate=SAMPLE_RATE, chunk=CHUNK, record_time=record_time)

