from .utils import zoom_translation

from moviepy import VideoClip, CompositeVideoClip, vfx
import random
import re

literal_entry_pattern = re.compile("^(\\d)?:?([a-z-]+)$")

def get_transitions_from_literal(entries:list[str] | None, error_callback):
    res = []
    for entry in entries:
        match = literal_entry_pattern.match(entry)
        if not match:
            error_callback("Invalid transition pattern '%s'. Should be 'NAME,' "
            "or 'WEIGTH:NAME,' or a chain of %s digits" % (entry, len(transitions)))
            return None
        
        weight = match.group(1)
        weight = int(weight) if weight else 1
        key = match.group(2)
        if key not in transitions:
            error_callback("Invalid transition name '%s'" % key)
            return None

        for _ in range(0, weight): # If higher weight, add more entries
            res.append(transitions.get(key))

    if len(res) == 0:
        error_callback("At least one transition must be specified")

    return res

def get_transitions_from_abbr(abbr: str, error_callback):
    res = []
    options = list(transitions.values())
    options_len = len(options)
    abbr_len = len(abbr)

    for i in range(0, options_len):
        weight = int(abbr[i]) if abbr_len > i else 0 # Bounds check to ensure forwards compatibility
        for _ in range(0, weight): # If higher weight, add more entries
            res.append(options[i])

    if len(res) == 0:
        error_callback("At least one transition must be specified")
        return None

    return res

def default_transitions():
    return list(transitions.values())

def jump(prev_outro:VideoClip, this_intro:VideoClip):
    return [prev_outro, this_intro]

def black_fade(prev_outro:VideoClip, this_intro:VideoClip):
    return [
        prev_outro.with_effects([vfx.FadeOut(prev_outro.duration)]),
        this_intro.with_effects([vfx.FadeIn(this_intro.duration)])
    ]

def zoom_out(prev_outro:VideoClip, this_intro:VideoClip):
    return [
        prev_outro.with_effects([vfx.Resize(zoom_translation(1, 0.5, prev_outro.duration))]),
        this_intro.with_effects([vfx.Resize(zoom_translation(0.5, 1, prev_outro.duration))])
    ]

def zoom_out_fade(prev_outro:VideoClip, this_intro:VideoClip):
    return [
        prev_outro.with_effects([
            vfx.Resize(zoom_translation(1, 0.5, prev_outro.duration)),
            vfx.FadeOut(prev_outro.duration)
        ]),
        this_intro.with_effects([
            vfx.Resize(zoom_translation(0.5, 1, prev_outro.duration)),
            vfx.FadeIn(this_intro.duration)
        ])
    ]

def zoom_in(prev_outro:VideoClip, this_intro:VideoClip):
    zoom_outro = (
        prev_outro.resized(zoom_translation(1, 1.5, prev_outro.duration))
        .with_position(('center', 'center'))
    )
    cropped_outro = CompositeVideoClip([zoom_outro], size=prev_outro.size)

    zoom_intro = (
        this_intro.resized(zoom_translation(1.5, 1, prev_outro.duration))
        .with_position(('center', 'center'))
    )
    cropped_intro = CompositeVideoClip([zoom_intro], size=this_intro.size)

    return [cropped_outro, cropped_intro]

def zoom_in_fade(prev_outro:VideoClip, this_intro:VideoClip):
    zoom_outro = (
        prev_outro.resized(zoom_translation(1, 1.5, prev_outro.duration))
        .with_position(('center', 'center'))
    )
    cropped_outro = CompositeVideoClip([zoom_outro], size=prev_outro.size) \
        .with_effects([vfx.FadeOut(prev_outro.duration)])

    zoom_intro = (
        this_intro.resized(zoom_translation(1.5, 1, prev_outro.duration))
        .with_position(('center', 'center'))
    )
    cropped_intro = CompositeVideoClip([zoom_intro], size=this_intro.size) \
        .with_effects([vfx.FadeIn(this_intro.duration)])

    return [cropped_outro, cropped_intro]

def cross_fade(prev_outro:VideoClip, this_intro:VideoClip):
    # Since both clips are played simultaneously, we gotta slow them
    #  down a bit so the transition duration still fits
    transition_duration = prev_outro.duration + this_intro.duration
    return [CompositeVideoClip([
        prev_outro \
            .with_effects([vfx.CrossFadeOut(transition_duration)]) \
            .with_speed_scaled(final_duration=transition_duration),
        this_intro \
            .with_effects([vfx.CrossFadeIn(transition_duration)]) \
            .with_speed_scaled(final_duration=transition_duration)
    ])]

def slide_out(prev_outro:VideoClip, this_intro:VideoClip):
    transition_duration = prev_outro.duration + this_intro.duration
    return [CompositeVideoClip([
        this_intro \
            .with_speed_scaled(final_duration=transition_duration),
        prev_outro \
            # Apply speed first so we dont mess up slide effect 
            .with_speed_scaled(final_duration=transition_duration) \
            .with_effects([vfx.SlideOut(transition_duration, rand_side())])
    ])]


def slide_in(prev_outro:VideoClip, this_intro:VideoClip):
    transition_duration = prev_outro.duration + this_intro.duration
    return [CompositeVideoClip([
        prev_outro \
            .with_speed_scaled(final_duration=transition_duration),
        this_intro \
            # Apply speed first so we dont mess up slide effect 
            .with_speed_scaled(final_duration=transition_duration) \
            .with_effects([vfx.SlideIn(transition_duration, rand_side())])
    ])]

def walk(prev_outro:VideoClip, this_intro:VideoClip):
    transition_duration = prev_outro.duration + this_intro.duration
    side = rand_side()

    return [CompositeVideoClip([
        prev_outro \
            .with_speed_scaled(final_duration=transition_duration) \
            .with_effects([vfx.SlideOut(transition_duration, side)]),
        this_intro \
            .with_speed_scaled(final_duration=transition_duration) \
            .with_effects([vfx.SlideIn(transition_duration, opposite_side(side))])
    ])]

def rand_side():
    return random.choice(["top", "left", "bottom", "right"])
def opposite_side(side):
    match side:
        case "top": return "bottom"
        case "left": return "right"
        case "bottom": return "top"
        case "right": return "left"
        case _: raise ValueError("Side has to be one of ['top', 'left', 'bottom', 'right']")


transitions = {
    "jump": jump,
    "black-fade": black_fade,
    "cross-fade": cross_fade,
    "zoom-out": zoom_out,
    "zoom-out-fade": zoom_out_fade,
    "zoom-in": zoom_in,
    "zoom-in-fade": zoom_in_fade,
    "slide-out": slide_out,
    "slide-in": slide_in,
    "walk": walk,
}