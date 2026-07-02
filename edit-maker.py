#!/usr/bin/env python3

import argparse

arg_parser = argparse.ArgumentParser("edit-maker", description="Generates TikTik edits")
arg_parser.add_argument("audio", help="The audio file to use for the edit", type=str)
arg_parser.add_argument("output", help="The output file to save the edit in", type=str)
arg_parser.add_argument("--beat-tightness", "-t", help="The tightness of the detected audio beat distribution around tempo", type=float, default=100, nargs='?')
args = arg_parser.parse_args()

import librosa
from moviepy import AudioFileClip, ColorClip, concatenate_videoclips

audio_path = args.audio
output_path = args.output

# Analyze audio
y, sr = librosa.load(audio_path)
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr, tightness=args.beat_tightness)
beat_times = librosa.frames_to_time(beat_frames, sr=sr)

audio = AudioFileClip(audio_path)
duration = audio.duration

clips = []

colors = [(0, 0, 255), (0, 255, 0)]
current_color = 0
previous = 0

for beat in beat_times:
    clips.append(
        ColorClip(
            size=(1080, 1920),
            color=colors[current_color],
            duration=beat - previous,
        )
    )
    current_color ^= 1
    previous = beat

# Tail after the last beat
clips.append(
    ColorClip(
        size=(1080, 1920),
        color=colors[current_color],
        duration=duration - previous,
    )
)

video = concatenate_videoclips(clips)
fvideo = video.with_audio(audio)

fvideo.write_videofile(
    output_path,
    fps=30,
    codec="libx264",
    audio_codec="aac",
    audio_bitrate="192k"
)
