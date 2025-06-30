# File: audio/generator.py

from transformers import pipeline
import scipy.io.wavfile
import os
from datetime import datetime

def generate_music_clip(prompt, output_dir="generated_audio"):
    synthesiser = pipeline("text-to-audio", model="facebook/musicgen-small")
    music = synthesiser(prompt, forward_params={"do_sample": True})

    os.makedirs(output_dir, exist_ok=True)
    filename = f"{datetime.now():%Y%m%d_%H%M%S}_{prompt[:20].replace(' ', '_')}.wav"
    file_path = os.path.join(output_dir, filename)

    scipy.io.wavfile.write(file_path, rate=music["sampling_rate"], data=music["audio"])
    return file_path, music["sampling_rate"]
