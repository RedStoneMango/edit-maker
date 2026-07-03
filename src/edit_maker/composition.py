from .graphics import instantiate_clip
from .records import RenderOptions
from .utils import contain_scale, cover_scale
from .effects import Blur
from .records import AudioData

from moviepy import CompositeVideoClip

def build_clips(audio_data:AudioData, graphics, size, render_options:RenderOptions):
    audio_data
    clips = []

    current_graphic = 0
    previous = 0

    for beat in audio_data.beats:
        clips.append(access_clip(
            graphics[current_graphic],
            beat - previous,
            size,
            render_options
        ))
        current_graphic = (current_graphic + 1) % len(graphics)
        previous = beat

    # Tail after the last beat
    clips.append(access_clip(
            graphics[current_graphic],
            audio_data.duration - previous,
            size,
            render_options
    ))

    return clips

def find_auto_size(graphics):
    size = (0, 0)
    for graphic in graphics:
        inst = instantiate_clip(graphic)
        size = tuple(max(a, b) for a, b in zip(size, inst.size))
    return size

def access_clip(graphic, duration, size, render_options:RenderOptions):
    clip = instantiate_clip(graphic, duration=duration)

    scale = contain_scale(
        clip.w, clip.h,
        size[0], size[1]
    )

    clip = clip.resized(scale)
    
    if render_options.blur:
        return blur_background(clip, size)
    return clip


def blur_background(clip, canvas_size):
    if clip.size == canvas_size:
        return clip
    
    scale = cover_scale(
        clip.w, clip.h,
        canvas_size[0], canvas_size[1]
    )

    bg = clip \
        .resized(scale) \
        .with_effects([Blur(intensity=200)]) \
        .with_position("center")

    return CompositeVideoClip([bg, clip.with_position("center")], size=canvas_size)
