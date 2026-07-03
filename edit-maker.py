#!/usr/bin/env python3

import argparse
import os

def size_type(strings):    
    strings = strings.replace("(", "").replace(")", "")
    try:
        tuple_int = tuple(map(int, strings.split("x")))
    except:
        try:
            tuple_int = tuple(map(int, strings.split(",")))
        except:
            raise argparse.ArgumentTypeError("Values should be positive integers")
    if len(tuple_int) != 2:
        raise argparse.ArgumentTypeError("Should be of format WIDTH,HEIGHT or WIDTHxHEIGHT")
    if tuple_int[0] <= 0 or tuple_int[1] <= 0:
        raise argparse.ArgumentTypeError("Should be greater than 0")
    return tuple_int

def file_type(string):
    if not os.path.isfile(string):
        raise argparse.ArgumentTypeError("File '" + string  + "' does not exist")
    return string

def positive_float_type(string):
    try:
        f = float(string)
    except:
        raise argparse.ArgumentTypeError("Should be a (decimal) number")
    if f < 0:
        raise argparse.ArgumentTypeError("Should be geater or equal to 0")
    return f

arg_parser = argparse.ArgumentParser("edit-maker", description="Generates TikTok edits")
arg_parser.add_argument("audio", help="The audio file to use for the edit", type=file_type)
arg_parser.add_argument("output", help="The output file to save the edit in", type=str) # Output is not required to exist, therefore no file_type
arg_parser.add_argument("graphics", help="The graphics to be used in the edit", type=file_type, nargs="+")
arg_parser.add_argument("--beat-tightness", "-t", help="The tightness of the detected audio beat distribution around the tempo of the audio file. Must be greater or equal 0 and can have decimal points", type=positive_float_type, default=100, required=False)
arg_parser.add_argument("--size", "-s", help="The size of the resulting edit in format WIDTH,HEIGHT / WIDTHxHEIGHT. This will scale all graphics to this value while respecting the aspect ratio. Without this option, the size is the max width/height of the provided graphics", type=size_type, default=None, required=False, metavar="[WIDTH,HEIGHT|WIDTHxHEIGHT]")

import librosa
import magic
from moviepy import AudioFileClip, ImageClip, VideoFileClip, concatenate_videoclips

is_video_cache = {}

def main():
    args = arg_parser.parse_args()

    size = args.size
    if size == None:
        size = find_auto_size(args.graphics)
    
    audio_data = analyze_audio(args.audio, args.beat_tightness)
    clips = build_clips(audio_data, args.graphics, size)
    render(clips, audio_data, args.output)

def find_auto_size(graphics):
    size = (0, 0)
    for graphic in graphics:
        inst = instantiate_clip(graphic)
        size = tuple(max(a, b) for a, b in zip(size, inst.size))
    return size

def analyze_audio(audio_path, tightness):
    y, sr = librosa.load(audio_path)
    _, beat_frames = librosa.beat.beat_track(y=y, sr=sr, tightness=tightness)
    beats = librosa.frames_to_time(beat_frames, sr=sr)
    audio = AudioFileClip(audio_path)
    return (beats, audio.duration, audio)

def build_clips(audio_data, graphics, size):
    beats, duration, _ = audio_data
    clips = []

    current_graphic = 0
    previous = 0

    for beat in beats:
        clips.append(access_clip(
            graphics[current_graphic],
            beat - previous,
            size
        ))
        current_graphic = (current_graphic + 1) % len(graphics)
        previous = beat

    # Tail after the last beat
    clips.append(access_clip(
            graphics[current_graphic],
            duration - previous,
            size
    ))

    return clips

def access_clip(graphic, duration, size):
    clip = instantiate_clip(graphic, duration=duration)

    canvas_w, canvas_h = size
    if canvas_w / clip.w < canvas_h / clip.h:
        clip = clip.resized(width=size[0])
    else:
        clip = clip.resized(height=size[1])
    
    return clip

# When needed, directly provide the duration value to improve performance
#  with ImageClip creation
def instantiate_clip(graphic, duration=None):
    if is_video(graphic):
        clip = VideoFileClip(
            graphic
        )
        if duration != None:
            clip = clip.subclipped(0, duration)
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
