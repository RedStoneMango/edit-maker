#!/usr/bin/env python3

import argparse

arg_parser = argparse.ArgumentParser("edit-maker", description="Generates TikTik edits")
arg_parser.add_argument("audio", help="The audio file to use for the edit", type=str)
arg_parser.add_argument("output", help="The output file to save the edit in", type=str)
arg_parser.add_argument("graphics", help="The graphics to be used in the edit", type=str, nargs="+")
arg_parser.add_argument("--beat-tightness", "-t", help="The tightness of the detected audio beat distribution around tempo", type=float, default=100, nargs='?')

import librosa
import magic
import os
from moviepy import AudioFileClip, ImageClip, VideoFileClip, concatenate_videoclips

is_video_cache = {}

def main():
    args = arg_parser.parse_args()
    
    audio_data = analyze_audio(args.audio, args.beat_tightness)
    clips = build_clips(audio_data, args.graphics)
    render(clips, audio_data, args.output)

def analyze_audio(audio_path, tightness):
    y, sr = librosa.load(audio_path)
    _, beat_frames = librosa.beat.beat_track(y=y, sr=sr, tightness=tightness)
    beats = librosa.frames_to_time(beat_frames, sr=sr)
    audio = AudioFileClip(audio_path)
    return (beats, audio.duration, audio)

def build_clips(audio_data, graphics):
    beats, duration, _ = audio_data
    clips = []

    current_graphic = 0
    previous = 0

    for beat in beats:
        clips.append(instantiate_clip(
            graphics[current_graphic],
            duration=beat - previous
        ))
        current_graphic = (current_graphic + 1) % len(graphics)
        previous = beat

    # Tail after the last beat
    clips.append(instantiate_clip(
            graphics[current_graphic],
            duration=duration - previous
    ))

    return clips

def instantiate_clip(graphic, duration):
    if is_video(graphic):
        clip = VideoFileClip(
            graphic
        ).subclipped(0, duration)
    else:
        clip = ImageClip(
            graphic,
            duration=duration
        )

    return clip

def is_video(file):
    if not file in is_video_cache:
        try:
            mime_type = magic.from_file(file, mime=True)
            is_video_cache[file] = \
                mime_type.startswith('video/') or mime_type == "image/gif"
        except Exception:
            is_video_cache[file] = False
    
    return is_video_cache[file]

def render(clips, audio_data, out):
    _, _, audio = audio_data

    video = concatenate_videoclips(clips, method="compose")
    fvideo = video.with_audio(audio)

    fvideo.write_videofile(
        out,
        fps=30,
        codec="libx264",
        audio_codec="aac",
    audio_bitrate="192k"
)

if __name__ == "__main__":
    main()
