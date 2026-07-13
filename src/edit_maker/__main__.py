from .cli import parse_args
from .composition import find_auto_size
from .dataholders import *
from .generator import generate
from .audio import analyze_audio
from .ansi_colors import Colors
from .mutator import subclip, scale_volume, cutout, concat

import random
from tqdm import tqdm
import magic


def main():
    args = parse_args()
    if args.action == "generate":
        invoke_generator(args)
    elif args.action == "analyze-audio":
        invoke_audio_analysis(args)
    elif args.action == "mutate-file":
        invoke_mutation(args)
    else:
        tqdm.write("Invalid action: %s" % args.action)

def invoke_mutation(args):
    if args.mutation == "subclip":
        subclip(args.file, args.start, args.end, args.save_as)
    elif args.mutation == "volume":
        scale_volume(args.file, args.factor, args.save_as)
    elif args.mutation == "cutout":
        cutout(args.file, args.cutout_start, args.cutout_end, args.save_as)
    elif args.mutation == "concat":
        concat(args.files, args.result)
    else:
        tqdm.write("Invalid mutation: %s" % args.mutation)

def invoke_audio_analysis(args):
    file = args.audio_file
    data = analyze_audio(file, args.beat_tightness, args.clips_per_beat, args.intro_end_time, log=False)
    mime = magic.from_file(file, mime=True)

    tqdm.write(Colors.UNDERLINE + "File " + Colors.BOLD + file + Colors.END + Colors.UNDERLINE + ":" + Colors.END)
    tqdm.write("    " + Colors.BOLD + "Edit Clip Count:" + Colors.END + "  " + str(len(data.clip_durations)))
    tqdm.write("")
    tqdm.write("    " + Colors.BOLD + "File Type:" + Colors.END + "        " + mime)
    tqdm.write("")
    tqdm.write("    " + Colors.BOLD + "Audio Duration:" + Colors.END + "   " + str(data.duration))
    tqdm.write("    " + Colors.BOLD + "Audio FPS:" + Colors.END + "        " + str(data.clip.fps))
    tqdm.write("    " + Colors.BOLD + "Audio Channels:" + Colors.END + "   " + str(data.clip.nchannels))

def invoke_generator(args):
    print("Preparing...", end="")
    random.seed(args.seed)
    size = args.size or find_auto_size(args.graphics)
    print("\r", end="")

    generate(
        GeneralData(
            audio=args.audio,
            out=args.output,
            size=size
        ),
        BaseEditData(
            graphics=args.graphics,
            beat_tightness=args.beat_tightness,
            beat_deviation=args.beat_deviation,
            clips_per_beat=args.clips_per_beat,
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
                duration=args.intro_duration,
                play_audio=args.intro_audio_overlap is not None,
                audio_time_of_end = None if args.intro_audio_overlap == -1 else args.intro_audio_overlap,
                apply_effects=args.apply_intro_effects
            )
            if args.intro else None
        )
    )


if __name__ == "__main__":
    main()
