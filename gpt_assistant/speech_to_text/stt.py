import os
import gpt_assistant.speech_to_text.openai as openai
import gpt_assistant.speech_to_text.whisper_local as whisper_local

def transcribe(filename):
    """Transcribe audio into text."""
    provider = os.getenv("STT_PROVIDER", "openai")
    print("\rProcessing audio with", provider, "...")
    if provider == "whisper_local":
        return whisper_local.transcribe_audio(filename)
    else:
        return openai.transcribe_audio(filename)
