from .cli import parse_args
from .audio import analyze_audio
from .composition import build_clips, find_auto_size
from .renderer import render
from .dataholders import RenderOptions


def main():
    args = parse_args()

    size = args.size or find_auto_size(args.graphics)

    audio = analyze_audio(args.audio, args.beat_tightness)

    clips = build_clips(
        audio,
        args.graphics,
        size,
        RenderOptions(
            blur=not args.no_background_blur,
            graphic_beats=args.graphic_beats
        )
    )

    render(clips, audio, args.output)


if __name__ == "__main__":
    main()
