import os
import boto3
from pydub import AudioSegment
from scipy.io import wavfile
import tempfile
import sounddevice as sd
import gpt_assistant.sound as sound


def text_to_speech(text):
    """Convert text to speech using AWS Polly."""
    polly = boto3.client("polly")

    # Call the synthesize_speech method with your desired input text and output format
    response = polly.synthesize_speech(
        Text=text,
        OutputFormat="mp3",
        VoiceId=os.environ.get("AWS_POLLY_VOICE_ID", "Hiujin"),
        LanguageCode=os.environ.get("AWS_POLLY_LANGUAGE_CODE", "yue-CN"),
        Engine=os.environ.get("AWS_POLLY_ENGINE", "neural"),
    )

    # Save the synthesized speech to an mp3 file
    with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as f:
        f.write(response["AudioStream"].read())
        f.seek(0)
        mp3_audio = AudioSegment.from_file(f.name, format="mp3")
        with tempfile.NamedTemporaryFile(delete=True, suffix=".wav") as wav_fp:
            mp3_audio.export(wav_fp.name, format="wav")
            wav_fp.seek(0)
            sound.play(wav_fp.name)
