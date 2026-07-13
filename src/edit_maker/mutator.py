from .graphics import is_video
from .logger import VideoWriteLogger

from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips, concatenate_audioclips
import tempfile
import os
import shutil
from tqdm import tqdm

def base_routine(inputs, save_as, action):
    """
    We can assume that all contents of `inputs` are of the same resource type (i.e. audio vs video)
    even though their file type may differ (e.g MP3 and OGG might both be part of the same list).
    The list length is constrained by `0 < len`.

    Callers should **NEVER** violate these constraints.
    """
    _, ext = os.path.splitext(os.path.basename(inputs[0]))
    ext = ext.lower()
    out = save_as or tempfile.mkstemp(suffix=ext)[1]

    clips = []
    for input in inputs:
        video = is_video(input)
        clips.append(
            VideoFileClip(input)
            if video else
            AudioFileClip(input)
        )

    res = action(clips)

    if video:
        res.write_videofile(
            out,
            logger=VideoWriteLogger(export_only=True)
        )
    else:
        res.write_audiofile(
            out,
            logger=VideoWriteLogger(print_substep=False)
        )

    if not save_as:
        # Overwrite input file
        shutil.move(out, inputs[0])

    tqdm.write("Saved as %s!" % save_as if save_as else "File mutated!")

def subclip(input, start, end, save_as):
    base_routine([input], save_as,
                 lambda clips: clips[0].subclipped(max(0, start), min(clips[0].duration, end)))
    
def cutout(input, start, end, save_as):
    base_routine([input], save_as,
                 lambda clips: clips[0].with_section_cut_out(max(0.0001, start), min(clips[0].duration, end)))

def scale_volume(input, factor, save_as):
    base_routine([input], save_as,
                 lambda clips: clips[0].without_audio() if factor == 0 and isinstance(clips[0], VideoFileClip) else clips[0].with_volume_scaled(factor))

def concat(inputs, save_as):
    base_routine(inputs, save_as,
                 lambda clips: concatenate_videoclips(clips, method="compose") if isinstance(clips[0], VideoFileClip) else concatenate_audioclips(clips))
