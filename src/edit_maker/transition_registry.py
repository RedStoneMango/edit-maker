from .utils import zoom_in, zoom_out, rotate_in, rotate_out

from moviepy import VideoClip

transitions = [
    {
        "name": "none",
        "factory": lambda prev_outro, this_intro: none(prev_outro, this_intro)
    }
]

def none(prev_outro:VideoClip, this_intro:VideoClip):
    return [prev_outro, this_intro]
