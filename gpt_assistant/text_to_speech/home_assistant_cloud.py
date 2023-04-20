import sounddevice as sd
import requests
import json
from pydub import AudioSegment
from scipy.io import wavfile
import tempfile
import gpt_assistant.home_assistant.api as api


def download_file(file, url):
    response = requests.get(url)
    if response.status_code == 200:
        file.write(response.content)
    else:
        raise Exception(f"Error downloading file: {response.status_code}")


def text_to_speech(text):
    """Convert text to speech using Home Assistant Cloud TTS."""
    response = requests.post(f"{api.api_root}tts_get_url", headers=api.headers, data=json.dumps(
        {"language": "zh-HK", "message": text, "platform": "cloud"}))
    if response.status_code == 200:
        url = response.json()['url']
        try:
            with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as mp3_fp:
                download_file(mp3_fp, url)
                mp3_audio = AudioSegment.from_file(mp3_fp.name, format="mp3")
                with tempfile.NamedTemporaryFile(delete=True, suffix=".wav") as wav_fp:
                    mp3_audio.export(wav_fp.name, format="wav")
                    wav_fp.seek(0)

                    # Read audio data from the WAV file
                    sample_rate, audio_data = wavfile.read(wav_fp.name)

                    # Play the audio
                    sd.play(audio_data, sample_rate)
                    sd.wait()

        except Exception as e:
            raise Exception(f"Error converting text to speech: {str(e)}")
    else:
        print(f"Error: {response.status_code} | {response.text}")
