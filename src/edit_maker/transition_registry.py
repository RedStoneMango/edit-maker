from .utils import zoom_translation

from moviepy import VideoClip, CompositeVideoClip, vfx

transitions = [
    {
        "name": "jump",
        "factory": lambda prev_outro, this_intro: jump(prev_outro, this_intro)
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
    },
    {
        "name": "cross-fade",
        "factory": lambda prev_outro, this_intro: cross_fade(prev_outro, this_intro)
    },
    {
        "name": "slide-out-top",
        "factory": lambda prev_outro, this_intro: slide_out_top(prev_outro, this_intro)
    },
    {
        "name": "slide-out-left",
        "factory": lambda prev_outro, this_intro: slide_out_left(prev_outro, this_intro)
    },
    {
        "name": "slide-out-right",
        "factory": lambda prev_outro, this_intro: slide_out_right(prev_outro, this_intro)
    },
    {
        "name": "slide-out-bottom",
        "factory": lambda prev_outro, this_intro: slide_out_bottom(prev_outro, this_intro)
    },
    {
        "name": "slide-in-top",
        "factory": lambda prev_outro, this_intro: slide_in_top(prev_outro, this_intro)
    },
    {
        "name": "slide-in-left",
        "factory": lambda prev_outro, this_intro: slide_in_left(prev_outro, this_intro)
    },
    {
        "name": "slide-in-right",
        "factory": lambda prev_outro, this_intro: slide_in_right(prev_outro, this_intro)
    },
    {
        "name": "slide-in-bottom",
        "factory": lambda prev_outro, this_intro: slide_in_bottom(prev_outro, this_intro)
    },
    {
        "name": "walk-up",
        "factory": lambda prev_outro, this_intro: walk_up(prev_outro, this_intro)
    },
    {
        "name": "walk-left",
        "factory": lambda prev_outro, this_intro: walk_left(prev_outro, this_intro)
    },
    {
        "name": "walk-down",
        "factory": lambda prev_outro, this_intro: walk_down(prev_outro, this_intro)
    },
    {
        "name": "walk-right",
        "factory": lambda prev_outro, this_intro: walk_right(prev_outro, this_intro)
    }
]

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

def slide_out_top(prev_outro:VideoClip, this_intro:VideoClip):
    transition_duration = prev_outro.duration + this_intro.duration
    return [CompositeVideoClip([
        this_intro \
            .with_speed_scaled(final_duration=transition_duration),
        prev_outro \
            # Apply speed first so we dont mess up slide effect 
            .with_speed_scaled(final_duration=transition_duration) \
            .with_effects([vfx.SlideOut(transition_duration, "top")])
    ])]

def slide_out_left(prev_outro:VideoClip, this_intro:VideoClip):
    transition_duration = prev_outro.duration + this_intro.duration
    return [CompositeVideoClip([
        this_intro \
            .with_speed_scaled(final_duration=transition_duration),
        prev_outro \
            # Apply speed first so we dont mess up slide effect 
            .with_speed_scaled(final_duration=transition_duration) \
            .with_effects([vfx.SlideOut(transition_duration, "left")])
    ])]

def slide_out_right(prev_outro:VideoClip, this_intro:VideoClip):
    transition_duration = prev_outro.duration + this_intro.duration
    return [CompositeVideoClip([
        this_intro \
            .with_speed_scaled(final_duration=transition_duration),
        prev_outro \
            # Apply speed first so we dont mess up slide effect 
            .with_speed_scaled(final_duration=transition_duration) \
            .with_effects([vfx.SlideOut(transition_duration, "right")])
    ])]

def slide_out_bottom(prev_outro:VideoClip, this_intro:VideoClip):
    transition_duration = prev_outro.duration + this_intro.duration
    return [CompositeVideoClip([
        this_intro \
            .with_speed_scaled(final_duration=transition_duration),
        prev_outro \
            # Apply speed first so we dont mess up slide effect 
            .with_speed_scaled(final_duration=transition_duration) \
            .with_effects([vfx.SlideOut(transition_duration, "bottom")])
    ])]


