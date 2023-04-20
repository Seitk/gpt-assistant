import os
import openai


def transcribe_audio(filename):
    """Transcribe audio using OpenAI's Whisper"""
    file = open(filename, "rb")
    transcript = openai.Audio.transcribe("whisper-1", file=file, language=os.getenv("OPENAI_WHISPER_LANGUAGE", "en"))
    print("\rYou:", transcript.text)
    return transcript.text
