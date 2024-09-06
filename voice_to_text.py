import os
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


class VoiceToText:
    def __init__(self):
        self.client = initialize_groq_client()

    def transcribe_audio(self, audio_file_path:str):
        transcription = transcribe_audio(
            client=self.client,
            audio_file_path=audio_file_path,
        )
        # os.unlink(audio_file_path)
        return transcription

if __name__ == "__main__":
    vtt = VoiceToText()
    transcription = vtt.transcribe_audio("こんにちは.wav")
    # print(transcription)
    assert transcription == "こんにちは"
