from .transition_registry import get_transitions_from_literal, get_transitions_from_abbr, default_transitions
from .utils import raise_
from .graphics import is_valid_graphic
from .audio import is_valid_audio

import argparse
import os
import re
from moviepy.tools import convert_to_seconds

def size_type(strings):    
    if "," not in strings and "x" not in strings and "×" not in strings:
        raise argparse.ArgumentTypeError("Should be of format WIDTH,HEIGHT or WIDTHxHEIGHT")

    try:
        tuple_int = tuple(map(int, strings.split("x")))
    except:
        try:
            tuple_int = tuple(map(int, strings.split("×")))
        except:
            try:
                tuple_int = tuple(map(int, strings.split(",")))
            except:
                raise argparse.ArgumentTypeError("Values should be positive integers")
        
    if len(tuple_int) != 2:
        raise argparse.ArgumentTypeError("Should be of format WIDTH,HEIGHT or WIDTHxHEIGHT")
    if tuple_int[0] <= 0 or tuple_int[1] <= 0:
        raise argparse.ArgumentTypeError("Should be greater than 0")
    return tuple_int

def audio_file_type(string):
    if not os.path.isfile(string):
        raise argparse.ArgumentTypeError("File '" + string  + "' does not exist")
    if not is_valid_audio(string):
        raise argparse.ArgumentTypeError("File '" + string  + "' is not an audio")
    return string

def graphic_file_type(string):
    if not os.path.isfile(string):
        raise argparse.ArgumentTypeError("File '" + string  + "' does not exist")
    if not is_valid_graphic(string):
        raise argparse.ArgumentTypeError("File '" + string  + "' is not an image or video")
    return string

def positive_float_type(string):
    try:
        f = float(string)
    except:
        raise argparse.ArgumentTypeError("Should be a (decimal) number")
    if f < 0:
        raise argparse.ArgumentTypeError("Should be greater or equal to 0")
    return f

def positive_float_type_no_zero(string):
    try:
        f = float(string)
    except:
        raise argparse.ArgumentTypeError("Should be a (decimal) number")
    if f <= 0:
        raise argparse.ArgumentTypeError("Should be greater than 0")
    return f

def positive_int_type(string):
    try:
        i = int(string)
    except:
        raise argparse.ArgumentTypeError("Should be an integer")
    if i <= 0:
        raise argparse.ArgumentTypeError("Should be greater than 0")
    return i

def deactivatable_positive_float_type(string):
    if string.lower().strip() == "off":
        return None

    try:
        f = float(string)
    except:
        raise argparse.ArgumentTypeError("Should be a (decimal) number or 'off'")
    if f < 0:
        raise argparse.ArgumentTypeError("Should be greater or equal to 0")
    return f

def transition_list_type(arg):
    if arg == "":
        raise argparse.ArgumentTypeError("At least one transition must be specified")
    
    if re.compile("\\d+").match(arg):
        return get_transitions_from_abbr(
            arg,
            lambda error: raise_(argparse.ArgumentTypeError(error))
        )

    return get_transitions_from_literal(
        arg.split(","),
        lambda error: raise_(argparse.ArgumentTypeError(error))
    )

def timestamp_type(arg):
    try:
        secs = convert_to_seconds(arg) # Fork out to moviepy utility
    except ValueError as e:
        raise argparse.ArgumentTypeError("Invalid timestamp format")
    return secs


