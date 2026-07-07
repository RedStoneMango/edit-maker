from .cli import parse_args
from .audio import analyze_audio
from .composition import build_clips, find_auto_size
from .renderer import render
from .dataholders import RenderOptions
from .transition import apply_transitions
from .graphics import shuffle_for_length

import random


def main():
    args = parse_args()

    print("Preparing...", end="") # Just in case find_auto_size takes too long

    render_options = RenderOptions(
        blur=args.background_blur,
        vignette=args.vignette,
        darken=args.darken
    )

    random.seed(args.seed) # Seed the global random

    size = args.size or find_auto_size(args.graphics)

    print("\r", end="") # We are ready to start!

    audio = analyze_audio(args.audio, args.beat_tightness, args.clips_per_beat)

    shuffled_clips = shuffle_for_length(args.graphics, len(audio.clip_durations))

    clips = build_clips(
        audio,
        shuffled_clips,
        size,
        render_options
    )

    clips = apply_transitions(
        clips,
        args.transitions
    )

    render(clips, audio, args.output)


if __name__ == "__main__":
    main()
