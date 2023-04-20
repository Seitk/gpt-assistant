import subprocess
import os


def transcribe_audio(filename):
    """Transcribe audio using local Whisper"""

    options = os.getenv("WHISPER_CMD_OPTIONS", "--model tiny.en --language en")

    # Replace this command with the actual Whisper CLI command
    # cmd = f"whisper --model {WHISPER_MODEL} {filename} --language en --output_format txt --fp16 False  | cut -c 28-"
    cmd = f"whisper {options} {filename} --output_format txt --fp16 False {filename} | cut -c 28-"
    result = subprocess.run(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, shell=True, text=True)

    if result.returncode == 0:
        transcription = result.stdout.strip()
        print("\rYou:", transcription)
        return transcription
    else:
        print("Error:", result.stderr)
        return None
