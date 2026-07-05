from .cli import parse_args
from .audio import analyze_audio
from .composition import build_clips, find_auto_size
from .renderer import render
from .dataholders import RenderOptions
from .transition import apply_transitions


def main():
    args = parse_args()
    render_options = RenderOptions(
        blur=args.background_blur,
        graphic_beats=args.graphic_beats
    )

    size = args.size or find_auto_size(args.graphics)

    audio = analyze_audio(args.audio, args.beat_tightness)

    clips = build_clips(
        audio,
        args.graphics,
        size,
        render_options
    )

    clips = apply_transitions(
        clips
    )

    render(clips, audio, args.output)


if __name__ == "__main__":
    main()