def slide_in_top(prev_outro:VideoClip, this_intro:VideoClip):
    transition_duration = prev_outro.duration + this_intro.duration
    return [CompositeVideoClip([
        prev_outro \
            .with_speed_scaled(final_duration=transition_duration),
        this_intro \
            # Apply speed first so we dont mess up slide effect 
            .with_speed_scaled(final_duration=transition_duration) \
            .with_effects([vfx.SlideIn(transition_duration, "top")])
    ])]

def slide_in_left(prev_outro:VideoClip, this_intro:VideoClip):
    transition_duration = prev_outro.duration + this_intro.duration
    return [CompositeVideoClip([
        prev_outro \
            .with_speed_scaled(final_duration=transition_duration),
        this_intro \
            # Apply speed first so we dont mess up slide effect 
            .with_speed_scaled(final_duration=transition_duration) \
            .with_effects([vfx.SlideIn(transition_duration, "left")])
    ])]

def slide_in_right(prev_outro:VideoClip, this_intro:VideoClip):
    transition_duration = prev_outro.duration + this_intro.duration
    return [CompositeVideoClip([
        prev_outro \
            .with_speed_scaled(final_duration=transition_duration),
        this_intro \
            # Apply speed first so we dont mess up slide effect 
            .with_speed_scaled(final_duration=transition_duration) \
            .with_effects([vfx.SlideIn(transition_duration, "right")])
    ])]

def slide_in_bottom(prev_outro:VideoClip, this_intro:VideoClip):
    transition_duration = prev_outro.duration + this_intro.duration
    return [CompositeVideoClip([
        prev_outro \
            .with_speed_scaled(final_duration=transition_duration),
        this_intro \
            # Apply speed first so we dont mess up slide effect 
            .with_speed_scaled(final_duration=transition_duration) \
            .with_effects([vfx.SlideIn(transition_duration, "bottom")])
    ])]

def walk_up(prev_outro:VideoClip, this_intro:VideoClip):
    transition_duration = prev_outro.duration + this_intro.duration
    return [CompositeVideoClip([
        prev_outro \
            .with_speed_scaled(final_duration=transition_duration) \
            .with_effects([vfx.SlideOut(transition_duration, "top")]),
        this_intro \
            .with_speed_scaled(final_duration=transition_duration) \
            .with_effects([vfx.SlideIn(transition_duration, "bottom")])
    ])]

def walk_left(prev_outro:VideoClip, this_intro:VideoClip):
    transition_duration = prev_outro.duration + this_intro.duration
    return [CompositeVideoClip([
        prev_outro \
            .with_speed_scaled(final_duration=transition_duration) \
            .with_effects([vfx.SlideOut(transition_duration, "left")]),
        this_intro \
            .with_speed_scaled(final_duration=transition_duration) \
            .with_effects([vfx.SlideIn(transition_duration, "right")])
    ])]

def walk_down(prev_outro:VideoClip, this_intro:VideoClip):
    transition_duration = prev_outro.duration + this_intro.duration
    return [CompositeVideoClip([
        prev_outro \
            .with_speed_scaled(final_duration=transition_duration) \
            .with_effects([vfx.SlideOut(transition_duration, "bottom")]),
        this_intro \
            .with_speed_scaled(final_duration=transition_duration) \
            .with_effects([vfx.SlideIn(transition_duration, "top")])
    ])]

def walk_right(prev_outro:VideoClip, this_intro:VideoClip):
    transition_duration = prev_outro.duration + this_intro.duration
    return [CompositeVideoClip([
        prev_outro \
            .with_speed_scaled(final_duration=transition_duration) \
            .with_effects([vfx.SlideOut(transition_duration, "right")]),
        this_intro \
            .with_speed_scaled(final_duration=transition_duration) \
            .with_effects([vfx.SlideIn(transition_duration, "left")])
    ])]
