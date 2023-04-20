# from process import execute
from datetime import datetime
import time
import wave
import struct
from pvrecorder import PvRecorder
import pvporcupine
import os
import tempfile

from dotenv import load_dotenv
load_dotenv()

keyword_paths = [os.environ["PORCUPINE_KEYWORD_PATH"]]
try:
    porcupine = pvporcupine.create(
        access_key=os.environ["PORCUPINE_ACCESS_KEY"],
        keyword_paths=keyword_paths,
    )
except pvporcupine.PorcupineActivationError as e:
    print("AccessKey activation error")
    raise e
except pvporcupine.PorcupineError as e:
    print("Failed to initialize Porcupine")
    raise e

keywords = list()
for x in keyword_paths:
    keyword_phrase_part = os.path.basename(x).replace('.ppn', '').split('_')
    if len(keyword_phrase_part) > 6:
        keywords.append(' '.join(keyword_phrase_part[0:-6]))
    else:
        keywords.append(keyword_phrase_part[0])


def listen_for_wake_word(callback):
    with tempfile.NamedTemporaryFile(delete=True, suffix=".wav") as wav_file:
        recorder = PvRecorder(
            device_index=0, frame_length=porcupine.frame_length)

        f = wave.open(wav_file.name, "w")
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(16000)

        try:
            print("Waiting for wake word...")
            while True:
                recorder.start()
                pcm = recorder.read()
                result = porcupine.process(pcm)

                if f is not None:
                    f.writeframes(struct.pack("h" * len(pcm), *pcm))

                if result >= 0:
                    recorder.stop()
                    callback()
                    print("Waiting for wake word...")

        except KeyboardInterrupt:
            print('Stopping ...')
        finally:
            recorder.delete()
            porcupine.delete()
            f.close()
