from .transition_registry import get_transitions_from_literal, get_transitions_from_abbr, default_transitions
from .utils import raise_

import argparse
import os
import re

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

def file_type(string):
    if not os.path.isfile(string):
        raise argparse.ArgumentTypeError("File '" + string  + "' does not exist")
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


def parse_args():
    parser = argparse.ArgumentParser("edit-maker", description="Easily generate TikTok edits purely by providing an audio and image files. No video editing skills needed.")

    parser.add_argument("audio", help="The audio file to use for the edit", type=file_type)
    parser.add_argument("output", help="The output file to save the edit in", type=str) # Output is not required to exist, therefore no file_type
    parser.add_argument("graphics", help="The graphics to be used in the edit", type=file_type, nargs="+")
    parser.add_argument("--beat-tightness", help="The tightness of the detected audio beat distribution around the tempo of the audio file. Must be greater or equal 0 and can have decimal points", type=positive_float_type, default=100, required=False)
    parser.add_argument("--size", "-s", help="The size of the resulting edit in format WIDTH,HEIGHT / WIDTHxHEIGHT. This will scale all graphics to this value while respecting the aspect ratio. Without this option, the size is the max width/height of the provided graphics", type=size_type, default=None, required=False, metavar="[WIDTH,HEIGHT|WIDTHxHEIGHT]")
    parser.add_argument("--background-blur", "-B", help="Enables background blur for graphics whose size does not match the canvas size. Instead of a black area the outer part of the graphic will be a blurred version of the graphic itself", action="store_true")
    parser.add_argument("--clips-per-beat", "-c", help="The amount of clips to be displayed per audio beat. Can be a decimal number but must be greater than 0. Default: 1", required=False, default=1, type=positive_float_type_no_zero)
    parser.add_argument("--darken", "-d", help="The intensity of the darkening effect to be applied to every clip or 'off' to deactivate. Default: off", required=False, default=None, type=deactivatable_positive_float_type, metavar="[DARKEN|off]")
    parser.add_argument("--vignette", "-V", help="The base brightness of the vignette effect to be applied to every clip or 'off' to deactivate. Default: 0.8", required=False, default=0.8, type=deactivatable_positive_float_type, metavar="[VIGNETTE|off]")
    parser.add_argument("--transitions", "-t", help="The allowed transitions between graphic clips. Can be either a comma-separated list of names with optional weighting or a transition abbreviation. Refer to the documentation for further information", required=False, default=default_transitions(), type=transition_list_type)
    parser.add_argument("--seed", help="The seed to be used for random choices. When generating multiple videos with the same seed and same transition setting, the transitions are guaranteed to be the same random sequence. Can be any text", required=False, default=None, type=str)
    
    return parser.parse_args()
