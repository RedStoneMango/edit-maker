from .dataholders import AudioData

import librosa
from moviepy import AudioFileClip
from proglog import default_bar_logger
import numpy as np

def analyze_audio(audio_path, tightness, clips_per_beat):
    logger = default_bar_logger("bar")
    logger(message="[1/5]  Analyzing audio beats")
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

    clip_durations = figure_out_durations(clips_per_beat, beats, audio.duration)
    return AudioData(clip_durations=clip_durations, duration=audio.duration, clip=audio)

def figure_out_durations(clips_per_beat, beats, duration):
    # Beat boundaries (0 -> beat1 -> beat2 -> ... -> end)
    beat_times = np.concatenate(([0.0], beats, [duration]))
    num_intervals = len(beat_times) - 1

    total_clips = max(1, round(num_intervals * clips_per_beat))

    durations = []
    previous = 0.0

    for i in range(total_clips):
        # Position of this clip on the beat axis
        beat_pos = i * num_intervals / total_clips

        interval = int(beat_pos)
        frac = beat_pos - interval

        # Interpolate within that beat interval
        start = beat_times[interval]
        end = beat_times[interval + 1]
        t = start + frac * (end - start)

        durations.append(t - previous)
        previous = t

    durations.append(duration - previous)
    return durations