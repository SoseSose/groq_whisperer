import os
import tempfile
import wave
import pyaudio
import keyboard
import pyperclip
from groq import Groq


def read_api_key(file_path="key.txt"):
    try:
        with open(file_path, "r") as file:
            return file.read().strip()
    except (FileNotFoundError, IOError) as e:
        print(f"Error reading API key: {e}")
        return None


def initialize_groq_client():
    api_key = read_api_key()
    if not api_key:
        print("Failed to initialize Groq client. Exiting.")
        exit(1)
    return Groq(api_key=api_key)


def record_audio(trigger_key:str, SAMPLE_RATE:int, CHANNELS:int, CHUNK:int):
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=CHANNELS,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    print(f"Press and hold {trigger_key} to start recording...")
    keyboard.wait(trigger_key)
    print(f"Recording... (Release {trigger_key} to stop)")

    frames = []
    while keyboard.is_pressed(trigger_key):
        frames.append(stream.read(CHUNK))

    print("Recording finished.")
    stream.stop_stream()
    stream.close()
    p.terminate()

    return frames


def save_audio(frames:list, SAMPLE_RATE:int, CHANNELS:int):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
        with wave.open(temp_audio.name, "wb") as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
            wf.setframerate(SAMPLE_RATE)
            wf.writeframes(b"".join(frames))
        return temp_audio.name


def transcribe_audio(client:Groq, audio_file_path:str):
    try:
        with open(audio_file_path, "rb") as file:
            return client.audio.transcriptions.create(
                file=(os.path.basename(audio_file_path), file.read()),
                model="whisper-large-v3",
                response_format="text",
                language="ja",
            )
    except Exception as e:
        print(f"Transcription error: {e}")
        return None


def copy_to_clipboard_and_paste(text:str):
    pyperclip.copy(text)
    keyboard.send("ctrl+v")

def replace_hallucination(text:str):
    HALLUCINATION_TEXTS = [
        "ご視聴ありがとうございました", "ご視聴ありがとうございました。",
        "ありがとうございました", "ありがとうございました。",
        "どうもありがとうございました", "どうもありがとうございました。",
        "どうも、ありがとうございました", "どうも、ありがとうございました。",
        "おやすみなさい", "おやすみなさい。",
        "Thanks for watching!",
        "終わり", "おわり",
        "お疲れ様でした", "お疲れ様でした。",
    ]
    for hallucination_text in HALLUCINATION_TEXTS:
        text = text.replace(hallucination_text, "")
    return text

def main():
    SAMPLE_RATE = 16000
    CHANNELS = 1
    CHUNK = 1024
    DEFAULT_TRIGGER_KEY = "ctrl+shift+h"
    trigger_key = DEFAULT_TRIGGER_KEY
    client = initialize_groq_client()

    while True:

        
        frames = record_audio(
            trigger_key=trigger_key,
            SAMPLE_RATE=SAMPLE_RATE,
            CHANNELS=CHANNELS,
            CHUNK=CHUNK,
        )
        temp_audio_file = save_audio(
            frames=frames,
            SAMPLE_RATE=SAMPLE_RATE,
            CHANNELS=CHANNELS,
        )

        print("Transcribing...")
        transcription = transcribe_audio(
            client=client,
            audio_file_path=temp_audio_file,
        )

        if transcription:
            print("\nTranscription:")
            print(transcription)
            print("Copying transcription to clipboard...")
            transcription = replace_hallucination(transcription)
            copy_to_clipboard_and_paste(transcription)
            print("Transcription copied to clipboard and pasted.")
        else:
            print("Transcription failed.")

        os.unlink(temp_audio_file)
        print(f"\nReady for next recording. Press {trigger_key} to start.")


if __name__ == "__main__":
    main()