def parse_args():
    parser = argparse.ArgumentParser("edit-maker", description="Wrapper for generating TikTok edits using the 'generate' action. Other utilities are included as well")
    subparsers = parser.add_subparsers(dest="action")

    generate_description="Easily generate TikTok edits purely by providing an audio and image files. No video editing skills needed."
    generate_parser = subparsers.add_parser("generate", help=generate_description, description=generate_description)
    generate_parser.add_argument("audio", help="The audio file to use for the edit", type=audio_file_type)
    generate_parser.add_argument("output", help="The output file to save the edit in", type=str) # Output is not required to exist, therefore no file_type
    generate_parser.add_argument("graphics", help="The graphics to be used in the edit", type=graphic_file_type, nargs="+")
    generate_parser.add_argument("--beat-tightness", help="The tightness of the detected audio beat distribution around the tempo of the audio file. Must be greater or equal 0 and can have decimal points", type=positive_float_type, default=100, required=False)
    generate_parser.add_argument("--size", "-s", help="The size of the resulting edit in format WIDTH,HEIGHT / WIDTHxHEIGHT. This will scale all graphics to this value while respecting the aspect ratio. Without this option, the size is the max width/height of the provided graphics", type=size_type, default=None, required=False, metavar="WIDTH,HEIGHT|WIDTHxHEIGHT")
    generate_parser.add_argument("--background-blur", "-B", help="Enables background blur for graphics whose size does not match the canvas size. Instead of a black area the outer part of the graphic will be a blurred version of the graphic itself", action="store_true")
    generate_parser.add_argument("--clips-per-beat", "-c", help="The amount of clips to be displayed per audio beat. Can be a decimal number but must be greater than 0. Default: 1", required=False, default=1, type=positive_float_type_no_zero)
    generate_parser.add_argument("--darken", "-d", help="The intensity of the darkening effect to be applied to every clip or 'off' to deactivate. Default: off", required=False, default=None, type=deactivatable_positive_float_type, metavar="DARKEN|off")
    generate_parser.add_argument("--vignette", "-V", help="The base brightness of the vignette effect to be applied to every clip or 'off' to deactivate. Default: 0.8", required=False, default=0.8, type=deactivatable_positive_float_type, metavar="VIGNETTE|off")
    generate_parser.add_argument("--transitions", "-t", help="The allowed transitions between graphic clips. Can be either a comma-separated list of names with optional weighting or a transition abbreviation. Refer to the documentation for further information", required=False, default=default_transitions(), type=transition_list_type)
    generate_parser.add_argument("--intro", "-i", help="An optinal graphic file that is prepended to the edit but does get transitions applied. Useful for edits with an introduction clip before the edit itself starts", required=False, default=None, type=graphic_file_type)
    generate_parser.add_argument("--intro-duration", help="Specifies the length of the edit intro. The intro is sped up / down in such a way that its end (the edit's start) directly aligns with the provided audio timestamp. If this option is not provided, the intro's natural length is used. Has no effect if no --intro is provided", required=False, default=None, type=timestamp_type)
    generate_parser.add_argument("--intro-audio-overlap", help="Enables the edit audio to start playing while the intro is still active. If an argument is provided, it is interpret as the timestamp of the audio playback at which the intro will end. Has no effect if no --intro is provided", nargs="?", const=-1, required=False, default=None, type=timestamp_type, metavar="AUDIO-END-TIMESTAMP")
    generate_parser.add_argument("--apply-intro-effects", help="Applies the darken and vignette effects to the intro as well as configured by the '--vignette' and '--darken' options for the base edit", required=False, action="store_true")
    generate_parser.add_argument("--seed", help="The seed to be used for random choices. When generating multiple videos with the same seed and same transition setting, the random choices are guaranteed to be the same random sequence. Can be any text", required=False, default=None, type=str)

    analyze_description="Analyze an audio file and dump the amount of clips what will be used when generating an edit with this audio using the 'generate' action"
    analyze_parser = subparsers.add_parser("analyze-audio", help=analyze_description, description=analyze_description)
    analyze_parser.add_argument("audio_file", help="The audio file to analyze", type=audio_file_type)
    analyze_parser.add_argument("--beat-tightness", "-t", help="The tightness of the detected audio beat distribution around the tempo of the audio file. Must be greater or equal 0 and can have decimal points", type=positive_float_type, default=100, required=False)
    analyze_parser.add_argument("--clips-per-beat", "-c", help="The amount of clips to be displayed per audio beat. Can be a decimal number but must be greater than 0. Default: 1", required=False, default=1, type=positive_float_type_no_zero)
    analyze_parser.add_argument("--intro-end-time", "-e", help="Acts as if '--intro-audio-overlap' was used for 'generate', i.e. the edit audio starts playing while the intro is still active. The argument is the timestamp of the audio playback at which the intro would end", required=False, default=0, type=timestamp_type, metavar="AUDIO-END-TIMESTAMP")


    muatate_description="Basic mutations on audio or graphic files like cutting or volume adjustments for pre-editing data before generating an edit"
    mutate_parser = subparsers.add_parser("mutate-file", help=muatate_description, description=muatate_description)
    
    return parser.parse_args()
