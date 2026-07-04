from .dataholders import AudioData

import librosa
from moviepy import AudioFileClip
from proglog import default_bar_logger

def analyze_audio(audio_path, tightness):
    logger = default_bar_logger("bar")
    logger(message="[1/5]  Analyzing audio")
    logger.iter_bar(progress=range(5))

    logger.bars_callback("progress", "index", 1, 0)
    y, sr = librosa.load(audio_path)
    logger.bars_callback("progress", "index", 2, 1)
    _, beat_frames = librosa.beat.beat_track(y=y, sr=sr, tightness=tightness)
    logger.bars_callback("progress", "index", 3, 2)
    beats = librosa.frames_to_time(beat_frames, sr=sr)
    logger.bars_callback("progress", "index", 4, 3)
    audio = AudioFileClip(audio_path)
    logger.bars_callback("progress", "index", 5, 4)
    return AudioData(beats=beats, duration=audio.duration, clip=audio)
