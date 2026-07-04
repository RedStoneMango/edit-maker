from .utils import zoom_translation

from moviepy import VideoClip, CompositeVideoClip, vfx

transitions = [
    {
        "name": "none",
        "factory": lambda prev_outro, this_intro: none(prev_outro, this_intro)
    },
    {
        "name": "black-fade",
        "factory": lambda prev_outro, this_intro: black_fade(prev_outro, this_intro)
    },
    {
        "name": "zoom-out",
        "factory": lambda prev_outro, this_intro: zoom_out(prev_outro, this_intro)
    },
    {
        "name": "zoom-out-fade",
        "factory": lambda prev_outro, this_intro: zoom_out_fade(prev_outro, this_intro)
    },
    {
        "name": "zoom-in",
        "factory": lambda prev_outro, this_intro: zoom_in(prev_outro, this_intro)
    },
    {
        "name": "zoom-in-fade",
        "factory": lambda prev_outro, this_intro: zoom_in_fade(prev_outro, this_intro)
    }
]

def none(prev_outro:VideoClip, this_intro:VideoClip):
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
