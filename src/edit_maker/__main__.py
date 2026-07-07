from .cli import parse_args
from .composition import find_auto_size
from .dataholders import *
from .generator import generate

import random


def main():
    args = parse_args()

    print("Preparing...", end="")
    random.seed(args.seed)
    size = args.size or find_auto_size(args.graphics)
    print("\r", end="")

    generate(
        GeneralData(
            audio=args.audio,
            out=args.output
        ),
        BaseEditData(
            graphics=args.graphics,
            beat_tightness=args.beat_tightness,
            clips_per_beat=args.clips_per_beat,
            size=size,
            render_options=RenderOptions(
                blur=args.background_blur,
                vignette=args.vignette,
                darken=args.darken
            ),
            transitions=args.transitions
        ),
        intro=(
            IntroData(
                graphic=args.intro,
                duration=args.intro_audio
            )
            if args.intro else None
        )
    )


if __name__ == "__main__":
    main()
