from .dataholders import AudioData

import librosa
from moviepy import AudioClip, AudioFileClip, CompositeAudioClip, concatenate_audioclips
from proglog import default_bar_logger
import numpy as np
import magic

def is_valid_audio(file):
    try:
        return magic.from_file(file, mime=True).startswith("audio/")
    except:
        return False

def analyze_audio(audio_path, tightness, deviation, clips_per_beat, clips_start_offset, log=True):
    logger = default_bar_logger("bar")
    if log: logger(message="[1/5]  Analyzing audio beats")
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

    clip_durations = figure_out_durations(clips_per_beat, beats, audio.duration, clips_start_offset, deviation)
    return AudioData(clip_durations=clip_durations, duration=audio.duration, clip=audio)

def figure_out_durations(clips_per_beat, beats, duration, clips_start_offset, beat_deviation):
    # Beat boundaries (0 -> beat1 -> beat2 -> ... -> end)
    beat_times = np.concatenate(([0.0], beats, [duration]))
    num_intervals = len(beat_times) - 1

    total_clips = max(1, round(num_intervals * clips_per_beat))

    # Compute the normal clip boundary times.
    boundaries = []
    for i in range(total_clips):
        beat_pos = i * num_intervals / total_clips

        interval = int(beat_pos)
        frac = beat_pos - interval

        start = beat_times[interval]
        end = beat_times[interval + 1]
        boundaries.append(start + frac * (end - start))

    boundaries.append(duration)

    # Keep only boundaries after the offset.
    boundaries = [t for t in boundaries if t > clips_start_offset]

    durations = []
    previous = clips_start_offset

     # Convert to duration list
    for t in boundaries:
        durations.append(t - previous)
        previous = t

    # Make sure the first clip isn't too short (could happen if audio starts shortly before next beat)
    if durations[0] < durations[1] - beat_deviation:
        durations[0] += durations.pop(0)

    return durations

def align_audio_for_intro(audio:AudioClip, audio_time_of_end, intro_duration):
    """
    Return a mutated `audio` in such a way that if an intro of length `intro_duration` starts playing
    when the audio begins, the intro's end exactly matches the timestamp `audio_time_of_end` of the
    (initially provided) audio.

    If `audio_time_of_end` is None, return a mutation in such a way that if an intro intro of length
    `intro_duration` starts playing when the audio begins, the main audio content only starts at the exact
    time the intro ends.
    
    Return the unmutated audio if `audio_time_of_end >= audio.duration` or `intro_duration >= audio.duration`.
    """
    if not audio_time_of_end:
        return pad_audio_beginning(audio, intro_duration)
    
    if audio_time_of_end >= audio.duration or intro_duration >= audio.duration:
        return audio
    
    diff = audio_time_of_end - intro_duration
    if diff > 0:
        return audio.subclipped(abs(diff))
    else:
        return pad_audio_beginning(audio, abs(diff))


def pad_audio_beginning(audio, silence_duration):
    if silence_duration > 0:

        silence_clip = AudioClip(
            lambda t: np.zeros(audio.nchannels),
            duration=silence_duration,
            fps=audio.fps
        )

        return concatenate_audioclips([silence_clip, audio])
        
    return audio

def add_audio(video_clip, audio_clip):
    if not video_clip.audio:
        return video_clip.with_audio(audio_clip)
    
    combined_audio = CompositeAudioClip([video_clip.audio, audio_clip])
    return video_clip.with_audio(combined_audio)
