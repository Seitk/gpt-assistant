import sounddevice as sd
import tempfile
from gtts import gTTS
from scipy.io import wavfile
from pydub import AudioSegment

def text_to_speech(text):
    """Convert text to speech using Google TTS."""
    tts = gTTS(text, lang="en")
    
    # Save speech to a temporary file
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        tts.save(fp.name)
        fp.seek(0)
        
        # Convert MP3 to WAV using pydub
        mp3_audio = AudioSegment.from_file(fp.name, format="mp3")
        with tempfile.NamedTemporaryFile(delete=True, suffix=".wav") as wav_fp:
            mp3_audio.export(wav_fp.name, format="wav")
            wav_fp.seek(0)

            # Read audio data from the WAV file
            sample_rate, audio_data = wavfile.read(wav_fp.name)

            # Play the audio
            sd.play(audio_data, sample_rate)
            sd.wait()
