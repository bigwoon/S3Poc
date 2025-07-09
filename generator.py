# File: audio/generator.py

from transformers import pipeline
import scipy.io.wavfile
import os
import time
from datetime import datetime
from pydub import AudioSegment


# ✅ Preload globally
synthesiser = pipeline("text-to-audio", model="facebook/musicgen-small")

def trim_audio(file_path, duration_sec=30):
    audio = AudioSegment.from_wav(file_path)
    trimmed = audio[:duration_sec * 1000]  # pydub works in milliseconds
    trimmed.export(file_path, format="wav")


def generate_music_clip(prompt, output_dir="generated_audio"):
    print(f"🎧 Generating clip for prompt: '{prompt}'")
    start = time.time()

    # 🔊 Generate audio
    music = synthesiser(prompt, forward_params={"do_sample": True})

    end = time.time()
    print(f"⏱️ Generation took {end - start:.2f} seconds")

    os.makedirs(output_dir, exist_ok=True)
    filename = f"{datetime.now():%Y%m%d_%H%M%S}_{prompt[:20].replace(' ', '_')}.wav"
    file_path = os.path.join(output_dir, filename)

    scipy.io.wavfile.write(file_path, rate=music["sampling_rate"], data=music["audio"])
    print(f"💾 Saved audio to: {file_path}")

    return file_path, music["sampling_rate"]
