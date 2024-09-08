from wav_to_text import VoiceToText
from voice_to_wav import Recorder
from queue import Queue
import threading

class StreamingV2T:
    def __init__(self, channels:int, sample_rate:int, chunk:int, record_time:int):
        self.text:str = ""
        self.channels = channels
        self.sample_rate = sample_rate
        self.chunk = chunk
        self.record_time = record_time
        self.running = False

    def stop_update_text(self):
        print("stop_update_text")
        self.running = False

    def start_update_text(self):
        print("start_update_text")
        self.running = True
        queue = Queue()

        recorder = Recorder(channels=self.channels, sample_rate=self.sample_rate, chunk=self.chunk)
        save_audio_fn = recorder.save_audio

        def record_fn():

            while self.running:
                data = recorder.get_sound()
                queue.put(data)

        def v2t_fn():
            v2t = VoiceToText()
            max_sound_window_len = self.record_time * self.sample_rate // self.chunk 
            sound_window = []

            while self.running:
                if not queue.empty():
                    sound_window.append(queue.get())
                    sound_window    
                    if len(sound_window) >= max_sound_window_len:
                        sound_window = sound_window[1:]
                    f_name = save_audio_fn(sound_window)

                    text = v2t.transcribe_audio(f_name)
                    print(text)
                    self.text = text

        record_thread = threading.Thread(target=record_fn)
        record_thread.start()
        v2t_thread = threading.Thread(target=v2t_fn)
        v2t_thread.start()


if __name__ == "__main__":
    SAMPLE_RATE = 16000
    CHANNELS = 1
    CHUNK = 1024 * 10
    record_time = 10
    streming_v2t = StreamingV2T(channels=CHANNELS, sample_rate=SAMPLE_RATE, chunk=CHUNK, record_time=record_time)
    streming_v2t.start_update_text()
    import time
    time.sleep(10)
    streming_v2t.stop_update_text()

