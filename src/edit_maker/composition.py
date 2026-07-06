from .graphics import instantiate_clip
from .dataholders import RenderOptions
from .utils import contain_scale, cover_scale
from .effects import Blur, vignette_clip, darken_clip
from .dataholders import AudioData

from moviepy import CompositeVideoClip, ColorClip
from proglog import default_bar_logger

def build_clips(audio_data:AudioData, graphics, size, render_options:RenderOptions):
    logger = default_bar_logger("bar")
    logger(message="[2/5]  Generating beat-syncronized graphic clips")

    clips = []
    current_graphic = 0

    for clip_duration in logger.iter_bar(entry=audio_data.clip_durations):
        clips.append(prepare_clip(
            graphics[current_graphic],
            clip_duration,
            size,
            render_options
        ))
        current_graphic = (current_graphic + 1) % len(graphics)

    return clips

def find_auto_size(graphics):
    size = (0, 0)
    for graphic in graphics:
        inst = instantiate_clip(graphic)
        size = tuple(max(a, b) for a, b in zip(size, inst.size))
    return size

def prepare_clip(graphic, duration, size, render_options:RenderOptions):
    clip = instantiate_clip(graphic, duration=duration)

    scale = contain_scale(
        clip.w, clip.h,
        size[0], size[1]
    )
    clip = clip.resized(scale)

    if render_options.darken is not None:
        clip = darken_clip(clip, render_options.darken)
    if render_options.vignette is not None:
        clip = vignette_clip(clip, render_options.vignette)

    if render_options.blur:
        clip = blur_background(clip, size)
    else:
        clip = black_background(clip, size)
    
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

def black_background(clip, canvas_size):
    if clip.size == canvas_size:
        return clip

    bg = ColorClip(size=canvas_size, duration=clip.duration).with_position("center")
    return CompositeVideoClip([bg, clip.with_position("center")], size=canvas_size)
