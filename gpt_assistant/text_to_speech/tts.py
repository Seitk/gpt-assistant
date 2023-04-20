import os
import gpt_assistant.text_to_speech.gtts as gtts
import gpt_assistant.text_to_speech.aws_polly as aws_polly
import gpt_assistant.text_to_speech.home_assistant_cloud as hatts

def text_to_speech(text: str):
    """Convert text to speech."""
    print("\rAI:", text)
    provider = os.environ.get("TTS_PROVIDER", "google_tts")
    if provider == 'google_tts':
        gtts.text_to_speech(text)
    elif provider == 'aws_polly':
        aws_polly.text_to_speech(text)
    else:
        hatts.text_to_speech(text)
