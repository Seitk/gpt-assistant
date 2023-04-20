import os
import time
import audioop
import tempfile
from dotenv import load_dotenv
import speech_recognition as sr
import gpt_assistant.sound as sound
import gpt_assistant.speech_to_text.stt as speech


load_dotenv()


recognizer = sr.Recognizer()
with sr.Microphone() as source:
    audio = recognizer.listen(source)


def process_audio(audio):
    with tempfile.NamedTemporaryFile(delete=True, suffix=".wav") as f:
        f.write(audio.get_wav_data())
        f.seek(0)
        return speech.transcribe(f.name)


def is_speech_ended(recognizer, source, audio_data):
    sensitivity = int(os.environ.get("AUDIO_RECORD_SENSITIVITY", "500"))
    debounce = int(os.environ.get("AUDIO_RECORD_DEBOUNCING", "1"))  # seconds
    sample_duration = float(os.environ.get("AUDIO_RECORD_SAMPLE_DURATION", "0.25"))  # seconds
    pause_count_target = debounce / sample_duration

    pause_count = 0
    speech_detected = False

    # Detect if speech has ended and
    while pause_count < pause_count_target:
        recognizer.energy_threshold = sensitivity
        audio_segment = recognizer.record(source, duration=sample_duration)
        rms = audioop.rms(audio_segment.frame_data, audio_segment.sample_width)

        # Detect if speech is recognized
        if rms < recognizer.energy_threshold:
            # If speech is detected, increment pause_count
            if speech_detected:
                pause_count += 1
        else:
            # Reset pause_count if speech is detected
            speech_detected = True
            pause_count = 0

        # Start recording if speech is detected
        if speech_detected:
            audio_data.append(audio_segment)

        time.sleep(0.25)

    return True


def listen_for_speech():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("\rWaiting for command...")
        audio_data = []

        sound.play("./audio/start.wav")
        while not is_speech_ended(recognizer, source, audio_data):
            pass
        sound.play("./audio/end.wav")

        audio = sr.AudioData(b''.join([segment.get_raw_data(
        ) for segment in audio_data]), source.SAMPLE_RATE, source.SAMPLE_WIDTH)
        return process_audio(audio)
