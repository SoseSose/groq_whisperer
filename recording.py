import pyaudio
import numpy as np
import tempfile
import wave

class Recorder:
    def __init__(self, channels:int, sample_rate:int, chunk:int):

        self.CHANNELS = channels
        self.SAMPLE_RATE = sample_rate
        self.CHUNK = chunk

        self.pa = pyaudio.PyAudio()
        self.stream = self.pa.open(
            format=pyaudio.paInt16,
            channels=channels,
            rate=sample_rate,
            input=True,
            frames_per_buffer=self.CHUNK,
        )
        print("recording start")


    def get_sound(self):
        data = self.stream.read(self.CHUNK, exception_on_overflow=False)
        # data = np.frombuffer(data, dtype="int16") / float((np.power(2, 16) / 2) - 1)
        return data

    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.pa.terminate()

    def save_audio(self, frames:list):
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
            with wave.open(temp_audio.name, "wb") as wf:
                wf.setnchannels(self.CHANNELS)
                wf.setsampwidth(self.pa.get_sample_size(pyaudio.paInt16))
                wf.setframerate(self.SAMPLE_RATE)
                wf.writeframes(b"".join(frames))
            return temp_audio.name

if __name__ == "__main__":

    recorder = Recorder(channels=1, sample_rate=44100, chunk=1024)
    frames = []
    import time
    record_time = 3
    start_time = time.time()
    for i in range(1, int(44100 / 1024 * record_time)):
        data = recorder.get_sound()
        frames.append(data)
    end_time = time.time()
    print(f"recording time: {end_time - start_time}")

    recorder.stop()
    audio_file_path = recorder.save_audio(frames)
    print(audio_file_path)
    import os
    # os.unlink(audio_file_path)
 
    CHUNK_SIZE = 2**10

    from pydub import AudioSegment
    audio = AudioSegment.from_wav(audio_file_path)
    audio += 20
    audio.export(audio_file_path, format="wav")

    
    wf = wave.open(audio_file_path, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    
    data = wf.readframes(CHUNK_SIZE)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK_SIZE)
    
    stream.stop_stream()
    stream.close()
    p.terminate()
