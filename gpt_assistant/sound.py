from scipy.io import wavfile

import sounddevice as sd


def play(filename):
    sample_rate, audio_data = wavfile.read(filename)
    sd.play(audio_data, sample_rate)
    sd.wait()
