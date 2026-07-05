import argparse
import os

def size_type(strings):    
    strings = strings.replace("(", "").replace(")", "")
    try:
        tuple_int = tuple(map(int, strings.split("x")))
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

def positive_int_type(string):
    try:
        i = int(string)
    except:
        raise argparse.ArgumentTypeError("Should be an integer")
    if i <= 0:
        raise argparse.ArgumentTypeError("Should be greater than 0")
    return i

def parse_args():
    parser = argparse.ArgumentParser("edit-maker", description="Easily generate TikTok edits purely by providing an audio and image files. No video editing skills needed.")

    parser.add_argument("audio", help="The audio file to use for the edit", type=file_type)
    parser.add_argument("output", help="The output file to save the edit in", type=str) # Output is not required to exist, therefore no file_type
    parser.add_argument("graphics", help="The graphics to be used in the edit", type=file_type, nargs="+")
    parser.add_argument("--beat-tightness", "-t", help="The tightness of the detected audio beat distribution around the tempo of the audio file. Must be greater or equal 0 and can have decimal points", type=positive_float_type, default=100, required=False)
    parser.add_argument("--size", "-s", help="The size of the resulting edit in format WIDTH,HEIGHT / WIDTHxHEIGHT. This will scale all graphics to this value while respecting the aspect ratio. Without this option, the size is the max width/height of the provided graphics", type=size_type, default=None, required=False, metavar="[WIDTH,HEIGHT|WIDTHxHEIGHT]")
    parser.add_argument("--background-blur", "-B", help="Enables background blur for graphics whose size does not match the canvas size. Instead of a black area the outer part of the graphic will be a blurred version of the graphic itself", action="store_true")
    parser.add_argument("--graphic-beats", "-b", help="The amount of beats a graphic should be displayed", required=False, default=1, type=positive_int_type)
    
    return parser.parse_args()
